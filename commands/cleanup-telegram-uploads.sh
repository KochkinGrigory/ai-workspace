#!/bin/bash
# Автоматическая очистка старых загруженных файлов из Telegram
# Запускается через cron каждую ночь в 3:00

set -e

LOG_FILE="/opt/ai-workspace/logs/telegram-uploads-cleanup.log"
UPLOADS_DIR="/opt/ai-workspace/.claude/skills/telegram-notifier/uploads"
DAYS_TO_KEEP=7

# Создаем директорию для логов если нет
mkdir -p "$(dirname "$LOG_FILE")"

# Функция логирования
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Начало очистки загруженных файлов ==="

# Проверяем существование директории
if [ ! -d "$UPLOADS_DIR" ]; then
    log "⚠️ Директория $UPLOADS_DIR не существует, пропускаем очистку"
    exit 0
fi

# Счётчики
total_deleted=0
total_size_freed=0

# Очистка фотографий
PHOTOS_DIR="$UPLOADS_DIR/photos"
if [ -d "$PHOTOS_DIR" ]; then
    log "📸 Проверка фотографий в $PHOTOS_DIR"

    # Находим и удаляем файлы старше 7 дней
    while IFS= read -r -d '' file; do
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
        rm -f "$file"
        total_deleted=$((total_deleted + 1))
        total_size_freed=$((total_size_freed + size))
        log "  ✓ Удалено: $(basename "$file") ($(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo "${size}B"))"
    done < <(find "$PHOTOS_DIR" -type f -mtime +$DAYS_TO_KEEP -print0 2>/dev/null)
else
    log "⚠️ Директория $PHOTOS_DIR не существует"
fi

# Очистка документов
FILES_DIR="$UPLOADS_DIR/files"
if [ -d "$FILES_DIR" ]; then
    log "📎 Проверка документов в $FILES_DIR"

    # Находим и удаляем файлы старше 7 дней
    while IFS= read -r -d '' file; do
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
        rm -f "$file"
        total_deleted=$((total_deleted + 1))
        total_size_freed=$((total_size_freed + size))
        log "  ✓ Удалено: $(basename "$file") ($(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo "${size}B"))"
    done < <(find "$FILES_DIR" -type f -mtime +$DAYS_TO_KEEP -print0 2>/dev/null)
else
    log "⚠️ Директория $FILES_DIR не существует"
fi

# Итоговая статистика
if [ $total_deleted -gt 0 ]; then
    size_mb=$((total_size_freed / 1024 / 1024))
    log "✅ Очистка завершена: удалено $total_deleted файлов, освобождено ~${size_mb}MB"
else
    log "ℹ️ Нет файлов старше $DAYS_TO_KEEP дней для удаления"
fi

log "=== Конец очистки ==="
log ""

exit 0
