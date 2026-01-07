# AI Workspace - Technical Documentation

Production workspace для Claude Code на сервере analiticalo.ru

> Для инструкций Claude Code см. [CLAUDE.md](./CLAUDE.md)

---

## Обзор

**Назначение:** Centralized workspace для разработки с Claude Code, хостинг приложений, интеграция с Supabase
**Сервер:** 5.129.236.4 (production)
**ОС:** Linux (Ubuntu/Debian)
**Пользователь:** root (workspace), claude-agent (telegram bot)

---

## Структура проекта

```
/opt/ai-workspace/
├── .claude/                  # Claude Code конфигурация
│   ├── commands/            # Slash команды (markdown)
│   ├── skills/              # Skills (модульные возможности)
│   └── settings.local.json  # Локальные настройки
│
├── apps/                    # Приложения
│   ├── dashboard-pages/     # Дашборды с визуализацией (порт 3001)
│   ├── webapp/              # Веб-сайты и лендинги (порт 3005)
│   └── telegram-bot/        # Telegram бот (порт 8081)
│
├── commands/                # Shell скрипты для автоматизации
├── templates/               # Шаблоны проектов
├── config/                  # Конфигурационные файлы
├── logs/                    # Логи операций
├── supabase -> /opt/supabase  # Симлинк на Supabase
│
├── .env                     # Переменные окружения (не коммитить!)
├── CLAUDE.md                # Инструкции для Claude Code
├── README.md                # Техническая документация (этот файл)
└── components.json          # Конфиг shadcn UI
```

---

## Приложения

### 1. Dashboard Pages (порт 3001)

**Путь:** `/opt/ai-workspace/apps/dashboard-pages/`
**Технологии:** Next.js 15, TypeScript, Recharts, Tailwind CSS
**Назначение:** Интерактивные дашборды с визуализацией данных из БД

**Структура:**
```
dashboard-pages/
├── frontend/
│   ├── src/app/
│   │   ├── [report-name]/     # Каждый дашборд = отдельная папка
│   │   │   └── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

**Docker:**
- Container: `dashboard-frontend`
- Port: `3001:3001`
- Status: Up (может быть unhealthy если нет дашбордов)

**Команды:**
```bash
cd /opt/ai-workspace/apps/dashboard-pages
docker-compose restart          # После создания/изменения страниц
docker-compose logs -f          # Логи
docker-compose down && docker-compose up -d --build  # Полный rebuild
```

**URL:** http://5.129.236.4:3001/[report-name]

---

### 2. WebApp (порт 3005)

**Путь:** `/opt/ai-workspace/apps/webapp/`
**Технологии:** Next.js 15, TypeScript, @animate-ui, @aceternity, Tailwind CSS
**Назначение:** Веб-сайты, лендинги с анимациями и визуальными эффектами

**Структура:**
```
webapp/
├── frontend/
│   ├── src/app/
│   │   ├── [page-name]/       # Каждый сайт = отдельная папка
│   │   │   └── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/ui/         # shadcn компоненты
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

**Docker:**
- Container: `webapp-frontend`
- Port: `3005:3005`
- Status: Up

**Команды:**
```bash
cd /opt/ai-workspace/apps/webapp
docker-compose restart          # После создания/изменения страниц
docker-compose logs -f          # Логи
docker-compose down && docker-compose up -d --build  # Полный rebuild
```

**URL:** http://5.129.236.4:3005/[page-name]

---

### 3. Telegram Bot (порт 8081)

**Путь:** `/opt/ai-workspace/apps/telegram-bot/`
**Технологии:** Python 3.11, aiogram, Docker
**Назначение:** Telegram бот для взаимодействия с Claude Code

**Структура:**
```
telegram-bot/
├── bot.py                     # Основной файл бота
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env                       # Токен бота и настройки
```

**Docker:**
- Container: `ai-workspace-telegram-bot`
- Port: `8081:8081` (webhook)
- User: `claude-agent` (внутри контейнера имеет доступ к docker socket)
- Status: Up (healthy)

**Команды:**
```bash
cd /opt/ai-workspace/apps/telegram-bot
docker-compose restart
docker-compose logs -f telegram-bot
```

**Uploads:**
- Фото: `.claude/skills/telegram-notifier/uploads/photos/`
- Файлы: `.claude/skills/telegram-notifier/uploads/files/`
- Автоочистка: cron job в 3:00 удаляет файлы старше 7 дней

