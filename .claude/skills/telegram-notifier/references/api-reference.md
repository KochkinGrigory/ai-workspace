# Telegram Bot HTTP API Reference

## Endpoints

### POST /send
Отправить текстовое сообщение

**Request:**
```json
{
  "text": "Текст сообщения",
  "parse_mode": "HTML" | "Markdown"
}
```

**Response (Success):**
```json
{
  "success": true
}
```

**Response (Error):**
```json
{
  "error": "Error message"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8081/send \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello!", "parse_mode": "HTML"}'
```

---

### POST /send_file
Отправить файл

**Request:**
- Multipart form data
- `file`: binary file data
- `caption`: описание файла (опционально)

**Response (Success):**
```json
{
  "success": true,
  "file": "filename.ext"
}
```

**Response (Error):**
```json
{
  "error": "Error message"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8081/send_file \
  -F "file=@/path/to/report.xlsx" \
  -F "caption=Отчёт за октябрь"
```

---

### GET /health
Проверка состояния бота

**Response:**
```json
{
  "status": "ok",
  "uptime": "2025-11-02T12:34:56",
  "messages_count": 42
}
```

**cURL Example:**
```bash
curl http://localhost:8081/health
```

---

## Helper Script

Рекомендуется использовать helper скрипт вместо прямых curl запросов:

```bash
# Отправить текст
/opt/ai-workspace/commands/tg-send.sh "message"

# Отправить HTML
/opt/ai-workspace/commands/tg-send.sh "<b>bold</b> text"

# Отправить Markdown
/opt/ai-workspace/commands/tg-send.sh --markdown "*italic* text"

# Отправить файл
/opt/ai-workspace/commands/tg-send.sh --file /path/to/file.pdf "caption"

# Помощь
/opt/ai-workspace/commands/tg-send.sh --help
```

## Error Handling

### Возможные ошибки:

**Bot not running:**
```
curl: (7) Failed to connect to localhost port 8081: Connection refused
```
Решение: `docker-compose up -d` в `/opt/ai-workspace/apps/telegram-bot`

**Invalid token:**
```json
{"error": "Unauthorized"}
```
Решение: проверь `TELEGRAM_BOT_TOKEN` в `.env`

**Chat not found:**
```json
{"error": "Bad Request: chat not found"}
```
Решение: проверь `TELEGRAM_CHAT_ID` в `.env`, напиши боту `/start`

**File too large:**
```json
{"error": "Request entity too large"}
```
Решение: Telegram лимит файла - 50MB для ботов

## Rate Limits

Telegram Bot API ограничения:
- Максимум 30 сообщений в секунду
- Максимум 20 сообщений в минуту в один чат
- Максимальный размер файла: 50 MB

Helper скрипт автоматически обрабатывает эти ограничения.
