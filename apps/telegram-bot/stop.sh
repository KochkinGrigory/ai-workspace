#!/bin/bash
#
# stop.sh - Остановка Telegram бота
#

cd /opt/ai-workspace/apps/telegram-bot

if [ -f logs/bot.pid ]; then
    PID=$(cat logs/bot.pid)
    echo "🛑 Остановка бота (PID: $PID)..."
    kill $PID 2>/dev/null
    rm logs/bot.pid
    echo "✅ Бот остановлен"
else
    echo "⚠️  PID файл не найден, ищу процесс..."
    pkill -f "python3 src/bot.py"
    echo "✅ Процесс остановлен"
fi