**Документация:**
- [DEPLOYMENT.md](./apps/telegram-bot/DEPLOYMENT.md) - Установка на новом сервере с нуля
- [SETUP.md](./apps/telegram-bot/SETUP.md) - Быстрая настройка токенов
- [README.md](./apps/telegram-bot/README.md) - Полное описание возможностей

---

## Инфраструктура

### Supabase

**Путь:** `/opt/supabase` (симлинк: `/opt/ai-workspace/supabase`)
**Компоненты:**

| Service | Container | Port | Status |
|---------|-----------|------|--------|
| PostgreSQL | supabase-db | 5432 | Up (healthy) |
| Kong (API Gateway) | supabase-kong | 8000, 8443 | Up (healthy) |
| Studio | supabase-studio | 9000 | Up (healthy) |
| Auth | supabase-auth | - | Up (healthy) |
| Storage | supabase-storage | 5000 | Up (healthy) |
| Realtime | supabase-realtime | - | Up (healthy) |
| Edge Functions | supabase-edge-functions | - | Up |

**Доступ к БД:**
- Через MCP: `mcp__buisness-database-analiticalo__query` (read-only)
- Direct PostgreSQL: `localhost:5432` (credentials в .env)

**URLs:**
- API: https://api.analiticalo.ru (Kong, порт 8443)
- Studio: https://studio.analiticalo.ru (Nginx → 9000)

---

## Сеть и домены

### Текущие URL

| Service | URL | Port | SSL |
|---------|-----|------|-----|
| Supabase API | https://api.analiticalo.ru | 8443 | ✅ |
| Supabase Studio | https://studio.analiticalo.ru | 9000 | ✅ |
| Dashboard Pages | http://5.129.236.4:3001 | 3001 | ❌ |
| WebApp | http://5.129.236.4:3005 | 3005 | ❌ |

### Доступные домены для деплоя

- `app.analiticalo.ru` - не используется
- `dashboard.analiticalo.ru` - не используется
- `admin.analiticalo.ru` - не используется

### Nginx конфигурация

**Файлы:** `/etc/nginx/sites-available/`, `/etc/nginx/sites-enabled/`

**Текущие конфиги:**
- `api.analiticalo.ru` → proxy_pass http://localhost:8443 (Kong)
- `studio.analiticalo.ru` → proxy_pass http://localhost:9000 (Studio)

**Команды:**
```bash
sudo nginx -t                  # Проверить конфигурацию
sudo systemctl reload nginx    # Применить изменения
sudo systemctl status nginx    # Статус
```

---

## База данных (PostgreSQL)

### Доступ

**Read-Only через MCP:** `mcp__buisness-database-analiticalo__query`

**Direct access:**
```bash
# Через Docker
docker exec -it supabase-db psql -U postgres -d postgres

# Через локальный psql
psql -h localhost -p 5432 -U postgres -d postgres
```

### Основные таблицы

| Таблица | Назначение |
|---------|------------|
| `leads` | Заявки клиентов, конверсии |
| `sales` | Транзакции продаж |
| `read_before_start_analis` | Документация, бизнес-логика |

**Важно:**
- Уникальность клиентов: поле `phone`
- Бизнес-логика конверсий в таблице `read_before_start_analis`

---

## Skills и команды

### Skills

**Путь:** `/opt/ai-workspace/.claude/skills/`

Доступные skills:
- `dashboard-pages-generator` - генерация дашбордов
- `website-pages-generator` - создание сайтов
- `analiticalo-db-analytics` - SQL аналитика
- `xlsx` - работа с Excel
- `telegram-notifier` - Telegram уведомления
- `ui-components-library` - UI компоненты
- `skill-creator` - создание skills

Подробнее: [.claude/SKILLS_QUICK_REFERENCE.md](./.claude/SKILLS_QUICK_REFERENCE.md)

### Slash Commands

**Путь:** `/opt/ai-workspace/.claude/commands/`

Доступные команды:
- `/tg [текст]` - отправить сообщение в Telegram
- `/tg-file [путь]` - отправить файл в Telegram
- `/tg-status` - проверить статус бота

---

## Безопасность

### Пользователи и права

- **Workspace:** работает от `root` (для гибкости разработки)
- **Telegram bot:** `claude-agent` (имеет доступ к docker socket)
- **Production apps:** рекомендуется создать `webapp-user`

### Секреты

**Файл:** `/opt/ai-workspace/.env` (НЕ коммитить в git!)

Содержит:
- Supabase credentials
- Telegram bot token
- Database URLs
- API keys

### Firewall (UFW)

```bash
sudo ufw status
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 8081/tcp    # Telegram webhook
```

---

## Разработка

