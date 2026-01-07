#!/bin/bash
#
# tg-session-send.sh - Отправка сообщений в Telegram из Claude Code сессии
#
# Назначение:
#   Wrapper для tg-send.sh который автоматически завершает процесс Claude
#   после отправки сообщения. Используется в Telegram Agent режиме для
#   управления сессиями через --resume.
#
# Как работает:
#   1. Вызывает tg-send.sh с переданными параметрами
#   2. Завершает текущий процесс Claude с exit 0
#   3. Session ID остаётся в active_session.txt для последующего resume
#
# Использование:
#   /tg "текст сообщения"        # Отправить текст
#   /tg-file путь "описание"     # Отправить файл
#
# Примеры:
#   /tg "✅ <b>Готово!</b> Результаты в файле ⬇️"
#   /tg-file /tmp/report.xlsx "Отчёт по продажам"
#

# Вызываем существующий tg-send.sh с всеми переданными аргументами
/opt/ai-workspace/commands/tg-send.sh "$@"

# Запоминаем exit code
EXIT_CODE=$?

# Завершаем процесс Claude
# Session ID остаётся в active_session.txt
# Следующее сообщение от пользователя сделает --resume
exit $EXIT_CODE
