#!/bin/bash
#
# cleanup-tmp.sh - Очистка временных файлов
#
# Использование:
#   ./cleanup-tmp.sh [дней]   # По умолчанию 7 дней
#

TMP_DIR="/opt/ai-workspace/apps/telegram-bot/tmp"
DAYS_OLD=${1:-7}

echo "🧹 Очистка временных файлов..."
echo "Директория: $TMP_DIR"
echo "Удаляем файлы старше: $DAYS_OLD дней"
echo ""

# Показываем что будет удалено
FILES_TO_DELETE=$(find "$TMP_DIR" -type f -mtime +$DAYS_OLD 2>/dev/null)

if [ -z "$FILES_TO_DELETE" ]; then
    echo "✅ Старых файлов не найдено"
    exit 0
fi

echo "Файлы для удаления:"
echo "$FILES_TO_DELETE" | while read file; do
    SIZE=$(du -h "$file" | cut -f1)
    echo "  • $(basename "$file") ($SIZE)"
done
echo ""

# Удаляем
DELETED=$(find "$TMP_DIR" -type f -mtime +$DAYS_OLD -delete -print 2>/dev/null | wc -l)

if [ $DELETED -gt 0 ]; then
    echo "✅ Удалено файлов: $DELETED"
else
    echo "⚠️ Файлы не были удалены"
fi

# Показываем статистику
REMAINING=$(ls -1 "$TMP_DIR" 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$TMP_DIR" 2>/dev/null | cut -f1)

echo ""
echo "📊 Статистика:"
echo "  • Осталось файлов: $REMAINING"
echo "  • Общий размер: $TOTAL_SIZE"