### Создание нового приложения

1. Создай директорию в `apps/[app-name]/`
2. Добавь `docker-compose.yml`
3. Настрой порт (используй 3000-3999)
4. Создай `.claude/` для app-specific команд (опционально)

### Деплой на домен

1. Создай Nginx конфиг:
```bash
sudo nano /etc/nginx/sites-available/subdomain.analiticalo.ru
```

2. Настрой proxy_pass:
```nginx
server {
    listen 80;
    server_name subdomain.analiticalo.ru;

    location / {
        proxy_pass http://localhost:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Включи конфиг:
```bash
sudo ln -s /etc/nginx/sites-available/subdomain.analiticalo.ru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

4. Получи SSL сертификат:
```bash
sudo certbot --nginx -d subdomain.analiticalo.ru
```

### Добавление нового skill

```bash
cd /opt/ai-workspace/.claude/skills
python3 ../../../.claude/skills/skill-creator/scripts/init_skill.py skill-name --path .
```

См. [skill-creator/SKILL.md](./.claude/skills/skill-creator/SKILL.md)

---

## Мониторинг

### Docker

```bash
# Все контейнеры
docker ps -a

# Конкретное приложение
docker ps | grep dashboard
docker ps | grep webapp
docker ps | grep telegram

# Логи
docker logs -f container-name
docker-compose logs -f service-name

# Статистика
docker stats
```

### Nginx

```bash
# Логи доступа
sudo tail -f /var/log/nginx/access.log

# Логи ошибок
sudo tail -f /var/log/nginx/error.log

# Статус
sudo systemctl status nginx
```

### Диск

```bash
df -h                          # Общее использование
du -sh /opt/ai-workspace/*     # По директориям
docker system df               # Docker использование

# Очистка Docker
docker system prune -a         # Удалить неиспользуемые образы
```

---

## Backup

### База данных

```bash
# Через Docker
docker exec supabase-db pg_dump -U postgres -d postgres > backup.sql

# Восстановление
docker exec -i supabase-db psql -U postgres -d postgres < backup.sql
```

### Приложения

```bash
# Резервная копия workspace
tar -czf ai-workspace-backup-$(date +%Y%m%d).tar.gz /opt/ai-workspace \
  --exclude='node_modules' \
  --exclude='.next' \
  --exclude='logs'
```

---

## Troubleshooting

### Проблема: Порт занят

```bash
# Найти процесс на порту
sudo lsof -ti:3001
sudo lsof -ti:3005

# Убить процесс
sudo kill -9 $(lsof -ti:3001)
```

### Проблема: 404 после создания страницы

**Причина:** Забыли перезапустить Docker

**Решение:**
```bash
cd /opt/ai-workspace/apps/dashboard-pages
docker-compose restart

# Проверка
curl -I http://5.129.236.4:3001/page-name
```

### Проблема: Docker контейнер unhealthy

```bash
# Проверить логи
docker logs container-name

# Перезапустить
docker restart container-name

# Полный rebuild
cd /opt/ai-workspace/apps/[app-name]
docker-compose down
docker-compose up -d --build
```

### Проблема: Нет места на диске

```bash
# Проверить использование
df -h

# Очистить Docker
docker system prune -a -f
docker volume prune -f

# Очистить логи
sudo journalctl --vacuum-time=7d
```

---

## Tech Stack

| Категория | Технологии |
|-----------|-----------|
| **Backend** | Supabase (PostgreSQL + API), Python (Telegram bot) |
| **Frontend** | Next.js 15, React 18, TypeScript |
| **UI** | Tailwind CSS, shadcn UI, @animate-ui, @aceternity |
| **Визуализация** | Recharts |
| **Deployment** | Docker Compose, Nginx, Let's Encrypt |
| **Интеграция** | MCP (Model Context Protocol) |
| **Бот** | aiogram (Python) |

---

## Полезные ссылки

- **Claude Code Docs:** https://docs.claude.com/claude-code
- **Supabase Docs:** https://supabase.com/docs
- **Next.js Docs:** https://nextjs.org/docs
- **shadcn UI:** https://ui.shadcn.com
- **Recharts:** https://recharts.org

---

## Changelog

- **2025-11-04:** Реструктуризация документации (CLAUDE.md + README.md)
- **2025-11-03:** Добавлен webapp (порт 3005)
- **2025-11-02:** Создан dashboard-pages (порт 3001)
- **2025-11-01:** Первоначальная настройка workspace

---

**Для инструкций Claude Code см. [CLAUDE.md](./CLAUDE.md)**
