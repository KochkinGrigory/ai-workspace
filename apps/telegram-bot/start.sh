#!/bin/bash
#
# start.sh - Запуск Telegram бота
#

cd /opt/ai-workspace/apps/telegram-bot

# Проверка зависимостей
if ! python3 -c "import aiogram" 2>/dev/null; then
    echo "Установка зависимостей..."
    pip3 install -r requirements.txt --break-system-packages
fi

# Создание директории для логов
mkdir -p logs

# Проверка .env
if ! grep -q "^TELEGRAM_BOT_TOKEN=" /opt/ai-workspace/.env; then
    echo "❌ TELEGRAM_BOT_TOKEN не настроен в .env"
    exit 1
fi

# Запуск бота
echo "🚀 Запуск Telegram бота..."
nohup python3 src/bot.py > logs/nohup.log 2>&1 &
echo $! > logs/bot.pid

echo "✅ Бот запущен (PID: $(cat logs/bot.pid))"
echo "📋 Логи: tail -f logs/nohup.log"
