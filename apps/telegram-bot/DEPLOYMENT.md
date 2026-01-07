# 🚀 Полное руководство по развертыванию Telegram бота

Пошаговая инструкция по установке и настройке Telegram бота с интеграцией Claude Code на новом сервере.

---

## 📋 Требования к серверу

### Минимальные требования

- **ОС:** Ubuntu 22.04 LTS / Debian 11+ (рекомендуется) или другой Linux
- **CPU:** 2 cores
- **RAM:** 2 GB минимум (4 GB рекомендуется)
- **Диск:** 10 GB свободного места
- **Network:** Стабильное интернет-соединение
- **Доступ:** SSH с sudo/root правами

### Что будет установлено

- Docker & Docker Compose
- Node.js 20.x (для Claude CLI)
- Claude CLI
- Python 3.11+ (в контейнере)
- Telegram Bot (aiogram 3.14)

---

## 🔧 Шаг 1: Подготовка сервера

### 1.1. Подключитесь к серверу

```bash
ssh root@your-server-ip
```

### 1.2. Обновите систему

```bash
apt update && apt upgrade -y
```

### 1.3. Установите базовые утилиты

```bash
apt install -y curl wget git vim htop nano
```

---

## 🐳 Шаг 2: Установка Docker

### 2.1. Установите Docker Engine

```bash
# Удалите старые версии (если есть)
apt remove -y docker docker-engine docker.io containerd runc

# Установите зависимости
apt install -y ca-certificates curl gnupg lsb-release

# Добавьте официальный GPG ключ Docker
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Добавьте репозиторий Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установите Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 2.2. Проверьте установку

```bash
docker --version
docker compose version
```

Ожидаемый вывод:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

### 2.3. Запустите Docker

```bash
systemctl start docker
systemctl enable docker
systemctl status docker
```

---

## 📦 Шаг 3: Установка Node.js и Claude CLI

### 3.1. Установите Node.js 20.x

```bash
# Добавьте репозиторий NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -

# Установите Node.js
apt install -y nodejs

# Проверьте версию
node --version   # Должно быть v20.x.x
npm --version    # Должно быть v10.x.x
```

### 3.2. Установите Claude CLI

```bash
# Установите глобально через npm
npm install -g @anthropic-ai/claude-code

# Проверьте установку
claude --version
```

### 3.3. Настройте Claude CLI

```bash
# Авторизуйтесь (откроется браузер)
claude login

# Если на сервере нет GUI, используйте:
# 1. Запустите на локальной машине: claude login
# 2. Скопируйте токен из ~/.claude/config.json
# 3. Создайте config вручную на сервере
```

---

## 👤 Шаг 4: Создание пользователя claude-agent

### 4.1. Создайте группу и пользователя

```bash
# Создайте группу claude-agent (GID 986)
groupadd -g 986 claude-agent

# Создайте пользователя claude-agent (UID 994)
useradd -r -u 994 -g 986 -s /bin/bash -d /home/claude-agent -m claude-agent

