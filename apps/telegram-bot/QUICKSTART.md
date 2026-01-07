# 🚀 Quick Start - Telegram Bot

Бот запущен и работает! ✅

## 📊 Текущий статус

```bash
# Проверка статуса
curl http://localhost:8081/health

# Логи (в реальном времени)
tail -f /opt/ai-workspace/apps/telegram-bot/logs/nohup.log

# Процесс
ps aux | grep "python3 src/bot.py"
```

## 💬 Как отправлять сообщения

### Простое сообщение
```bash
/opt/ai-workspace/commands/tg-send.sh "Привет!"
```

### С форматированием
```bash
/opt/ai-workspace/commands/tg-send.sh "✅ <b>Готово!</b> Проверяй результаты"
```

### Отправить файл
```bash
/opt/ai-workspace/commands/tg-send.sh --file /path/to/file.xlsx "Описание"
```

## 🔄 Управление ботом

### Запуск
```bash
cd /opt/ai-workspace/apps/telegram-bot
./start.sh
```

### Остановка
```bash
cd /opt/ai-workspace/apps/telegram-bot
./stop.sh
```

### Перезапуск
```bash
./stop.sh && ./start.sh
```

## 📁 Важные файлы

- **Конфиг:** `/opt/ai-workspace/.env`
- **Логи:** `/opt/ai-workspace/apps/telegram-bot/logs/`
- **Код:** `/opt/ai-workspace/apps/telegram-bot/src/bot.py`
- **Skill:** `/opt/ai-workspace/.claude/skills/telegram-notifier/`

## 🤖 Claude Integration

Когда ты просишь меня (Claude) отправить что-то в Telegram, я использую:
```bash
/opt/ai-workspace/commands/tg-send.sh "твоё сообщение"
```

**Примеры команд:**
- "Отправь мне в телеграм результаты анализа"
- "Пришли отчёт в бота"
- "Уведоми меня когда закончишь"

## 🔧 Troubleshooting

### Бот не отвечает
```bash
# Проверь процесс
ps aux | grep bot.py

# Перезапусти
./stop.sh && ./start.sh
```

### Сообщения не приходят
```bash
# Проверь health
curl http://localhost:8081/health

# Проверь логи на ошибки
tail -50 logs/nohup.log | grep -i error
```

### Проверка конфигурации
```bash
grep TELEGRAM /opt/ai-workspace/.env
```

## 📚 Полная документация

- **README:** `/opt/ai-workspace/apps/telegram-bot/README.md`
- **Setup Guide:** `/opt/ai-workspace/apps/telegram-bot/SETUP.md`
- **Skill Docs:** `/opt/ai-workspace/.claude/skills/telegram-notifier/SKILL.md`
