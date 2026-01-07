#!/bin/bash
#
# tg-send.sh - Helper скрипт для отправки сообщений в Telegram через бота
#
# Использование:
#   tg-send.sh "текст сообщения"
#   tg-send.sh --file /path/to/file.txt "описание файла"
#   tg-send.sh --html "<b>жирный</b> текст"
#

set -euo pipefail

# Конфигурация
BOT_API="http://localhost:8081"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция вывода ошибки
error() {
    echo -e "${RED}❌ Ошибка: $1${NC}" >&2
    exit 1
}

# Функция вывода успеха
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Функция вывода предупреждения
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Проверка, что бот запущен
check_bot_running() {
    if ! curl -s -f "$BOT_API/health" > /dev/null 2>&1; then
        error "Telegram бот не запущен или недоступен!\nЗапусти: cd /opt/ai-workspace/apps/telegram-bot && docker-compose up -d"
    fi
}

# Отправка текстового сообщения
send_text() {
    local text="$1"
    local parse_mode="${2:-HTML}"

    local response
    response=$(curl -s -X POST "$BOT_API/send" \
        -H "Content-Type: application/json" \
        -d "{\"text\": $(echo "$text" | jq -Rs .), \"parse_mode\": \"$parse_mode\"}")

    if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
        success "Сообщение отправлено"
        return 0
    else
        local err_msg=$(echo "$response" | jq -r '.error // "Unknown error"')
        error "Не удалось отправить сообщение: $err_msg"
    fi
}

# Отправка файла
send_file() {
    local file_path="$1"
    local caption="${2:-}"

    if [[ ! -f "$file_path" ]]; then
        error "Файл не найден: $file_path"
    fi

    local response
    if [[ -n "$caption" ]]; then
        response=$(curl -s -X POST "$BOT_API/send_file" \
            -F "file=@$file_path" \
            -F "caption=$caption")
    else
        response=$(curl -s -X POST "$BOT_API/send_file" \
            -F "file=@$file_path")
    fi

    if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
        local filename=$(echo "$response" | jq -r '.file')
        success "Файл отправлен: $filename"
        return 0
    else
        local err_msg=$(echo "$response" | jq -r '.error // "Unknown error"')
        error "Не удалось отправить файл: $err_msg"
    fi
}

# Показать помощь
show_help() {
    cat << EOF
🤖 Telegram Bot - Helper для отправки сообщений

Использование:
  $(basename "$0") [опции] "текст или путь к файлу"

Опции:
  -f, --file PATH       Отправить файл (второй аргумент - описание)
  -h, --html            Использовать HTML форматирование (по умолчанию)
  -m, --markdown        Использовать Markdown форматирование
  --help                Показать эту справку

Примеры:
  # Простое текстовое сообщение
  $(basename "$0") "Привет из Claude!"

  # HTML форматирование
  $(basename "$0") "<b>Важно!</b> Проверь результаты"

  # Markdown форматирование
  $(basename "$0") --markdown "*Анализ завершён*"

  # Отправить файл
  $(basename "$0") --file report.xlsx "Отчёт по продажам за месяц"

  # Отправить файл без описания
  $(basename "$0") --file /tmp/screenshot.png

Проверка статуса:
  curl $BOT_API/health

Примечание:
  Бот должен быть запущен:
  cd /opt/ai-workspace/apps/telegram-bot && docker-compose up -d
EOF
}

# Парсинг аргументов
MODE="text"
PARSE_MODE="HTML"
FILE_PATH=""
CAPTION=""
MESSAGE=""

if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            show_help
            exit 0
            ;;
        -f|--file)
            MODE="file"
            FILE_PATH="$2"
            shift 2
            ;;
        -h|--html)
            PARSE_MODE="HTML"
            shift
            ;;
        -m|--markdown)
            PARSE_MODE="Markdown"
            shift
            ;;
        *)
            MESSAGE="$1"
            shift
            ;;
    esac
done

# Проверка зависимостей
if ! command -v curl &> /dev/null; then
    error "curl не установлен"
fi

if ! command -v jq &> /dev/null; then
    error "jq не установлен. Установи: apt-get install jq"
fi

# Проверка, что бот работает
check_bot_running

# Выполнение действия
if [[ "$MODE" == "file" ]]; then
    if [[ -z "$FILE_PATH" ]]; then
        error "Не указан путь к файлу"
    fi
    CAPTION="$MESSAGE"
    send_file "$FILE_PATH" "$CAPTION"
else
    if [[ -z "$MESSAGE" ]]; then
        error "Не указан текст сообщения"
    fi
    send_text "$MESSAGE" "$PARSE_MODE"
fi
