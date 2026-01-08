#!/bin/bash

# Скрипт очистки старых загруженных файлов от пользователей Telegram
# Удаляет файлы старше 7 дней из директорий uploads/photos и uploads/files

set -euo pipefail

# Директории для очистки
PHOTOS_DIR="/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/photos"
FILES_DIR="/opt/ai-workspace/.claude/skills/telegram-notifier/uploads/files"
TMP_DIR="/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"

# Логирование
LOG_FILE="/opt/ai-workspace/logs/telegram-uploads-cleanup.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Функция логирования
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== Начало очистки загруженных файлов ==="

# Очистка фотографий старше 7 дней
if [ -d "$PHOTOS_DIR" ]; then
    log "Проверяю фото в $PHOTOS_DIR"
    DELETED_PHOTOS=$(find "$PHOTOS_DIR" -type f -name "*.jpg" -mtime +7 2>/dev/null | wc -l)

    if [ "$DELETED_PHOTOS" -gt 0 ]; then
        find "$PHOTOS_DIR" -type f -name "*.jpg" -mtime +7 -delete
        log "Удалено фото: $DELETED_PHOTOS файлов"
    else
        log "Фото для удаления не найдено"
    fi
else
    log "WARN: Директория $PHOTOS_DIR не существует"
fi

# Очистка документов старше 7 дней
if [ -d "$FILES_DIR" ]; then
    log "Проверяю документы в $FILES_DIR"
    DELETED_FILES=$(find "$FILES_DIR" -type f -mtime +7 2>/dev/null | wc -l)

    if [ "$DELETED_FILES" -gt 0 ]; then
        find "$FILES_DIR" -type f -mtime +7 -delete
        log "Удалено документов: $DELETED_FILES файлов"
    else
        log "Документов для удаления не найдено"
    fi
else
    log "WARN: Директория $FILES_DIR не существует"
fi

# Очистка временных файлов старше 1 дня (они должны удаляться сразу после отправки)
if [ -d "$TMP_DIR" ]; then
    log "Проверяю временные файлы в $TMP_DIR"
    DELETED_TMP=$(find "$TMP_DIR" -type f -mtime +1 2>/dev/null | wc -l)

    if [ "$DELETED_TMP" -gt 0 ]; then
        find "$TMP_DIR" -type f -mtime +1 -delete
        log "Удалено забытых временных файлов: $DELETED_TMP файлов"
    else
        log "Забытых временных файлов не найдено"
    fi
else
    log "WARN: Директория $TMP_DIR не существует"
fi

# Статистика оставшихся файлов
REMAINING_PHOTOS=$(find "$PHOTOS_DIR" -type f 2>/dev/null | wc -l || echo 0)
REMAINING_FILES=$(find "$FILES_DIR" -type f 2>/dev/null | wc -l || echo 0)
REMAINING_TMP=$(find "$TMP_DIR" -type f 2>/dev/null | wc -l || echo 0)

log "=== Статистика после очистки ==="
log "Фото: $REMAINING_PHOTOS файлов"
log "Документы: $REMAINING_FILES файлов"
log "Временные: $REMAINING_TMP файлов"
log "=== Очистка завершена ==="
log ""
