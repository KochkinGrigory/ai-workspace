# Автоматическая очистка загруженных файлов

## 📋 Обзор

Настроена автоматическая очистка файлов, загруженных пользователями через Telegram бота:
- **Что удаляется**: файлы старше 7 дней
- **Когда**: каждый день в 3:00 ночи
- **Где**:
  - `/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/` - фото
  - `/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files/` - документы
  - `/opt/ai-workspace/.claude/skills/telegram-notifier/tmp/` - временные файлы (старше 1 дня)

## 🔧 Компоненты

### 1. Скрипт очистки
**Путь**: `/opt/ai-workspace/.claude/skills/telegram-notifier/cleanup-uploads.sh`

**Запуск вручную**:
```bash
sudo /opt/ai-workspace/.claude/skills/telegram-notifier/cleanup-uploads.sh
```

### 2. Cron задача
**Конфигурация**: root crontab

**Просмотр**:
```bash
sudo crontab -l
```

**Расписание**: `0 3 * * *` (каждый день в 3:00)

### 3. Логи
**Путь**: `/opt/ai-workspace/logs/telegram-uploads-cleanup.log`

**Просмотр последних записей**:
```bash
tail -f /opt/ai-workspace/logs/telegram-uploads-cleanup.log
```

## 📊 Статистика

**Текущие файлы**:
```bash
# Фотографии
ls -lh /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/

# Документы
ls -lh /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files/

# Временные
ls -lh /opt/ai-workspace/.claude/skills/telegram-notifier/tmp/
```

**Статистика**:
```bash
echo "Фото: $(find /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/ -type f | wc -l)"
echo "Документы: $(find /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files/ -type f | wc -l)"
echo "Временные: $(find /opt/ai-workspace/.claude/skills/telegram-notifier/tmp/ -type f | wc -l)"
```

## 🛠️ Управление

### Запустить очистку вручную
```bash
sudo /opt/ai-workspace/.claude/skills/telegram-notifier/cleanup-uploads.sh
```

### Изменить расписание
```bash
# Редактировать crontab
sudo crontab -e

# Примеры расписаний:
# 0 3 * * *     - каждый день в 3:00
# 0 */6 * * *   - каждые 6 часов
# 0 0 * * 0     - каждое воскресенье в полночь
```

### Изменить срок хранения файлов

Отредактируйте скрипт `/opt/ai-workspace/.claude/skills/telegram-notifier/cleanup-uploads.sh`:

```bash
# Найдите строки с `-mtime +7` и измените число:
# -mtime +7  → файлы старше 7 дней
# -mtime +14 → файлы старше 14 дней
# -mtime +30 → файлы старше 30 дней
```

### Отключить автоочистку
```bash
# Удалить задачу из crontab
sudo crontab -l | grep -v cleanup-uploads.sh | sudo crontab -
```

### Включить автоочистку обратно
```bash
(sudo crontab -l 2>/dev/null; echo "0 3 * * * /opt/ai-workspace/.claude/skills/telegram-notifier/cleanup-uploads.sh") | sudo crontab -
```

## 🔍 Диагностика

### Проверка что cron работает
```bash
# Статус сервиса
ps aux | grep cron | grep -v grep

# Если не запущен - запустить
sudo service cron start
```

### Просмотр логов cron
```bash
# Системные логи cron (если доступно)
tail -f /var/log/cron.log

# Логи нашего скрипта
tail -f /opt/ai-workspace/logs/telegram-uploads-cleanup.log
```

### Тестирование

**1. Создать тестовый старый файл**:
```bash
# Создаём файл
touch /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/test.jpg

# Меняем дату модификации (8 дней назад)
touch -d "8 days ago" /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/test.jpg

# Проверяем
ls -lh /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/test.jpg
```

**2. Запустить очистку**:
```bash
sudo /opt/ai-workspace/.claude/skills/telegram-notifier/cleanup-uploads.sh
```

**3. Проверить что файл удалён**:
```bash
ls -lh /opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos/test.jpg
# Должно вернуть: No such file or directory
```

## ⚠️ Важные замечания

1. **Резервные копии**: Автоочистка удаляет файлы безвозвратно. Если нужны файлы дольше 7 дней - перемещайте их в другую директорию.

2. **Временные файлы**: Файлы в `tmp/` должны удаляться сразу после отправки в Telegram. Если они остаются дольше 1 дня - это признак проблемы.

3. **Права доступа**: Скрипт должен запускаться от root (через sudo в cron), чтобы иметь права на удаление файлов.

4. **Дисковое пространство**: Регулярно проверяйте использование диска:
   ```bash
   df -h /opt/ai-workspace
   ```

## 📝 История изменений

- **2025-11-03**: Первая версия автоочистки (7 дней хранения)

## 🔗 См. также

- [SKILL.md](./SKILL.md) - Основная документация telegram-notifier skill
- [telegram_agent_context.md](/opt/ai-workspace/apps/telegram-bot/telegram_agent_context.md) - Контекст для Claude при запуске из Telegram
- [CLAUDE.md](/opt/ai-workspace/CLAUDE.md) - Общая документация проекта