# Добавьте в группу docker (для доступа к Docker socket)
usermod -aG docker claude-agent
```

### 4.2. Настройте sudo права

```bash
# Создайте sudoers файл для claude-agent
echo "claude-agent ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/claude-agent
chmod 440 /etc/sudoers.d/claude-agent
```

### 4.3. Настройте Claude CLI для claude-agent

```bash
# Скопируйте конфиг Claude для claude-agent
mkdir -p /home/claude-agent/.claude
cp -r ~/.claude/* /home/claude-agent/.claude/
chown -R claude-agent:claude-agent /home/claude-agent/.claude
```

### 4.4. Проверьте пользователя

```bash
# Проверьте ID
id claude-agent

# Ожидаемый вывод:
# uid=994(claude-agent) gid=986(claude-agent) groups=986(claude-agent),XXX(docker)

# Переключитесь на пользователя (тест)
su - claude-agent
claude --version  # Должно работать
exit
```

---

## 📁 Шаг 5: Установка workspace и бота

### 5.1. Создайте директорию workspace

```bash
mkdir -p /opt/ai-workspace
cd /opt/ai-workspace
```

### 5.2. Клонируйте или скопируйте проект

**Вариант A: Если у вас есть git репозиторий**

```bash
git clone https://your-repo-url.git /opt/ai-workspace
```

**Вариант B: Копирование с другого сервера**

На старом сервере:
```bash
cd /opt/ai-workspace
tar -czf telegram-bot-backup.tar.gz apps/telegram-bot
scp telegram-bot-backup.tar.gz root@new-server:/tmp/
```

На новом сервере:
```bash
cd /opt/ai-workspace
tar -xzf /tmp/telegram-bot-backup.tar.gz
```

**Вариант C: Создание структуры вручную**

```bash
mkdir -p /opt/ai-workspace/apps/telegram-bot/{src,logs}
cd /opt/ai-workspace/apps/telegram-bot

# Скачайте файлы проекта:
# - Dockerfile
# - docker-compose.yml
# - requirements.txt
# - src/bot.py
# - telegram_agent_context.md
```

### 5.3. Настройте права доступа

```bash
cd /opt/ai-workspace

# Создайте необходимые директории
mkdir -p .claude/skills/telegram-notifier/{tmp,uploads/{files,photos}}
mkdir -p apps/telegram-bot/logs

# Установите права
chown -R root:claude-agent .claude/skills/telegram-notifier
chmod -R 775 .claude/skills/telegram-notifier

chown -R root:root apps/telegram-bot
chmod 755 apps/telegram-bot
```

---

## 🔐 Шаг 6: Настройка конфигурации

### 6.1. Создайте Telegram бота

1. Откройте Telegram, найдите **@BotFather**
2. Отправьте `/newbot`
3. Назовите бота (например: "My Workspace Bot")
4. Придумайте username (например: `my_workspace_bot`)
5. Получите **токен**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### 6.2. Узнайте свой chat_id

**Способ 1 - Через @userinfobot:**
1. Найдите в Telegram: **@userinfobot**
2. Отправьте `/start`
3. Скопируйте свой ID (число)

**Способ 2 - Через API:**
1. Напишите любое сообщение своему боту
2. Откройте в браузере:
   ```
   https://api.telegram.org/bot<ВАШТОКЕН>/getUpdates
   ```
3. Найдите `"chat":{"id":123456789}`

### 6.3. Создайте .env файл

```bash
cd /opt/ai-workspace/apps/telegram-bot

# Создайте локальный .env (для docker-compose)
cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
TELEGRAM_CHAT_ID=ваш_chat_id

# HTTP API Configuration
BOT_HTTP_PORT=8081

# Logging
LOG_LEVEL=INFO

# OpenAI API (для Whisper транскрипции голосовых)
OPENAI_API_KEY=ваш_openai_api_key_если_есть
EOF

# Установите безопасные права
chmod 600 .env
```

### 6.4. (Опционально) Настройте глобальный .env

Если у вас есть общий .env для всего workspace:

```bash
cd /opt/ai-workspace

# Добавьте переменные в общий .env
cat >> .env << 'EOF'
# Telegram Bot
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_CHAT_ID=ваш_chat_id
OPENAI_API_KEY=ваш_openai_api_key
EOF
```

И обновите `docker-compose.yml` чтобы читать из `/opt/ai-workspace/.env`.

---

## 🏗️ Шаг 7: Сборка и запуск

### 7.1. Соберите Docker образ

```bash
cd /opt/ai-workspace/apps/telegram-bot

# Соберите образ
docker-compose build
```

### 7.2. Запустите контейнер

```bash
docker-compose up -d
```

### 7.3. Проверьте статус

```bash
# Проверьте контейнер
docker ps | grep telegram-bot

# Должны увидеть:
# ai-workspace-telegram-bot   Up X seconds   0.0.0.0:8081->8081/tcp

# Проверьте логи
docker logs -f ai-workspace-telegram-bot
```

Ожидаемый вывод:
```
🚀 Запуск Telegram бота...
Разрешённый chat_id: 123456789
HTTP API запущен на порту 8081
✅ Бот готов к работе
```

### 7.4. Проверьте health endpoint

```bash
curl http://localhost:8081/health
```

Ожидаемый ответ:
```json
{"status":"ok","uptime":"2026-01-07T...","messages_count":0}
```

---

## ✅ Шаг 8: Финальная проверка

### 8.1. Проверьте бота в Telegram

1. Найдите своего бота в Telegram (по username)
2. Отправьте `/start`
3. Бот должен ответить приветственным сообщением

### 8.2. Проверьте отправку сообщений

```bash
# Создайте тестовый скрипт для отправки
mkdir -p /opt/ai-workspace/commands

cat > /opt/ai-workspace/commands/tg-send.sh << 'EOFSCRIPT'
#!/bin/bash
# Простой скрипт для отправки сообщений в Telegram

API_URL="http://localhost:8081/send"

if [ "$1" = "--file" ]; then
    # Отправка файла
    FILE_PATH="$2"
    CAPTION="${3:-}"

    curl -X POST http://localhost:8081/send_file \
        -F "file=@$FILE_PATH" \
        -F "caption=$CAPTION"
else
    # Отправка текста
    TEXT="$1"

    curl -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "{\"text\":\"$TEXT\",\"parse_mode\":\"HTML\"}"
fi
EOFSCRIPT

chmod +x /opt/ai-workspace/commands/tg-send.sh

# Протестируйте
/opt/ai-workspace/commands/tg-send.sh "✅ Бот успешно установлен!"
```

Вы должны получить сообщение в Telegram!

### 8.3. Проверьте интеграцию с Claude

Напишите боту в Telegram:
```
Привет! Какая сегодня дата?
```

Бот должен:
1. Принять сообщение
2. Запустить Claude Code сессию
3. Ответить результатом

---

## 🔄 Шаг 9: Настройка автозапуска

### 9.1. Проверьте Docker autostart

```bash
# Docker должен запускаться автоматически
systemctl is-enabled docker
# Должен вывести: enabled

# Контейнер настроен на restart: unless-stopped в docker-compose.yml
```

### 9.2. (Опционально) Создайте systemd service

Если не используете `restart: unless-stopped` в docker-compose:

```bash
cat > /etc/systemd/system/telegram-bot.service << 'EOF'
[Unit]
Description=Telegram Bot with Claude Code Integration
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/ai-workspace/apps/telegram-bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
ExecReload=/usr/bin/docker-compose restart

[Install]
WantedBy=multi-user.target
EOF

# Активируйте service
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
```

---

## 🛡️ Шаг 10: Безопасность

### 10.1. Настройте firewall (если нужно)

```bash
# Если используете ufw
apt install -y ufw

# Разрешите SSH
ufw allow 22/tcp

# Закройте порт 8081 для внешнего доступа (бот доступен только локально)
# По умолчанию Docker может обойти UFW, поэтому:
# В docker-compose.yml используйте: "127.0.0.1:8081:8081"

ufw enable
```

### 10.2. Защитите .env файлы

```bash
# Убедитесь что .env не читаем другими пользователями
chmod 600 /opt/ai-workspace/.env
chmod 600 /opt/ai-workspace/apps/telegram-bot/.env

# Добавьте в .gitignore
echo ".env" >> /opt/ai-workspace/.gitignore
```

### 10.3. Настройте logrotate

```bash
cat > /etc/logrotate.d/telegram-bot << 'EOF'
/opt/ai-workspace/apps/telegram-bot/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
EOF
```

---

## 🔍 Шаг 11: Мониторинг и логи

### 11.1. Полезные команды

```bash
# Статус контейнера
docker ps | grep telegram-bot

# Логи в реальном времени
docker logs -f ai-workspace-telegram-bot

# Последние 100 строк логов
docker logs --tail 100 ai-workspace-telegram-bot

# Статистика ресурсов
docker stats ai-workspace-telegram-bot

# Проверка здоровья
curl http://localhost:8081/health
```

### 11.2. Структура логов

```
/opt/ai-workspace/apps/telegram-bot/logs/
├── bot_2026-01-07.log     # Логи бота (ротация ежедневная)
└── nohup.log              # Если запускается через nohup (deprecated)
```

---

## 🐛 Troubleshooting

### Проблема: Контейнер не запускается

```bash
# Проверьте логи
docker logs ai-workspace-telegram-bot

# Проверьте .env
docker exec ai-workspace-telegram-bot env | grep TELEGRAM

# Проверьте права на Docker socket
ls -la /var/run/docker.sock
# Должна быть группа docker

# Пересоберите
docker-compose down
docker-compose up -d --build
```

### Проблема: Бот не отвечает в Telegram

```bash
# Проверьте токен
curl "https://api.telegram.org/bot<ВАШТОКЕН>/getMe"

# Проверьте chat_id
grep TELEGRAM_CHAT_ID /opt/ai-workspace/apps/telegram-bot/.env

# Проверьте логи
docker logs ai-workspace-telegram-bot | grep -i error
```

### Проблема: Claude Code не запускается

```bash
# Проверьте что claude-agent может запускать Claude
su - claude-agent
cd /opt/ai-workspace
claude --version
exit

# Проверьте права на workspace
ls -la /opt/ai-workspace

# Проверьте логи Claude
ls -la /home/claude-agent/.claude/logs/
```

### Проблема: "Permission denied" на Docker socket

```bash
# Проверьте группу docker
getent group docker

# Добавьте claude-agent в группу
usermod -aG docker claude-agent

# Перезапустите контейнер
docker-compose restart
```

### Проблема: "Unauthorized" ошибка от Telegram

- Проверьте токен - скопирован ли полностью
- Убедитесь что нет лишних пробелов в .env
- Попробуйте создать нового бота

---

## 📚 Дополнительные настройки

### Интеграция с Nginx (опционально)

Если хотите выставить webhook вместо long polling:

```nginx
# /etc/nginx/sites-available/telegram-bot
server {
    listen 443 ssl;
    server_name bot.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Настройка MCP серверов (если используются)

```bash
# Установите необходимые MCP серверы
cd /opt/ai-workspace
# Следуйте инструкциям в .claude/skills/mcp-integration/
```

---

## ✅ Чеклист установки

- [ ] Docker и Docker Compose установлены
- [ ] Node.js 20.x установлен
- [ ] Claude CLI установлен и авторизован
- [ ] Пользователь claude-agent создан (UID 994, GID 986)
- [ ] claude-agent в группе docker
- [ ] Проект скопирован в /opt/ai-workspace/apps/telegram-bot
- [ ] .env файл создан и настроен
- [ ] Telegram бот создан через @BotFather
- [ ] TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID настроены
- [ ] Контейнер собран и запущен
- [ ] Health endpoint отвечает
- [ ] Бот отвечает на /start в Telegram
- [ ] Тестовое сообщение успешно отправлено
- [ ] Claude Code сессия запускается из бота
- [ ] Автозапуск настроен

---

## 🎉 Готово!

Ваш Telegram бот с интеграцией Claude Code успешно развернут!

**Следующие шаги:**
1. Прочитайте [README.md](./README.md) - описание возможностей
2. Изучите [SETUP.md](./SETUP.md) - дополнительные настройки
3. См. [telegram-notifier skill](../../.claude/skills/telegram-notifier/SKILL.md) - как использовать из Claude

**Полезные ссылки:**
- Документация Claude Code: https://code.claude.com/docs
- Telegram Bot API: https://core.telegram.org/bots/api
- Docker Docs: https://docs.docker.com
- aiogram 3 Docs: https://docs.aiogram.dev/en/latest/

**Поддержка:**
- GitHub Issues: (добавьте ссылку на ваш репозиторий)
- Telegram: (добавьте контакт для поддержки)

---

**Версия:** 1.0.0
**Дата:** 2026-01-07
**Автор:** AI Workspace Team
