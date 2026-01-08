#!/bin/bash
#
# cleanup-tmp.sh - Очистка временных файлов в tmp/ директории
#
# Использование:
#   ./cleanup-tmp.sh [дней]   # По умолчанию 7 дней
#
# Примеры:
#   ./cleanup-tmp.sh          # Удалить файлы старше 7 дней
#   ./cleanup-tmp.sh 3        # Удалить файлы старше 3 дней
#   ./cleanup-tmp.sh 0        # Удалить ВСЕ файлы (кроме .gitkeep)
#

TMP_DIR="/opt/ai-workspace/.claude/skills/telegram-notifier/tmp"
DAYS_OLD=${1:-7}

echo "🧹 Очистка временных файлов..."
echo "Директория: $TMP_DIR"
echo "Удаляю файлы старше: $DAYS_OLD дней"
echo ""

if [ ! -d "$TMP_DIR" ]; then
    echo "❌ Директория $TMP_DIR не существует!"
    exit 1
fi

# Подсчёт файлов перед удалением
BEFORE_COUNT=$(find "$TMP_DIR" -type f ! -name '.gitkeep' | wc -l)

if [ "$BEFORE_COUNT" -eq 0 ]; then
    echo "✅ Нет файлов для удаления"
    exit 0
fi

echo "Найдено файлов: $BEFORE_COUNT"

# Удаление старых файлов
if [ "$DAYS_OLD" -eq 0 ]; then
    # Удалить ВСЕ файлы (кроме .gitkeep)
    find "$TMP_DIR" -type f ! -name '.gitkeep' -delete
else
    # Удалить файлы старше N дней
    find "$TMP_DIR" -type f ! -name '.gitkeep' -mtime +$DAYS_OLD -delete
fi

# Подсчёт после удаления
AFTER_COUNT=$(find "$TMP_DIR" -type f ! -name '.gitkeep' | wc -l)
DELETED=$((BEFORE_COUNT - AFTER_COUNT))

echo ""
echo "✅ Удалено файлов: $DELETED"
echo "Осталось файлов: $AFTER_COUNT"

# Показываем размер директории
DIR_SIZE=$(du -sh "$TMP_DIR" | cut -f1)
echo "Размер директории: $DIR_SIZE"
