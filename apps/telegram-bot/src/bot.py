#!/usr/bin/env python3
"""
Telegram Bot для ai-workspace
Двусторонняя связь: принимает сообщения от пользователя и отправляет по HTTP API
"""

import os
import sys
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand, MessageEntity
from aiogram.filters import CommandStart, Command
from aiohttp import web
from loguru import logger
from dotenv import load_dotenv

# Загрузка .env (docker-compose уже загружает через env_file, но на всякий случай)
load_dotenv("/opt/ai-workspace/.env")

# Конфигурация
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))
HTTP_PORT = int(os.getenv("BOT_HTTP_PORT", "8081"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CLAUDE_CLI_PATH = "/usr/local/bin/claude"  # Полный путь к Claude CLI

# Настройка логирования
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL
)
logger.add(
    "/app/logs/bot_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    level="DEBUG"
)

# Проверка конфигурации
if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не установлен в .env!")
    sys.exit(1)

if not ALLOWED_CHAT_ID:
    logger.error("TELEGRAM_CHAT_ID не установлен в .env!")
    sys.exit(1)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# История сообщений (для логирования)
message_history = []

# === SESSION MANAGEMENT ===

# Пути к файлам сессии
SESSION_FILE = "/opt/ai-workspace/apps/telegram-bot/active_session.txt"
CONTEXT_FILE = "/opt/ai-workspace/apps/telegram-bot/telegram_agent_context.md"
CLAUDE_WORKING_DIR = "/opt/ai-workspace"

# Время последней активности (для проверки неактивности)
last_activity_time = time.time()

# Флаги отправленных уведомлений
notification_30min_sent = False
notification_8h_sent = False

# Активный процесс Claude (для возможности остановки)
active_claude_process = None

# Текущая модель Claude (по умолчанию opus - умный режим)
current_model = "opus"

# Флаг блокировки параллельных сессий
is_processing = False

# Флаг процесса остановки (для защиты от race condition)
is_stopping = False

# Кеш для медиа-групп (альбомов с несколькими файлами)
# Структура: {media_group_id: {'messages': [Message, ...], 'timer': asyncio.Task}}
media_groups_cache = {}

# Трекинг промежуточных сообщений для прогресс-индикатора
intermediate_message_ids = []  # ID всех промежуточных сообщений от бота
current_hourglass_message_id = None  # ID текущего ⌛ сообщения

# === MULTI-MESSAGE ACCUMULATION STATE ===

# Режим /multi (явный)
multi_mode_active = False
multi_messages = []
multi_control_message_ids = []

# Авто-режим (неявный, с таймером 5 сек)
auto_mode = {
    'active': False,
    'messages': [],
    'timer_task': None,
    'control_message_id': None,
    'waiting_for_next': False
}

# Текущий вопрос от Claude (для /tg-ask)
pending_question = None


def read_active_session():
    """Читает session_id из файла. Возвращает None если нет активной сессии."""
    try:
        with open(SESSION_FILE, 'r') as f:
            content = f.read().strip()
            # Пропускаем строки с комментариями
            lines = [line for line in content.split('\n') if line and not line.startswith('#')]
            if lines:
                session_id = lines[0].strip()
                return session_id if session_id else None
            return None
    except FileNotFoundError:
        return None


def save_session_id(session_id: str):
    """Сохраняет session_id в файл."""
    with open(SESSION_FILE, 'w') as f:
        f.write(f"# Active Claude Code session ID\n")
        f.write(f"# Created: {datetime.now().isoformat()}\n")
        f.write(f"{session_id}\n")
    logger.info(f"Session ID сохранён: {session_id}")


def clear_session():
    """Очищает файл сессии."""
    with open(SESSION_FILE, 'w') as f:
        f.write("# Active Claude Code session ID\n")
        f.write("# When empty - no active session\n")
        f.write("#\n")
    logger.info("Session ID очищен")


async def cleanup_intermediate_messages():
    """
    Удаляет все промежуточные сообщения КРОМЕ последнего (финального) и индикатор прогресса ⌛.
    Вызывается перед началом новой задачи.
    """
    global intermediate_message_ids, current_hourglass_message_id

    try:
        # Если нет сообщений для очистки - выходим
        if not intermediate_message_ids and not current_hourglass_message_id:
            return

        # Удаляем все промежуточные сообщения КРОМЕ последнего
        # Последнее сообщение = финальный ответ Claude, оставляем его
        # Исключение: если сообщение только одно (например "Обрабатываю..." без ответа),
        # удаляем и его тоже
        if len(intermediate_message_ids) == 1:
            # Только одно сообщение - скорее всего "Обрабатываю..." без ответа
            messages_to_delete = intermediate_message_ids
        elif len(intermediate_message_ids) > 1:
            # Несколько сообщений - удаляем все кроме последнего
            messages_to_delete = intermediate_message_ids[:-1]
        else:
            # Нет сообщений
            messages_to_delete = []

        for message_id in messages_to_delete:
            try:
                await bot.delete_message(chat_id=ALLOWED_CHAT_ID, message_id=message_id)
                logger.debug(f"Удалено промежуточное сообщение: {message_id}")
            except Exception as e:
                logger.warning(f"Не удалось удалить промежуточное сообщение {message_id}: {e}")

        # Удаляем индикатор прогресса ⌛
        if current_hourglass_message_id:
            try:
                await bot.delete_message(chat_id=ALLOWED_CHAT_ID, message_id=current_hourglass_message_id)
                logger.debug(f"Удален индикатор прогресса: {current_hourglass_message_id}")
            except Exception as e:
                logger.warning(f"Не удалось удалить индикатор прогресса: {e}")

        # Очищаем списки
        intermediate_message_ids.clear()
        current_hourglass_message_id = None

        logger.info("✅ Промежуточные сообщения и прогресс-индикатор очищены")

    except Exception as e:
        logger.error(f"Ошибка при очистке промежуточных сообщений: {e}")


def update_activity():
    """Обновляет время последней активности и сбрасывает флаги уведомлений."""
    global last_activity_time, notification_30min_sent, notification_8h_sent
    last_activity_time = time.time()
    # Сбрасываем флаги уведомлений при любой активности
    notification_30min_sent = False
    notification_8h_sent = False


async def send_progress_indicator():
    """
    Отправляет кастомный эмодзи прогресс-индикатора из набора NewsEmoji.
    Custom emoji ID: 5386367538735104399

    Returns:
        Message ID отправленного индикатора
    """
    hourglass_msg = await bot.send_message(
        chat_id=ALLOWED_CHAT_ID,
        text="⏳",  # Фоллбэк для клиентов без поддержки custom emoji
        entities=[
            MessageEntity(
                type="custom_emoji",
                offset=0,
                length=1,
                custom_emoji_id="5386367538735104399"
            )
        ]
    )
    return hourglass_msg.message_id


def set_model(model: str):
    """Устанавливает модель Claude."""
    global current_model
    current_model = model
    logger.info(f"Модель изменена на: {model}")


async def stop_claude_process():
    """Останавливает активный процесс Claude (если есть)."""
    global active_claude_process, is_stopping

    if active_claude_process and active_claude_process.returncode is None:
        try:
            # Устанавливаем флаг остановки (защита от race condition)
            is_stopping = True

            pid = active_claude_process.pid
            logger.info(f"Останавливаем Claude процесс {pid}...")

            # Шаг 1: Пробуем graceful shutdown (SIGTERM)
            # Используем process group kill чтобы убить всё дерево процессов
            try:
                active_claude_process.terminate()
                await asyncio.wait_for(active_claude_process.wait(), timeout=2.0)
                logger.info(f"Процесс {pid} остановлен gracefully")
            except asyncio.TimeoutError:
                # Шаг 2: Если не помогло за 2 секунды - жёсткое убийство (SIGKILL)
                logger.warning(f"Процесс {pid} не ответил на SIGTERM, использую SIGKILL")
                active_claude_process.kill()
                await active_claude_process.wait()
                logger.info(f"Процесс {pid} убит через SIGKILL")

            # ⚠️ ВАЖНО: Очищаем переменную процесса
            active_claude_process = None
            # НЕ трогаем is_processing - он сбросится в finally блоке обработчика
            logger.info("Процесс остановлен, флаг is_stopping установлен")
            return True

        except Exception as e:
            logger.error(f"Ошибка остановки процесса: {e}")
            active_claude_process = None  # Очищаем даже при ошибке
            # НЕ трогаем is_processing
            return False

    # Процесса нет или он уже завершён
    return False


async def start_new_session(user_prompt: str, files: list[dict] = None):
    """Запускает новую сессию Claude Code."""
    global active_claude_process, is_processing, is_stopping
    import tempfile

    try:
        # Читаем контекст для TG-агента
        with open(CONTEXT_FILE, 'r') as f:
            context = f.read()

        # Формируем секцию с файлами если есть
        files_section = ""
        if files:
            files_section = "\n\n📎 **Файлы прикреплённые к сообщению:**\n\n"

            # Маппинг типов на эмодзи
            type_emoji = {
                'photo': '📸 Фото',
                'document': '📄 Документ',
                'video': '🎥 Видео',
                'audio': '🎵 Аудио',
                'voice': '🎤 Голосовое сообщение',
                'video_note': '⭕ Видео-заметка'
            }

            has_photos = False

            for file_info in files:
                file_type_label = type_emoji.get(file_info['type'], '📎 Файл')
                files_section += f"{file_type_label}: {file_info['name']}\n"
                files_section += f"Путь: {file_info['path']}\n"

                if file_info.get('size'):
                    size_mb = file_info['size'] / (1024 * 1024)
                    size_text = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{file_info['size'] / 1024:.2f} KB"
                    files_section += f"Размер: {size_text}\n"

                files_section += "\n"

                if file_info['type'] == 'photo':
                    has_photos = True

            if has_photos:
                files_section += "💡 Используй Read tool чтобы 'увидеть' изображение(я).\n\n"

        # Формируем полный промпт
        full_prompt = f"""{context}

---
[Новое сообщение от пользователя]
{files_section}
{user_prompt if user_prompt else "Проанализируй прикреплённые файлы"}
"""

        # Сохраняем промпт во временный файл в shared директории
        import time
        tmp_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"
        os.makedirs(tmp_dir, exist_ok=True)  # Создаём директорию если её нет
        tmp_file = f"{tmp_dir}/prompt_{int(time.time() * 1000)}.txt"
        with open(tmp_file, 'w') as f:
            f.write(full_prompt)
        os.chmod(tmp_file, 0o644)  # Читаемый для всех

        try:
            # Запускаем Claude Code в headless режиме
            cmd = f'export IS_SANDBOX=1 && cd {CLAUDE_WORKING_DIR} && cat {tmp_file} | {CLAUDE_CLI_PATH} --model {current_model} --dangerously-skip-permissions -p - --output-format json'

            active_claude_process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Сохраняем локальную ссылку (защита от race condition с stop_claude_process)
            local_process = active_claude_process
            stdout, stderr = await local_process.communicate()
        finally:
            # Удаляем временный файл
            os.remove(tmp_file)

        # Используем локальную ссылку (active_claude_process может быть None после stop_claude_process)
        if local_process.returncode != 0:
            error_msg = stderr.decode()
            logger.error(f"Claude failed: {error_msg}")
            active_claude_process = None  # Очищаем при ошибке

            # Проверяем: был ли процесс остановлен пользователем (/stop или /tg-ask)?
            if is_stopping:
                logger.info("Процесс был остановлен пользователем - пробуем сохранить session_id")
                # Попытаемся извлечь session_id из stdout даже при остановке
                try:
                    stdout_text = stdout.decode()
                    if stdout_text.strip():
                        data = json.loads(stdout_text)
                        session_id = data.get("session_id")
                        if session_id:
                            save_session_id(session_id)
                            logger.info(f"Session ID сохранён при остановке: {session_id}")
                except Exception as e:
                    logger.debug(f"Не удалось извлечь session_id при остановке: {e}")
                return

            raise Exception(f"Claude execution failed: {error_msg}")

        # Парсим JSON ответ
        data = json.loads(stdout.decode())
        session_id = data.get("session_id")

        if session_id:
            # Сохраняем session_id
            save_session_id(session_id)
            logger.info(f"Новая сессия создана: {session_id}")
        else:
            logger.warning("Session ID не найден в ответе Claude")

        # ⚠️ ВАЖНО: Очищаем переменную после естественного завершения
        # Session ID сохранён, можно будет продолжить новым сообщением
        active_claude_process = None

        update_activity()

    except Exception as e:
        logger.error(f"Ошибка при создании сессии: {e}")
        # Отправляем сообщение об ошибке только если НЕ была остановка пользователем
        if not is_stopping:
            await bot.send_message(
                ALLOWED_CHAT_ID,
                f"❌ <b>Ошибка запуска Claude</b>\n\n<code>{str(e)}</code>",
                parse_mode="HTML"
            )
    finally:
        # ВСЕГДА сбрасываем ОБА флага после завершения
        is_processing = False
        is_stopping = False
        logger.info("Флаги is_processing и is_stopping сброшены (start_new_session завершена)")

        # Удаляем прогресс-индикатор ⏳ после завершения задачи
        global current_hourglass_message_id
        if current_hourglass_message_id:
            try:
                await bot.delete_message(chat_id=ALLOWED_CHAT_ID, message_id=current_hourglass_message_id)
                logger.debug(f"Удален финальный ⏳ после завершения задачи: {current_hourglass_message_id}")
                current_hourglass_message_id = None
            except Exception as e:
                logger.warning(f"Не удалось удалить финальный ⏳: {e}")


async def resume_session(session_id: str, user_prompt: str, files: list[dict] = None):
    """Продолжает существующую сессию Claude Code."""
    global active_claude_process, is_processing, is_stopping
    import tempfile

    try:
        # Читаем контекст (напоминание)
        with open(CONTEXT_FILE, 'r') as f:
            context = f.read()

        # Формируем секцию с файлами если есть
        files_section = ""
        if files:
            files_section = "\n\n📎 **Файлы прикреплённые к сообщению:**\n\n"

            # Маппинг типов на эмодзи
            type_emoji = {
                'photo': '📸 Фото',
                'document': '📄 Документ',
                'video': '🎥 Видео',
                'audio': '🎵 Аудио',
                'voice': '🎤 Голосовое сообщение',
                'video_note': '⭕ Видео-заметка'
            }

            has_photos = False

            for file_info in files:
                file_type_label = type_emoji.get(file_info['type'], '📎 Файл')
                files_section += f"{file_type_label}: {file_info['name']}\n"
                files_section += f"Путь: {file_info['path']}\n"

                if file_info.get('size'):
                    size_mb = file_info['size'] / (1024 * 1024)
                    size_text = f"{size_mb:.2f} MB" if size_mb >= 1 else f"{file_info['size'] / 1024:.2f} KB"
                    files_section += f"Размер: {size_text}\n"

                files_section += "\n"

                if file_info['type'] == 'photo':
                    has_photos = True

            if has_photos:
                files_section += "💡 Используй Read tool чтобы 'увидеть' изображение(я).\n\n"

        # Формируем промпт с напоминанием о контексте
        prompt = f"""[НАПОМИНАНИЕ: Ты в Telegram Agent режиме]
{context}

---
[Новое сообщение от пользователя]
{files_section}
{user_prompt if user_prompt else "Проанализируй прикреплённые файлы"}
"""

        # Сохраняем промпт во временный файл в shared директории
        import time
        tmp_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"
        os.makedirs(tmp_dir, exist_ok=True)  # Создаём директорию если её нет
        tmp_file = f"{tmp_dir}/prompt_{int(time.time() * 1000)}.txt"
        with open(tmp_file, 'w') as f:
            f.write(prompt)
        os.chmod(tmp_file, 0o644)  # Читаемый для всех

        try:
            # Запускаем Claude с --resume
            cmd = f'export IS_SANDBOX=1 && cd {CLAUDE_WORKING_DIR} && cat {tmp_file} | {CLAUDE_CLI_PATH} --model {current_model} --dangerously-skip-permissions --resume {session_id} -p - --output-format json'

            active_claude_process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Сохраняем локальную ссылку (защита от race condition с stop_claude_process)
            local_process = active_claude_process
            stdout, stderr = await local_process.communicate()
        finally:
            # Удаляем временный файл
            os.remove(tmp_file)

        # Используем локальную ссылку (active_claude_process может быть None после stop_claude_process)
        if local_process.returncode != 0:
            error_msg = stderr.decode()
            logger.error(f"Claude resume failed: {error_msg}")
            active_claude_process = None  # Очищаем при ошибке

            # Проверяем: был ли процесс остановлен пользователем (/stop или /tg-ask)?
            if is_stopping:
                logger.info(f"Процесс был остановлен пользователем - сессия {session_id} сохранена")
                return

            # Сессия протухла естественным образом - создаём новую
            logger.info("Сессия протухла, создаю новую...")
            clear_session()
            await start_new_session(user_prompt, files)
            return

        logger.info(f"Сессия {session_id} продолжена успешно")

        # ⚠️ ВАЖНО: Очищаем переменную после естественного завершения
        # Session ID сохранён, можно будет продолжить новым сообщением
        active_claude_process = None

        update_activity()

    except Exception as e:
        logger.error(f"Ошибка при продолжении сессии: {e}")

        # Создаём новую сессию только если НЕ была остановка пользователем
        if not is_stopping:
            clear_session()
            await start_new_session(user_prompt, files)
    finally:
        # ВСЕГДА сбрасываем ОБА флага после завершения
        is_processing = False
        is_stopping = False
        logger.info("Флаги is_processing и is_stopping сброшены (resume_session завершена)")

        # Удаляем прогресс-индикатор ⏳ после завершения задачи
        global current_hourglass_message_id
        if current_hourglass_message_id:
            try:
                await bot.delete_message(chat_id=ALLOWED_CHAT_ID, message_id=current_hourglass_message_id)
                logger.debug(f"Удален финальный ⏳ после завершения задачи: {current_hourglass_message_id}")
                current_hourglass_message_id = None
            except Exception as e:
                logger.warning(f"Не удалось удалить финальный ⏳: {e}")


# === HELPER: Медиа-группы ===

async def process_media_group(media_group_id: str):
    """
    Обрабатывает накопленные сообщения из медиа-группы.
    Вызывается через таймер после получения последнего файла.
    """
    global media_groups_cache, is_processing, is_stopping, intermediate_message_ids, current_hourglass_message_id

    if media_group_id not in media_groups_cache:
        return

    # Проверяем блокировку (оба флага)
    if is_processing or is_stopping:
        logger.warning(f"Медиа-группа {media_group_id} отклонена (processing={is_processing}, stopping={is_stopping})")
        # Оставляем в кеше, попробуем позже
        return

    group_data = media_groups_cache.pop(media_group_id)
    messages = group_data['messages']

    if not messages:
        return

    # Удаляем промежуточные сообщения от предыдущей задачи
    await cleanup_intermediate_messages()

    # Очищаем списки промежуточных сообщений перед новой сессией
    intermediate_message_ids.clear()
    current_hourglass_message_id = None
    logger.debug("Списки промежуточных сообщений очищены перед новой сессией (медиа-группа)")

    # Устанавливаем флаг блокировки
    is_processing = True
    logger.info(f"Обработка медиа-группы {media_group_id}: {len(messages)} сообщений")

    # Берём первое сообщение как основное (оно содержит текст/caption)
    first_message = messages[0]

    # Собираем файлы из ВСЕХ сообщений группы
    all_files = []
    for msg in messages:
        files, voice_info = await save_message_files(msg)
        all_files.extend(files)
        # В медиа-группах голосовых быть не должно, но на всякий случай проверяем
        if voice_info:
            logger.warning("⚠️ Голосовое сообщение в медиа-группе - пропускаем")

    # Формируем текст сообщения
    user_text = first_message.text or first_message.caption or ""

    # Логирование
    text_preview = user_text[:100] if user_text else f"[медиа-группа: {len(all_files)} файл(ов)]"
    logger.info(f"Получена медиа-группа: {text_preview}")
    message_history.append({
        "timestamp": datetime.now().isoformat(),
        "from": "user",
        "text": user_text,
        "files": [f['name'] for f in all_files] if all_files else []
    })

    # Формируем статусное сообщение
    files_info = f"{len(all_files)} файл(ов)"
    has_photos = any(f['type'] == 'photo' for f in all_files)
    status_emoji = "📸" if has_photos else "📎"

    # Проверяем активную сессию
    session_id = read_active_session()

    if session_id:
        # Продолжить существующую сессию
        logger.info(f"Продолжаю сессию: {session_id}")
        status_msg = f"{status_emoji} Обрабатываю медиа-группу ({files_info})..."

        # Отправляем статусное сообщение и трекаем его
        sent_msg = await first_message.answer(status_msg)
        intermediate_message_ids.append(sent_msg.message_id)

        # Отправляем индикатор прогресса (custom emoji из NewsEmoji)
        current_hourglass_message_id = await send_progress_indicator()

        await resume_session(session_id, user_text, all_files)
    else:
        # Создать новую сессию
        logger.info("Создаю новую сессию Claude Code")
        status_msg = f"{status_emoji} Обрабатываю медиа-группу ({files_info})..."

        # Отправляем статусное сообщение и трекаем его
        sent_msg = await first_message.answer(status_msg)
        intermediate_message_ids.append(sent_msg.message_id)

        # Отправляем индикатор прогресса (custom emoji из NewsEmoji)
        current_hourglass_message_id = await send_progress_indicator()

        await start_new_session(user_text, all_files)


# === HELPER: Сохранение файлов из сообщения ===

async def save_message_files(message: Message) -> tuple[list[dict], dict | None]:
    """
    Сохраняет все файлы из сообщения (фото, документы, видео, аудио).
    Голосовые сообщения обрабатываются отдельно.

    Returns:
        tuple[list[dict], dict | None]:
            - Список обычных файлов (БЕЗ голосовых)
            - Информация о голосовом сообщении (или None)
    """
    from datetime import datetime

    files = []
    voice_info = None

    # Обработка фото
    if message.photo:
        try:
            photo = message.photo[-1]  # Лучшее качество
            file_id = photo.file_id

            file = await bot.get_file(file_id)
            file_path = file.file_path

            photos_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos"
            os.makedirs(photos_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'jpg'
            local_filename = f"photo_{timestamp}.{file_extension}"
            local_path = os.path.join(photos_dir, local_filename)

            await bot.download_file(file_path, local_path)

            files.append({
                'type': 'photo',
                'path': local_path,
                'name': local_filename,
                'size': photo.file_size if hasattr(photo, 'file_size') else 0,
                'caption': message.caption
            })

            logger.info(f"Фото сохранено: {local_path}")

        except Exception as e:
            logger.error(f"Ошибка сохранения фото: {e}")

    # Обработка документов
    if message.document:
        try:
            document = message.document
            file_id = document.file_id
            original_filename = document.file_name or "document"

            file = await bot.get_file(file_id)
            file_path = file.file_path

            files_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files"
            os.makedirs(files_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if '.' in original_filename:
                name_parts = original_filename.rsplit('.', 1)
                base_name = name_parts[0]
                extension = name_parts[1]
                local_filename = f"{base_name}_{timestamp}.{extension}"
            else:
                local_filename = f"{original_filename}_{timestamp}"

            local_path = os.path.join(files_dir, local_filename)

            await bot.download_file(file_path, local_path)

            files.append({
                'type': 'document',
                'path': local_path,
                'name': local_filename,
                'size': document.file_size,
                'caption': message.caption
            })

            logger.info(f"Документ сохранён: {local_path}")

        except Exception as e:
            logger.error(f"Ошибка сохранения документа: {e}")

    # Обработка видео
    if message.video:
        try:
            video = message.video
            file_id = video.file_id

            file = await bot.get_file(file_id)
            file_path = file.file_path

            files_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files"
            os.makedirs(files_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'mp4'
            local_filename = f"video_{timestamp}.{file_extension}"
            local_path = os.path.join(files_dir, local_filename)

            await bot.download_file(file_path, local_path)

            files.append({
                'type': 'video',
                'path': local_path,
                'name': local_filename,
                'size': video.file_size,
                'caption': message.caption
            })

            logger.info(f"Видео сохранено: {local_path}")

        except Exception as e:
            logger.error(f"Ошибка сохранения видео: {e}")

    # Обработка аудио
    if message.audio:
        try:
            audio = message.audio
            file_id = audio.file_id

            file = await bot.get_file(file_id)
            file_path = file.file_path

            files_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files"
            os.makedirs(files_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'mp3'
            original_name = audio.file_name or f"audio_{timestamp}"

            if '.' in original_name:
                name_parts = original_name.rsplit('.', 1)
                local_filename = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
            else:
                local_filename = f"{original_name}.{file_extension}"

            local_path = os.path.join(files_dir, local_filename)

            await bot.download_file(file_path, local_path)

            files.append({
                'type': 'audio',
                'path': local_path,
                'name': local_filename,
                'size': audio.file_size,
                'caption': message.caption
            })

            logger.info(f"Аудио сохранено: {local_path}")

        except Exception as e:
            logger.error(f"Ошибка сохранения аудио: {e}")

    # Обработка голосовых сообщений
    # НЕ добавляем в files - обрабатываем отдельно
    if message.voice:
        try:
            voice = message.voice
            file_id = voice.file_id

            file = await bot.get_file(file_id)
            file_path = file.file_path

            files_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files"
            os.makedirs(files_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'ogg'
            local_filename = f"voice_{timestamp}.{file_extension}"
            local_path = os.path.join(files_dir, local_filename)

            await bot.download_file(file_path, local_path)

            # Сохраняем информацию о голосовом для последующей обработки
            voice_info = {
                'path': local_path,
                'name': local_filename,
                'size': voice.file_size,
                'caption': message.caption
            }

            logger.info(f"Голосовое сообщение скачано: {local_path}")

        except Exception as e:
            logger.error(f"Ошибка сохранения голосового: {e}")

    # Обработка видео-заметок (кружочки)
    if message.video_note:
        try:
            video_note = message.video_note
            file_id = video_note.file_id

            file = await bot.get_file(file_id)
            file_path = file.file_path

            files_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files"
            os.makedirs(files_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'mp4'
            local_filename = f"video_note_{timestamp}.{file_extension}"
            local_path = os.path.join(files_dir, local_filename)

            await bot.download_file(file_path, local_path)

            files.append({
                'type': 'video_note',
                'path': local_path,
                'name': local_filename,
                'size': video_note.file_size,
                'caption': message.caption
            })

            logger.info(f"Видео-заметка сохранена: {local_path}")

        except Exception as e:
            logger.error(f"Ошибка сохранения видео-заметки: {e}")

    return files, voice_info


async def transcribe_audio(audio_file_path: str, language: str = "ru") -> str | None:
    """
    Транскрибирует аудио файл используя OpenAI gpt-4o-transcribe.

    Модель gpt-4o-transcribe - улучшенная модель транскрипции от OpenAI,
    предоставляющая лучшую точность чем Whisper (меньше Word Error Rate),
    особенно для речи с акцентами и в шумной среде.

    Стоимость: $0.006 за минуту аудио (gpt-4o-transcribe)
    Лимит: 25 MB файл, до 2000 токенов на выход

    Args:
        audio_file_path: Путь к аудио файлу (ogg, mp3, mp4, mpeg, mpga, m4a, wav, webm)
        language: Код языка (ru, en, etc.) - опционально, помогает точности

    Returns:
        Текст транскрипции или None в случае ошибки
    """
    import subprocess
    converted_file = None

    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY не найден в .env - транскрипция пропущена")
            return None

        client = OpenAI(api_key=api_key)

        # Конвертируем .oga в .mp3 если нужно (Telegram отправляет голосовые в .oga)
        file_to_transcribe = audio_file_path
        if audio_file_path.endswith('.oga') or audio_file_path.endswith('.ogg'):
            converted_file = audio_file_path.rsplit('.', 1)[0] + '.mp3'
            logger.info(f"Конвертация {audio_file_path} -> {converted_file}")

            # ffmpeg -i input.oga -codec:a libmp3lame -q:a 2 output.mp3
            result = subprocess.run(
                ['ffmpeg', '-i', audio_file_path, '-codec:a', 'libmp3lame', '-q:a', '2', converted_file, '-y'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logger.error(f"Ошибка конвертации аудио: {result.stderr}")
                return None

            file_to_transcribe = converted_file
            logger.info("Конвертация завершена")

        # Открываем аудио файл и отправляем на транскрипцию
        with open(file_to_transcribe, "rb") as audio_file:
            logger.info(f"Отправка аудио на транскрипцию (gpt-4o-transcribe): {file_to_transcribe}")

            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",  # Новая модель с лучшей точностью
                file=audio_file,
                response_format="text",
                language=language,
                temperature=0.0,
            )

            # API возвращает строку напрямую при response_format="text"
            transcription_text = transcription.strip() if transcription else ""

            logger.info(f"Транскрипция получена: {len(transcription_text)} символов")
            return transcription_text

    except ImportError:
        logger.error("Библиотека openai не установлена. Установите: pip install openai")
        return None
    except Exception as e:
        logger.error(f"Ошибка транскрипции аудио: {e}")
        return None
    finally:
        # Удаляем временный конвертированный файл
        if converted_file and os.path.exists(converted_file):
            try:
                os.remove(converted_file)
                logger.debug(f"Удалён временный файл: {converted_file}")
            except Exception as e:
                logger.warning(f"Не удалось удалить временный файл {converted_file}: {e}")


async def submit_accumulated_messages(chat_id: int, messages_list: list, bot):
    """
    Отправляет накопленные сообщения в Claude Code.
    Используется как для multi-mode, так и для auto-mode.

    Args:
        chat_id: ID чата пользователя
        messages_list: Список сообщений для отправки
        bot: Экземпляр бота для отправки статусных сообщений
    """
    global is_processing, is_stopping, intermediate_message_ids, current_hourglass_message_id

    if not messages_list:
        logger.warning("submit_accumulated_messages вызван с пустым списком")
        return

    # Проверяем блокировку
    if is_processing or is_stopping:
        await bot.send_message(
            chat_id=chat_id,
            text="⏳ <b>Подожди немного</b>\n\nЯ ещё обрабатываю предыдущее сообщение.",
            parse_mode="HTML"
        )
        return

    # Удаляем промежуточные сообщения от предыдущей задачи
    await cleanup_intermediate_messages()
    intermediate_message_ids.clear()
    current_hourglass_message_id = None

    # Устанавливаем флаг блокировки
    is_processing = True
    logger.info(f"Обработка {len(messages_list)} накопленных сообщений")

    # Обрабатываем все сообщения и собираем файлы + текст
    all_files = []
    all_texts = []

    for msg in messages_list:
        # Сохраняем файлы если есть
        files, voice_info = await save_message_files(msg)
        if files:
            all_files.extend(files)

        # Собираем текст
        text = msg.text or msg.caption or ""

        # Обработка голосового сообщения
        if voice_info:
            try:
                transcription = await transcribe_audio(voice_info['path'], language="ru")
                if transcription:
                    text += f"\n\n🎤 Голосовое сообщение: {transcription}"
                else:
                    await bot.send_message(
                        chat_id=chat_id,
                        text="❌ <b>Ошибка транскрипции голосового сообщения</b>",
                        parse_mode="HTML"
                    )
                    is_processing = False
                    return
            finally:
                # Удаляем файлы голосового
                import os
                try:
                    if os.path.exists(voice_info['path']):
                        os.remove(voice_info['path'])
                    mp3_path = voice_info['path'].rsplit('.', 1)[0] + '.mp3'
                    if os.path.exists(mp3_path):
                        os.remove(mp3_path)
                except Exception as e:
                    logger.warning(f"Не удалось удалить файлы голосового: {e}")

        if text:
            all_texts.append(text)

    # Объединяем все тексты
    combined_text = "\n\n---\n\n".join(all_texts) if all_texts else ""

    # Логирование
    logger.info(f"Объединённый текст: {len(combined_text)} символов, {len(all_files)} файл(ов)")
    message_history.append({
        "timestamp": datetime.now().isoformat(),
        "from": "user",
        "text": combined_text,
        "files": [f['name'] for f in all_files] if all_files else []
    })

    # Формируем статусное сообщение
    if all_files:
        files_info = f"{len(all_files)} файл(ов)"
        status_emoji = "📎"
    else:
        files_info = ""
        status_emoji = "💬"

    # Проверяем активную сессию
    session_id = read_active_session()

    if session_id:
        # Продолжить существующую сессию
        logger.info(f"Продолжаю сессию: {session_id}")
        status_msg = f"{status_emoji} Обрабатываю {len(messages_list)} сообщений (продолжение сессии)..."
        if files_info:
            status_msg += f"\n📎 {files_info}"

        sent_msg = await bot.send_message(chat_id=chat_id, text=status_msg)
        intermediate_message_ids.append(sent_msg.message_id)
        current_hourglass_message_id = await send_progress_indicator()

        await resume_session(session_id, combined_text, all_files)
    else:
        # Создать новую сессию
        logger.info("Создаю новую сессию Claude Code")
        status_msg = f"{status_emoji} Обрабатываю {len(messages_list)} сообщений (новая сессия)..."
        if files_info:
            status_msg += f"\n📎 {files_info}"

        sent_msg = await bot.send_message(chat_id=chat_id, text=status_msg)
        intermediate_message_ids.append(sent_msg.message_id)
        current_hourglass_message_id = await send_progress_indicator()

        await start_new_session(combined_text, all_files)


# === HANDLERS TELEGRAM ===

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    if message.chat.id != ALLOWED_CHAT_ID:
        logger.warning(f"Неавторизованный доступ от {message.chat.id}")
        await message.answer("⛔ Доступ запрещён")
        return

    await message.answer(
        "🤖 <b>AI Workspace Bot активен!</b>\n\n"
        "Я могу:\n"
        "• Принимать твои сообщения и передавать их Claude\n"
        "• Отправлять тебе уведомления, отчеты и файлы\n"
        "• Логировать всю историю общения\n\n"
        "Команды:\n"
        "/status - статус бота\n"
        "/help - помощь",
        parse_mode="HTML"
    )
    logger.info(f"Команда /start от пользователя {message.chat.id}")


@router.message(Command("status"))
async def cmd_status(message: Message):
    """Обработчик команды /status"""
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = read_active_session()

    # Эмодзи и название режима
    if current_model == "haiku":
        model_emoji, model_name = "⚡️", "Быстрый"
    elif current_model == "opus":
        model_emoji, model_name = "🧠", "Умный"
    else:  # sonnet
        model_emoji, model_name = "⚖️", "Оптимальный"

    session_info = f"📝 Сессия: <code>{session_id[:8]}...</code>" if session_id else "📝 Сессия: нет"

    await message.answer(
        f"✅ <b>Бот работает</b>\n\n"
        f"🕐 Время сервера: {uptime}\n"
        f"{model_emoji} Режим: <b>{model_name}</b> (<code>{current_model}</code>)\n"
        f"{session_info}\n"
        f"📨 Сообщений в истории: {len(message_history)}\n"
        f"🆔 Ваш chat_id: <code>{message.chat.id}</code>",
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    help_text = (
        "📖 <b>Справка по командам</b>\n\n"
        "<b>🚀 /start</b>\n"
        "Начать работу с ботом. Показывает приветственное сообщение.\n\n"

        "<b>💬 Обычное сообщение (Auto-mode)</b>\n"
        "Просто напиши мне любое сообщение - появится таймер на 5 секунд. "
        "Можешь добавить ещё сообщения или дождаться автоотправки. "
        "Claude выполнит задачу и отправит результат.\n\n"

        "<b>📝 /multi</b>\n"
        "Включает/выключает режим накопления сообщений. "
        "Когда активен - твои сообщения накапливаются без таймера. "
        "Нажми кнопку [начать сессию] когда готов отправить всё сразу.\n\n"

        "<b>📊 /status</b>\n"
        "Показывает текущий статус бота, активной сессии и выбранной модели.\n\n"

        "<b>⏸ /stop</b>\n"
        "Останавливает текущее выполнение Claude, но сохраняет session ID. "
        "Следующее сообщение продолжит работу в этой же сессии.\n\n"

        "<b>❌ /end</b>\n"
        "Полностью завершает сессию: останавливает процесс и удаляет session ID. "
        "Следующее сообщение создаст новую сессию с чистого листа.\n\n"

        "<b>🔄 /restart</b>\n"
        "Полностью перезагружает бота: останавливает все процессы, очищает сессии и перезапускает контейнер. "
        "Используй если возникли проблемы с сессиями или ботом.\n\n"

        "<b>⚡️ /fast</b>\n"
        "Переключает на быстрый режим (модель Haiku). Быстрее и дешевле, подходит для простых задач.\n\n"

        "<b>🧠 /smart</b>\n"
        "Переключает на умный режим (модель Sonnet). Медленнее, но лучше справляется со сложными задачами.\n\n"

        "<b>📖 /help</b>\n"
        "Показывает эту справку.\n\n"

        "💡 <b>Как работает:</b>\n"
        "• Каждое сообщение запускает или продолжает сессию с Claude Code\n"
        "• Claude выполняет задачу автономно и отправляет обновления\n"
        "• Используй /stop для паузы или /end для полного завершения\n"
        "• Выбирай модель в зависимости от сложности задачи"
    )

    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    """Обработчик команды /stop - останавливает выполнение без ожидания ответа"""
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    session_id = read_active_session()

    # Останавливаем процесс если работает
    stopped = await stop_claude_process()

    if stopped:
        if session_id:
            await message.answer(
                "⏸ <b>Выполнение остановлено</b>\n\n"
                "Session ID сохранён - следующее сообщение возобновит сессию.\n\n"
                "Для полного завершения используй кнопку <b>❌ Завершить сессию</b>",
                parse_mode="HTML"
            )
        else:
            await message.answer("⏸ <b>Процесс остановлен</b>", parse_mode="HTML")
    else:
        await message.answer("ℹ️ Нет активного процесса для остановки", parse_mode="HTML")

    logger.info("Процесс остановлен командой /stop")


@router.message(Command("end"))
async def cmd_end(message: Message):
    """Обработчик команды /end - завершает сессию полностью"""
    global pending_question

    if message.chat.id != ALLOWED_CHAT_ID:
        return

    session_id = read_active_session()

    # Останавливаем процесс если работает
    stopped = await stop_claude_process()

    # Очищаем session_id и pending_question
    clear_session()
    pending_question = None

    if session_id:
        msg = f"✅ <b>Сессия завершена</b>\n\n"
        if stopped:
            msg += "Процесс остановлен и session ID удалён.\n"
        else:
            msg += "Session ID удалён.\n"
        msg += "\nСледующее сообщение создаст новую сессию."
        await message.answer(msg, parse_mode="HTML")
    else:
        await message.answer("ℹ️ Нет активной сессии", parse_mode="HTML")

    logger.info("Сессия завершена командой /end")


@router.message(Command("restart"))
async def cmd_restart(message: Message):
    """Обработчик команды /restart - перезапускает контейнер бота"""
    global pending_question

    if message.chat.id != ALLOWED_CHAT_ID:
        return

    # Останавливаем активный процесс если есть
    await stop_claude_process()

    # Очищаем сессию и pending_question
    clear_session()
    pending_question = None

    # Отправляем сообщение перед перезапуском
    await message.answer(
        "🔄 <b>Перезагружаю бота...</b>\n\n"
        "Контейнер будет перезапущен через несколько секунд.\n"
        "Все сессии будут очищены.",
        parse_mode="HTML"
    )

    logger.info("Перезапуск бота по команде пользователя")

    # Сохраняем флаг что нужно отправить сообщение после перезапуска
    restart_flag_file = "/opt/ai-workspace/.claude/skills/telegram-notifier/restart_flag.txt"
    with open(restart_flag_file, 'w') as f:
        f.write("1")

    # Запускаем перезапуск контейнера в фоне
    import subprocess
    subprocess.Popen([
        "docker-compose",
        "-f", "/opt/ai-workspace/apps/telegram-bot/docker-compose.yml",
        "restart"
    ])


@router.message(Command("fast"))
async def cmd_fast(message: Message):
    """Обработчик команды /fast - переключает на быстрый режим (haiku)"""
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    set_model("haiku")
    await message.answer(
        "⚡️ <b>Режим: Быстрый</b>\n\n"
        "Модель: <code>haiku</code>\n"
        "• Быстрые ответы\n"
        "• Меньшая стоимость\n"
        "• Подходит для простых задач",
        parse_mode="HTML"
    )


@router.message(Command("optimal"))
async def cmd_optimal(message: Message):
    """Обработчик команды /optimal - переключает на оптимальный режим (sonnet)"""
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    set_model("sonnet")
    await message.answer(
        "⚖️ <b>Режим: Оптимальный</b>\n\n"
        "Модель: <code>sonnet</code>\n"
        "• Баланс скорости и качества\n"
        "• Хорошее качество кода\n"
        "• Подходит для большинства задач",
        parse_mode="HTML"
    )


@router.message(Command("smart"))
async def cmd_smart(message: Message):
    """Обработчик команды /smart - переключает на умный режим (opus)"""
    if message.chat.id != ALLOWED_CHAT_ID:
        return

    set_model("opus")
    await message.answer(
        "🧠 <b>Режим: Умный</b>\n\n"
        "Модель: <code>opus</code>\n"
        "• Максимальное качество\n"
        "• Глубокий анализ\n"
        "• Лучшее для сложных задач",
        parse_mode="HTML"
    )


@router.message(Command("multi"))
async def cmd_multi(message: Message):
    """Обработчик команды /multi - включает/выключает режим накопления сообщений"""
    global multi_mode_active, multi_messages, multi_control_message_ids

    if message.chat.id != ALLOWED_CHAT_ID:
        return

    # Переключаем режим
    multi_mode_active = not multi_mode_active

    if multi_mode_active:
        # Включаем режим
        await message.answer(
            "📝 <b>Режим накопления включён</b>\n\n"
            "Твои сообщения будут накапливаться.\n"
            "Под каждым появится кнопка <b>[начать сессию]</b>\n\n"
            "Нажми её когда будешь готов отправить всё Claude сразу.\n\n"
            "Чтобы выключить режим, отправь /multi ещё раз",
            parse_mode="HTML"
        )
        logger.info("Режим /multi включён")
    else:
        # Выключаем режим и очищаем накопленные сообщения
        num_messages = len(multi_messages)
        multi_messages.clear()

        # Удаляем все контрольные сообщения с кнопками
        for msg_id in multi_control_message_ids:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
            except Exception as e:
                logger.warning(f"Не удалось удалить контрольное сообщение {msg_id}: {e}")
        multi_control_message_ids.clear()

        await message.answer(
            f"✅ <b>Режим накопления выключен</b>\n\n"
            f"Накопленные сообщения ({num_messages}) сброшены.\n"
            f"Возвращаюсь к обычному режиму работы.",
            parse_mode="HTML"
        )
        logger.info(f"Режим /multi выключён, сброшено {num_messages} сообщений")


@router.message(F.text | F.photo | F.document | F.video | F.audio | F.voice | F.video_note)
async def handle_message(message: Message):
    """Универсальный обработчик сообщений (текст, фото, документы, видео, аудио, голосовые) - запускает Claude Code"""
    global is_processing, is_stopping, intermediate_message_ids, current_hourglass_message_id
    global multi_mode_active, multi_messages, multi_control_message_ids, auto_mode, pending_question

    if message.chat.id != ALLOWED_CHAT_ID:
        logger.warning(f"Неавторизованное сообщение от {message.chat.id}")
        await message.answer("⛔ Доступ запрещён")
        return

    # === РЕЖИМ 1: Ответ на вопрос от Claude (/tg-ask) ===
    if pending_question and message.text:
        logger.info(f"Получен ответ на вопрос Claude: {message.text[:50]}")

        # Сбрасываем pending_question
        pending_question = None

        # Отправляем ответ в Claude через resume_session
        session_id = read_active_session()
        if session_id:
            await message.answer("✅ Ответ принят, передаю Claude...", parse_mode="HTML")
            intermediate_message_ids.clear()
            current_hourglass_message_id = None
            is_processing = True

            sent_msg = await message.answer("⏳ Обрабатываю ответ...")
            intermediate_message_ids.append(sent_msg.message_id)
            current_hourglass_message_id = await send_progress_indicator()

            await resume_session(session_id, message.text, [])
        else:
            await message.answer("❌ Сессия потеряна, начинаю новую...", parse_mode="HTML")
            is_processing = True
            await start_new_session(message.text, [])

        return  # Выходим, не продолжаем обычную обработку

    # === РЕЖИМ 2: Multi-mode (явный режим накопления) ===
    if multi_mode_active:
        logger.info("Multi-mode: добавляю сообщение в очередь")

        # Добавляем сообщение в список
        multi_messages.append(message)

        # Создаём кнопки [начать сессию] [отменить]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="▶️ Начать сессию", callback_data="multi_start_session"),
                InlineKeyboardButton(text="❌ Отменить", callback_data="multi_cancel")
            ]
        ])

        text_preview = message.text[:50] if message.text else "[файл/фото]"
        control_msg = await message.answer(
            f"📝 <b>Сообщение #{len(multi_messages)} добавлено</b>\n\n"
            f"{text_preview}...\n\n"
            f"Всего накоплено: <b>{len(multi_messages)}</b> сообщений",
            parse_mode="HTML",
            reply_markup=keyboard
        )

        multi_control_message_ids.append(control_msg.message_id)
        return  # Выходим, не продолжаем обычную обработку

    # === РЕЖИМ 3: Auto-mode (режим по умолчанию с 5-сек таймером) ===
    # Если мы здесь, значит multi_mode НЕ активен, используем auto-mode

    logger.info("Auto-mode: запускаю таймер для сообщения")

    # Добавляем сообщение в auto_mode
    auto_mode['messages'].append(message)
    auto_mode['active'] = True

    # Отменяем предыдущий таймер если был
    if auto_mode['timer_task'] and not auto_mode['timer_task'].done():
        auto_mode['timer_task'].cancel()
        logger.debug("Отменён предыдущий auto-mode таймер")

    # Удаляем предыдущее контрольное сообщение
    if auto_mode['control_message_id']:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=auto_mode['control_message_id'])
        except Exception as e:
            logger.warning(f"Не удалось удалить предыдущее контрольное сообщение: {e}")

    # Определяем текст и кнопки в зависимости от состояния
    if auto_mode['waiting_for_next']:
        # Пользователь нажал [+ сообщение], ожидали следующее
        keyboard_text = "Ещё одно сообщение добавлено"
        auto_mode['waiting_for_next'] = False  # Сбрасываем флаг
    else:
        keyboard_text = "Запрос принят"

    # Кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить сообщение", callback_data="auto_add_message"),
            InlineKeyboardButton(text="🚫 Отменить запрос", callback_data="auto_cancel")
        ]
    ])

    text_preview = message.text[:80] if message.text else "[файл/фото]"
    control_msg = await message.answer(
        f"✅ <b>{keyboard_text}</b>\n\n"
        f"{text_preview}...\n\n"
        f"Через 5 секунд отправлю Claude, либо выбери действие:",
        parse_mode="HTML",
        reply_markup=keyboard
    )

    auto_mode['control_message_id'] = control_msg.message_id

    # Создаём таймер с анимацией обратного отсчёта (5→4→3→2→1)
    async def auto_submit_after_timeout():
        try:
            # Обратный отсчёт с обновлением каждую секунду
            for seconds_left in range(5, 0, -1):
                try:
                    await message.bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=control_msg.message_id,
                        text=(
                            f"✅ <b>{keyboard_text}</b>\n\n"
                            f"{text_preview}...\n\n"
                            f"Через {seconds_left} {'секунд' if seconds_left >= 5 else 'секунды' if seconds_left >= 2 else 'секунду'} отправлю Claude, либо выбери действие:"
                        ),
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                except Exception as e:
                    logger.debug(f"Не удалось обновить countdown: {e}")

                # Ждём 1 секунду перед следующим обновлением
                await asyncio.sleep(1.0)

            logger.info("Auto-mode: таймер истёк, отправляю накопленные сообщения")

            # Удаляем контрольное сообщение
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=auto_mode['control_message_id'])
            except:
                pass

            # Отправляем накопленные сообщения
            messages_to_send = auto_mode['messages'].copy()
            auto_mode['messages'].clear()
            auto_mode['active'] = False
            auto_mode['control_message_id'] = None
            auto_mode['waiting_for_next'] = False

            await submit_accumulated_messages(message.chat.id, messages_to_send, message.bot)
        except asyncio.CancelledError:
            logger.debug("Auto-mode таймер отменён")

    auto_mode['timer_task'] = asyncio.create_task(auto_submit_after_timeout())

    return  # Выходим, сообщение будет обработано позже через таймер или кнопку

    # === ОБЫЧНЫЙ РЕЖИМ (КОД НИЖЕ УЖЕ НЕ ДОЛЖЕН ВЫПОЛНЯТЬСЯ) ===
    # Весь код ниже достигаться не будет, т.к. всегда сработает один из режимов выше

    # Проверяем: идёт ли уже обработка другого сообщения ИЛИ процесс остановки?
    if is_processing or is_stopping:
        text_preview = message.text[:100] if message.text else "[файл/фото]"
        logger.warning(f"Отклонено сообщение (processing={is_processing}, stopping={is_stopping}): {text_preview}")
        await message.answer(
            "⏳ <b>Подожди немного</b>\n\n"
            "Я ещё обрабатываю предыдущее сообщение.\n"
            "Напиши снова когда получишь ответ.",
            parse_mode="HTML"
        )
        return

    # Проверяем: это медиа-группа (альбом)?
    if message.media_group_id:
        media_group_id = message.media_group_id

        # Если это первое сообщение из группы - создаём запись
        if media_group_id not in media_groups_cache:
            media_groups_cache[media_group_id] = {
                'messages': [],
                'timer': None
            }

        # Добавляем сообщение в группу
        media_groups_cache[media_group_id]['messages'].append(message)

        # Отменяем предыдущий таймер если был
        if media_groups_cache[media_group_id]['timer']:
            media_groups_cache[media_group_id]['timer'].cancel()

        # Создаём новый таймер (0.5 секунды после последнего файла)
        # Когда все файлы придут, таймер сработает и обработает всю группу
        async def delayed_process():
            await asyncio.sleep(0.5)
            await process_media_group(media_group_id)

        media_groups_cache[media_group_id]['timer'] = asyncio.create_task(delayed_process())

        logger.info(f"Добавлено сообщение в медиа-группу {media_group_id} ({len(media_groups_cache[media_group_id]['messages'])} файлов)")
        return  # НЕ обрабатываем сейчас, дождёмся всех файлов

    # Удаляем промежуточные сообщения от предыдущей задачи
    await cleanup_intermediate_messages()

    # Очищаем списки промежуточных сообщений перед новой сессией
    intermediate_message_ids.clear()
    current_hourglass_message_id = None
    logger.debug("Списки промежуточных сообщений очищены перед новой сессией")

    # Устанавливаем флаг блокировки (только для одиночных сообщений)
    is_processing = True
    logger.info("Флаг is_processing установлен (начало обработки)")

    # Сохраняем файлы если есть
    files, voice_info = await save_message_files(message)

    # Формируем текст сообщения
    user_text = message.text or message.caption or ""

    # Обработка голосового сообщения (если есть)
    if voice_info:
        logger.info("🎤 Обнаружено голосовое сообщение, начинаю транскрипцию...")

        try:
            # Транскрибируем голосовое сообщение
            transcription = await transcribe_audio(voice_info['path'], language="ru")

            if transcription:
                # Успешно - добавляем транскрипцию к тексту сообщения
                voice_text = f"\n\n🎤 <b>Голосовое сообщение:</b>\n{transcription}"
                user_text = user_text + voice_text if user_text else voice_text.strip()
                logger.info(f"✅ Транскрипция успешна: {len(transcription)} символов")
            else:
                # Транскрипция не удалась - показываем ошибку
                error_msg = (
                    "❌ <b>Ошибка транскрипции голосового сообщения</b>\n\n"
                    "Не удалось расшифровать голосовое сообщение. "
                    "Возможные причины:\n"
                    "• Не настроен OPENAI_API_KEY\n"
                    "• Проблемы с API OpenAI\n"
                    "• Неподдерживаемый формат аудио"
                )
                await message.answer(error_msg, parse_mode="HTML")
                logger.error("Транскрипция не удалась - останавливаем обработку")
                is_processing = False
                return

        finally:
            # ВСЕГДА удаляем файлы голосового (.oga и .mp3 если создан)
            import os
            try:
                if os.path.exists(voice_info['path']):
                    os.remove(voice_info['path'])
                    logger.debug(f"Удалён .oga файл: {voice_info['path']}")

                # Удаляем .mp3 если был создан при конвертации
                mp3_path = voice_info['path'].rsplit('.', 1)[0] + '.mp3'
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                    logger.debug(f"Удалён .mp3 файл: {mp3_path}")
            except Exception as e:
                logger.warning(f"Не удалось удалить файлы голосового: {e}")

    # Логирование
    text_preview = user_text[:100] if user_text else f"[{len(files)} файл(ов)]"
    logger.info(f"Получено сообщение: {text_preview}")
    message_history.append({
        "timestamp": datetime.now().isoformat(),
        "from": "user",
        "text": user_text,
        "files": [f['name'] for f in files] if files else []
    })

    # Формируем статусное сообщение
    if files:
        files_info = ", ".join([f"{f['type']}: {f['name']}" for f in files])
        status_emoji = "📸" if files[0]['type'] == 'photo' else "📎"
    else:
        files_info = ""
        status_emoji = "💬"

    # Проверяем активную сессию
    session_id = read_active_session()

    if session_id:
        # Продолжить существующую сессию
        logger.info(f"Продолжаю сессию: {session_id}")
        status_msg = f"{status_emoji} Обрабатываю (продолжение сессии)..."
        if files_info:
            status_msg += f"\n📎 {files_info}"

        # Отправляем статусное сообщение и трекаем его
        sent_msg = await message.answer(status_msg)
        intermediate_message_ids.append(sent_msg.message_id)

        # Отправляем индикатор прогресса (custom emoji из NewsEmoji)
        current_hourglass_message_id = await send_progress_indicator()

        await resume_session(session_id, user_text, files)
    else:
        # Создать новую сессию
        logger.info("Создаю новую сессию Claude Code")
        status_msg = f"{status_emoji} Обрабатываю (новая сессия)..."
        if files_info:
            status_msg += f"\n📎 {files_info}"

        # Отправляем статусное сообщение и трекаем его
        sent_msg = await message.answer(status_msg)
        intermediate_message_ids.append(sent_msg.message_id)

        # Отправляем индикатор прогресса (custom emoji из NewsEmoji)
        current_hourglass_message_id = await send_progress_indicator()

        await start_new_session(user_text, files)

    # Claude САМ отправит ответ через /tg команды


@router.callback_query(F.data == "end_session")
async def handle_end_session(callback: CallbackQuery):
    """Обработчик кнопки 'Завершить сессию' - останавливает процесс и удаляет session_id"""
    # Останавливаем процесс если работает
    stopped = await stop_claude_process()

    # Очищаем session_id
    clear_session()

    msg = "✅ Сессия завершена"
    if stopped:
        msg += " (процесс остановлен)"

    await callback.answer(msg)

    # Убираем кнопки из сообщения
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass  # Игнорируем если не удалось убрать кнопки

    logger.info("Сессия завершена пользователем")


@router.callback_query(F.data == "stop_execution")
async def handle_stop_execution(callback: CallbackQuery):
    """Обработчик кнопки 'Остановить выполнение' - останавливает процесс, но сохраняет session_id"""
    # Останавливаем процесс если работает
    stopped = await stop_claude_process()

    # НЕ очищаем session_id - следующее сообщение возобновит сессию

    msg = "⏸ Выполнение остановлено"
    if stopped:
        msg += "\nСледующее сообщение возобновит сессию"
    else:
        msg += "\nПроцесс уже завершён"

    await callback.answer(msg, show_alert=True)

    # Убираем кнопки из сообщения
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass  # Игнорируем если не удалось убрать кнопки

    logger.info("Выполнение остановлено пользователем (session_id сохранён)")


@router.callback_query(F.data == "continue_session")
async def handle_continue_session(callback: CallbackQuery):
    """Обработчик кнопки 'Продолжить работу' (при неактивности)"""
    update_activity()
    await callback.answer("✅ Таймер сброшен")

    # Удаляем сообщение с предложением
    try:
        await callback.message.delete()
    except Exception:
        pass

    logger.info("Сессия продолжена пользователем")


@router.callback_query(F.data == "auto_add_message")
async def handle_auto_add_message(callback: CallbackQuery):
    """Обработчик кнопки '+ Добавить сообщение' в auto-mode"""
    global auto_mode

    # Отменяем таймер
    if auto_mode['timer_task'] and not auto_mode['timer_task'].done():
        auto_mode['timer_task'].cancel()
        logger.info("Auto-mode: таймер отменён, ожидаю следующее сообщение")

    # Устанавливаем флаг ожидания
    auto_mode['waiting_for_next'] = True

    # Удаляем текущее контрольное сообщение
    try:
        await callback.message.delete()
    except Exception as e:
        logger.warning(f"Не удалось удалить контрольное сообщение: {e}")

    auto_mode['control_message_id'] = None

    # Отправляем подтверждение
    await callback.answer("✅ Жду следующее сообщение")

    # Отправляем новое сообщение
    await callback.message.answer(
        "📝 <b>Отправь следующее сообщение</b>\n\n"
        "После отправки снова появится таймер на 5 секунд.",
        parse_mode="HTML"
    )


@router.callback_query(F.data == "auto_cancel")
async def handle_auto_cancel(callback: CallbackQuery):
    """Обработчик кнопки 'Отменить запрос' в auto-mode"""
    global auto_mode

    # Отменяем таймер
    if auto_mode['timer_task'] and not auto_mode['timer_task'].done():
        auto_mode['timer_task'].cancel()

    num_messages = len(auto_mode['messages'])

    # Очищаем auto_mode
    auto_mode['messages'].clear()
    auto_mode['active'] = False
    auto_mode['control_message_id'] = None
    auto_mode['waiting_for_next'] = False
    auto_mode['timer_task'] = None

    # Удаляем контрольное сообщение
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.answer(f"❌ Запрос отменён ({num_messages} сообщений сброшено)")
    logger.info(f"Auto-mode: запрос отменён, сброшено {num_messages} сообщений")


@router.callback_query(F.data == "multi_start_session")
async def handle_multi_start_session(callback: CallbackQuery):
    """Обработчик кнопки 'Начать сессию' в multi-mode"""
    global multi_messages, multi_control_message_ids

    if not multi_messages:
        await callback.answer("❌ Нет накопленных сообщений")
        return

    num_messages = len(multi_messages)
    messages_to_send = multi_messages.copy()

    # Очищаем multi_mode
    multi_messages.clear()

    # Удаляем все контрольные сообщения
    for msg_id in multi_control_message_ids:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_id)
        except Exception:
            pass
    multi_control_message_ids.clear()

    await callback.answer(f"▶️ Отправляю {num_messages} сообщений в Claude...")
    logger.info(f"Multi-mode: начинаю сессию с {num_messages} сообщениями")

    # Отправляем накопленные сообщения
    await submit_accumulated_messages(callback.message.chat.id, messages_to_send, callback.bot)


