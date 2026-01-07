#!/bin/bash
#
# tg-ask.sh - Отправка вопроса с кнопками-вариантами ответа в Telegram
#
# Назначение:
#   Отправляет пользователю вопрос с несколькими вариантами ответа (до 8 кнопок).
#   После отправки ЗАВЕРШАЕТ процесс Claude (как /tg).
#   Ответ пользователя придёт в новой сессии через --resume.
#
# Использование:
#   /tg-ask '{"question": "Текст вопроса?", "options": ["Вариант 1", "Вариант 2"]}'
#   /tg-ask '{"question": "Какой период?", "options": ["Месяц", "Квартал", "Год"]}'
#
# Формат JSON:
#   {
#     "question": "Текст вопроса для пользователя",
#     "options": ["Вариант 1", "Вариант 2", "Вариант 3"]
#   }
#
# Ограничения:
#   - Максимум 8 вариантов ответа
#   - Пользователь может либо нажать кнопку, либо написать свой ответ
#   - Процесс ЗАВЕРШАЕТСЯ после отправки (как /tg)
#

set -euo pipefail

# Конфигурация
BOT_API="http://localhost:8081"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Функция вывода ошибки
error() {
    echo -e "${RED}❌ Ошибка: $1${NC}" >&2
    exit 1
}

# Функция вывода успеха
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Проверка, что бот запущен
check_bot_running() {
    if ! curl -s -f "$BOT_API/health" > /dev/null 2>&1; then
        error "Telegram бот не запущен или недоступен!"
    fi
}

# Проверка зависимостей
if ! command -v curl &> /dev/null; then
    error "curl не установлен"
fi

if ! command -v jq &> /dev/null; then
    error "jq не установлен"
fi

# Проверка аргументов
if [[ $# -eq 0 ]]; then
    error "Использование: /tg-ask '{\"question\": \"...\", \"options\": [\"...\", \"...\"]}'"
fi

# Получаем JSON из аргументов
JSON_INPUT="$1"

# Валидация JSON
if ! echo "$JSON_INPUT" | jq . > /dev/null 2>&1; then
    error "Невалидный JSON: $JSON_INPUT"
fi

# Извлекаем question и options
QUESTION=$(echo "$JSON_INPUT" | jq -r '.question // empty')
OPTIONS=$(echo "$JSON_INPUT" | jq -c '.options // []')

if [[ -z "$QUESTION" ]]; then
    error "Не указан 'question' в JSON"
fi

if [[ "$OPTIONS" == "[]" ]]; then
    error "Не указаны 'options' в JSON или массив пустой"
fi

# Проверка количества вариантов
OPTIONS_COUNT=$(echo "$OPTIONS" | jq 'length')
if [[ $OPTIONS_COUNT -gt 8 ]]; then
    error "Слишком много вариантов ответа (максимум 8, указано $OPTIONS_COUNT)"
fi

# Проверка, что бот работает
check_bot_running

# Формируем /tg-ask команду в правильном формате
# Бот ожидает: {"text": "/tg-ask {...}", "parse_mode": "HTML"}
TG_ASK_PAYLOAD=$(jq -n \
    --arg question "$QUESTION" \
    --argjson options "$OPTIONS" \
    '{question: $question, options: $options}' | jq -c .)

FULL_TEXT="/tg-ask $TG_ASK_PAYLOAD"

# Отправка через /send endpoint
response=$(curl -s -X POST "$BOT_API/send" \
    -H "Content-Type: application/json" \
    -d "{\"text\": $(echo "$FULL_TEXT" | jq -Rs .), \"parse_mode\": \"HTML\"}")

# Проверка результата
if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
    success "Вопрос отправлен. Ожидаем ответ пользователя..."

    # Завершаем процесс Claude (как /tg)
    # Session ID остаётся в active_session.txt для --resume
    exit 0
else
    err_msg=$(echo "$response" | jq -r '.error // "Unknown error"')
    error "Не удалось отправить вопрос: $err_msg"
fi