@router.callback_query(F.data == "multi_cancel")
async def handle_multi_cancel(callback: CallbackQuery):
    """Обработчик кнопки 'Отменить' в multi-mode"""
    global multi_messages, multi_control_message_ids

    num_messages = len(multi_messages)

    # Очищаем multi_mode
    multi_messages.clear()

    # Удаляем все контрольные сообщения
    for msg_id in multi_control_message_ids:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_id)
        except Exception:
            pass
    multi_control_message_ids.clear()

    await callback.answer(f"❌ Отменено ({num_messages} сообщений сброшено)")
    logger.info(f"Multi-mode: отменено, сброшено {num_messages} сообщений")


@router.callback_query(F.data.startswith("answer_"))
async def handle_question_answer(callback: CallbackQuery):
    """Обработчик ответов на вопросы Claude (/tg-ask)"""
    global pending_question, is_processing

    if not pending_question:
        await callback.answer("❌ Нет активного вопроса")
        return

    # Извлекаем индекс ответа
    try:
        answer_index = int(callback.data.split("_")[1])
        answer_text = pending_question['options'][answer_index]
    except (IndexError, ValueError) as e:
        logger.error(f"Ошибка извлечения ответа: {e}")
        await callback.answer("❌ Ошибка обработки ответа")
        return

    logger.info(f"Получен ответ на вопрос Claude: {answer_text}")

    # Удаляем сообщение с вопросом
    try:
        await callback.message.delete()
    except Exception:
        pass

    # Сбрасываем pending_question
    pending_question = None

    # Отправляем ответ в Claude через resume_session
    session_id = read_active_session()
    if session_id:
        await callback.answer("✅ Ответ отправлен Claude")

        # Показываем пользователю что было выбрано
        await callback.message.answer(f"✅ Ты выбрал: <b>{answer_text}</b>", parse_mode="HTML")

        intermediate_message_ids.clear()
        current_hourglass_message_id = None
        is_processing = True

        sent_msg = await callback.message.answer("⏳ Обрабатываю ответ...")
        intermediate_message_ids.append(sent_msg.message_id)
        current_hourglass_message_id = await send_progress_indicator()

        await resume_session(session_id, answer_text, [])
    else:
        await callback.answer("❌ Сессия потеряна")
        await callback.message.answer("❌ Сессия потеряна, начинаю новую...", parse_mode="HTML")
        is_processing = True
        await start_new_session(answer_text, [])


# Старые обработчики handle_photo и handle_document удалены
# Теперь используется универсальный handle_message который обрабатывает текст, фото и документы


# === HTTP API ДЛЯ CLAUDE ===

async def send_message_handler(request):
    """
    POST /send
    Body: {"text": "message", "parse_mode": "HTML"}

    Поддерживает специальную команду /tg-ask для вопросов с кнопками:
    {"text": "/tg-ask {\"question\": \"Вопрос?\", \"options\": [\"Вариант 1\", \"Вариант 2\"]}"}
    """
    global pending_question

    try:
        data = await request.json()
        text = data.get("text")
        parse_mode = data.get("parse_mode", "HTML")

        if not text:
            return web.json_response({"error": "text is required"}, status=400)

        # === ОБРАБОТКА /tg-ask (вопросы с кнопками) ===
        if text.strip().startswith("/tg-ask "):
            import json

            try:
                # Извлекаем JSON после "/tg-ask "
                json_str = text.strip()[8:].strip()  # Убираем "/tg-ask " в начале
                question_data = json.loads(json_str)

                question_text = question_data.get("question")
                options = question_data.get("options", [])

                if not question_text:
                    return web.json_response({"error": "question is required in /tg-ask"}, status=400)

                if not isinstance(options, list) or len(options) < 1:
                    return web.json_response({"error": "options must be a non-empty array"}, status=400)

                # Создаём кнопки для каждого варианта (максимум 8, по 2 в ряд)
                buttons = []
                for i, option in enumerate(options[:8]):  # Ограничиваем 8 кнопками
                    button = InlineKeyboardButton(
                        text=str(option),
                        callback_data=f"answer_{i}"  # Идентификатор ответа
                    )

                    # Группируем по 2 кнопки в ряд
                    if i % 2 == 0:
                        buttons.append([button])
                    else:
                        buttons[-1].append(button)

                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

                # Сохраняем вопрос в pending_question
                pending_question = {
                    'question': question_text,
                    'options': options
                }

                # Отправляем вопрос с кнопками
                sent_message = await bot.send_message(
                    chat_id=ALLOWED_CHAT_ID,
                    text=f"❓ <b>{question_text}</b>\n\n"
                         f"Выбери вариант или напиши свой ответ:",
                    parse_mode="HTML",
                    reply_markup=keyboard
                )

                logger.info(f"/tg-ask: отправлен вопрос с {len(options)} вариантами")

                # Останавливаем процесс Claude (как при "Остановить выполнение")
                # НЕ очищаем session_id - следующее сообщение возобновит сессию
                await stop_claude_process()
                logger.info("/tg-ask: процесс Claude остановлен, ожидаем ответ пользователя")

                return web.json_response({"success": True, "type": "question"})

            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON в /tg-ask: {e}")
                return web.json_response({"error": f"Invalid JSON in /tg-ask: {str(e)}"}, status=400)
            except Exception as e:
                logger.error(f"Ошибка обработки /tg-ask: {e}")
                return web.json_response({"error": f"/tg-ask error: {str(e)}"}, status=500)

        # === ОБЫЧНОЕ СООБЩЕНИЕ ===

        # Проверяем есть ли активная сессия
        session_id = read_active_session()

        # Создаём кнопки управления если сессия активна
        keyboard = None
        if session_id:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⏸ Остановить выполнение",
                        callback_data="stop_execution"
                    ),
                    InlineKeyboardButton(
                        text="❌ Завершить сессию",
                        callback_data="end_session"
                    )
                ]
            ])

        # Отправляем основное сообщение и сохраняем его ID
        sent_message = await bot.send_message(
            chat_id=ALLOWED_CHAT_ID,
            text=text,
            parse_mode=parse_mode,
            reply_markup=keyboard
        )

        logger.info(f"Отправлено сообщение через API: {text[:100]}")
        message_history.append({
            "timestamp": datetime.now().isoformat(),
            "from": "bot",
            "text": text
        })

        # Управление прогресс-индикатором
        global current_hourglass_message_id

        # НЕ добавляем финальные сообщения в intermediate_message_ids!
        # Они должны оставаться в чате, только промежуточные "/update" и статусы удаляются

        # Удаляем предыдущий индикатор прогресса ⌛ если есть
        if current_hourglass_message_id:
            try:
                await bot.delete_message(chat_id=ALLOWED_CHAT_ID, message_id=current_hourglass_message_id)
                logger.debug(f"Удален предыдущий ⌛: {current_hourglass_message_id}")
            except Exception as e:
                logger.warning(f"Не удалось удалить предыдущий ⌛: {e}")

        # Отправляем новый индикатор прогресса (custom emoji из NewsEmoji)
        current_hourglass_message_id = await send_progress_indicator()
        logger.debug(f"Отправлен новый прогресс-индикатор: {current_hourglass_message_id}")

        update_activity()  # Обновляем время активности

        return web.json_response({"success": True})

    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def send_file_handler(request):
    """
    POST /send_file
    Multipart form: file=<binary>, caption=<text>
    """
    try:
        reader = await request.multipart()

        file_data = None
        file_name = None
        caption = None

        async for field in reader:
            if field.name == 'file':
                file_name = field.filename
                file_data = await field.read()
            elif field.name == 'caption':
                caption = await field.text()

        if not file_data:
            return web.json_response({"error": "file is required"}, status=400)

        # Сохраняем временно
        tmp_dir = "/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"
        temp_path = f"{tmp_dir}/{file_name}"
        with open(temp_path, "wb") as f:
            f.write(file_data)
        os.chmod(temp_path, 0o644)  # Читаемый для всех

        # Отправляем
        await bot.send_document(
            chat_id=ALLOWED_CHAT_ID,
            document=FSInputFile(temp_path),
            caption=caption,
            parse_mode="HTML"
        )

        # Удаляем временный файл
        os.remove(temp_path)

        logger.info(f"Отправлен файл через API: {file_name}")
        return web.json_response({"success": True, "file": file_name})

    except Exception as e:
        logger.error(f"Ошибка отправки файла: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def health_handler(request):
    """GET /health - проверка здоровья бота"""
    return web.json_response({
        "status": "ok",
        "uptime": datetime.now().isoformat(),
        "messages_count": len(message_history)
    })


# === ЗАПУСК ===

async def check_inactivity_loop():
    """
    Background task - проверяет неактивность сессии.
    Отправляет два уведомления: через 30 минут и через 8 часов.
    """
    INTERVAL_30MIN = 30 * 60  # 30 минут в секундах
    INTERVAL_8H = 8 * 60 * 60  # 8 часов в секундах
    CHECK_INTERVAL = 5 * 60  # Проверяем каждые 5 минут

    global notification_30min_sent, notification_8h_sent

    while True:
        await asyncio.sleep(CHECK_INTERVAL)

        session_id = read_active_session()

        if session_id:
            inactive_time = time.time() - last_activity_time

            # Уведомление через 30 минут (только если ещё не отправляли)
            if inactive_time >= INTERVAL_30MIN and not notification_30min_sent:
                logger.info(f"Сессия неактивна {int(inactive_time/60)} минут - отправляю первое уведомление")

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="✅ Продолжить работу",
                        callback_data="continue_session"
                    )],
                    [InlineKeyboardButton(
                        text="❌ Завершить сессию",
                        callback_data="end_session"
                    )]
                ])

                try:
                    await bot.send_message(
                        ALLOWED_CHAT_ID,
                        f"⏰ <b>Сессия неактивна 30 минут</b>\n\n"
                        f"Хочешь завершить сессию или продолжить работу?",
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                    notification_30min_sent = True
                    logger.info("✅ Первое уведомление (30 мин) отправлено")
                except Exception as e:
                    logger.error(f"Ошибка отправки уведомления о неактивности (30 мин): {e}")

            # Уведомление через 8 часов (только если ещё не отправляли)
            if inactive_time >= INTERVAL_8H and not notification_8h_sent:
                logger.info(f"Сессия неактивна {int(inactive_time/3600)} часов - отправляю второе уведомление")

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="✅ Продолжить работу",
                        callback_data="continue_session"
                    )],
                    [InlineKeyboardButton(
                        text="❌ Завершить сессию",
                        callback_data="end_session"
                    )]
                ])

                try:
                    await bot.send_message(
                        ALLOWED_CHAT_ID,
                        f"⏰ <b>Сессия неактивна 8 часов</b>\n\n"
                        f"Хочешь завершить сессию или продолжить работу?",
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                    notification_8h_sent = True
                    logger.info("✅ Второе уведомление (8 часов) отправлено")
                except Exception as e:
                    logger.error(f"Ошибка отправки уведомления о неактивности (8 часов): {e}")


async def start_http_server():
    """Запуск HTTP сервера для API"""
    app = web.Application()
    app.router.add_post('/send', send_message_handler)
    app.router.add_post('/send_file', send_file_handler)
    app.router.add_get('/health', health_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', HTTP_PORT)
    await site.start()

    logger.info(f"HTTP API запущен на порту {HTTP_PORT}")


async def set_bot_commands():
    """Устанавливает меню команд в Telegram"""
    commands = [
        BotCommand(command="start", description="🚀 Начать работу"),
        BotCommand(command="status", description="📊 Статус бота и сессии"),
        BotCommand(command="help", description="📖 Справка по командам"),
        BotCommand(command="stop", description="⏸ Остановить выполнение"),
        BotCommand(command="end", description="❌ Завершить сессию"),
        BotCommand(command="restart", description="🔄 Перезапустить бота"),
        BotCommand(command="fast", description="⚡️ Быстрый (Haiku)"),
        BotCommand(command="optimal", description="⚖️ Оптимальный (Sonnet)"),
        BotCommand(command="smart", description="🧠 Умный (Opus)"),
        BotCommand(command="multi", description="📝 Режим накопления сообщений"),
    ]
    await bot.set_my_commands(commands)
    logger.info("✅ Меню команд установлено")


async def check_restart_flag():
    """Проверяет флаг перезапуска и отправляет сообщение если нужно"""
    restart_flag_file = "/opt/ai-workspace/.claude/skills/telegram-notifier/restart_flag.txt"

    if os.path.exists(restart_flag_file):
        try:
            # Удаляем флаг
            os.remove(restart_flag_file)

            # Даём боту немного времени на полную инициализацию
            await asyncio.sleep(1)

            # Отправляем сообщение о готовности
            await bot.send_message(
                ALLOWED_CHAT_ID,
                "✅ <b>Бот перезапущен и готов к работе!</b>\n\n"
                "Все сессии очищены, можешь начинать работу.",
                parse_mode="HTML"
            )
            logger.info("Отправлено сообщение о завершении перезапуска")
        except Exception as e:
            logger.error(f"Ошибка при обработке флага перезапуска: {e}")


async def main():
    """Главная функция"""
    logger.info("🚀 Запуск Telegram бота...")
    logger.info(f"Разрешённый chat_id: {ALLOWED_CHAT_ID}")

    # Устанавливаем меню команд
    await set_bot_commands()

    # Запускаем HTTP API
    await start_http_server()

    # Запускаем background task для проверки неактивности
    asyncio.create_task(check_inactivity_loop())
    logger.info("✅ Background task неактивности запущен")

    # Проверяем флаг перезапуска
    asyncio.create_task(check_restart_flag())

    # Регистрируем роутер
    dp.include_router(router)

    # Запускаем polling
    logger.info("✅ Бот готов к работе")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен")
