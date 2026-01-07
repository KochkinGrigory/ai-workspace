#!/bin/bash

# Добавляет команду в список разрешенных sudo для claude-agent
# Использование: sudo ./add-sudo-command.sh /path/to/command

set -e

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Проверка root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Запустите скрипт с правами root${NC}"
    exit 1
fi

# Проверка аргумента
if [ -z "$1" ]; then
    echo "Использование: sudo ./add-sudo-command.sh <command_path>"
    echo ""
    echo "Примеры:"
    echo "  sudo ./add-sudo-command.sh /usr/bin/certbot"
    echo "  sudo ./add-sudo-command.sh /usr/bin/nginx"
    echo ""
    exit 1
fi

COMMAND=$1

# Проверка что команда существует
if [ ! -f "$COMMAND" ] && [ ! -L "$COMMAND" ]; then
    echo -e "${YELLOW}⚠️  Предупреждение: Файл $COMMAND не найден${NC}"
    read -p "Добавить всё равно? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        exit 0
    fi
fi

# Проверка текущего режима
if grep -q "ALL=(ALL) NOPASSWD: ALL" /etc/sudoers.d/claude-agent 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Текущий режим: ПОЛНЫЙ ДОСТУП${NC}"
    echo "   claude-agent уже может выполнять все команды через sudo"
    echo "   Добавление отдельной команды не имеет смысла"
    echo ""
    read -p "Переключиться на ОГРАНИЧЕННЫЙ режим? (y/n): " switch_mode
    if [ "$switch_mode" = "y" ]; then
        # Создаём restricted конфигурацию с этой командой
        cat > /etc/sudoers.d/claude-agent << EOF
# Claude Agent - Restricted sudo access
claude-agent ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/systemctl, \
                                  /usr/bin/docker, \
                                  $COMMAND
EOF
        chmod 440 /etc/sudoers.d/claude-agent
        echo -e "${GREEN}✅ Переключено на ОГРАНИЧЕННЫЙ режим${NC}"
        echo -e "${GREEN}✅ Команда добавлена: $COMMAND${NC}"
    fi
    exit 0
fi

# Добавление команды в существующий список
if [ -f "/etc/sudoers.d/claude-agent" ]; then
    # Проверка что команда уже есть
    if grep -q "$COMMAND" /etc/sudoers.d/claude-agent; then
        echo -e "${YELLOW}⚠️  Команда уже в списке: $COMMAND${NC}"
        exit 0
    fi

    # Добавляем команду в конец списка через продолжение строки
    sed -i "$ s|$|, \\\\\\n                                  $COMMAND|" /etc/sudoers.d/claude-agent

    echo -e "${GREEN}✅ Команда добавлена: $COMMAND${NC}"
else
    echo -e "${RED}❌ Файл /etc/sudoers.d/claude-agent не найден${NC}"
    exit 1
fi

# Проверка валидности
if ! visudo -c -f /etc/sudoers.d/claude-agent &>/dev/null; then
    echo -e "${RED}❌ ОШИБКА: Невалидный файл sudoers!${NC}"
    echo "Откатываем изменения..."
    git checkout /etc/sudoers.d/claude-agent 2>/dev/null || \
        echo "claude-agent ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/claude-agent
    exit 1
fi

echo ""
echo "Текущие разрешенные команды:"
grep "NOPASSWD:" /etc/sudoers.d/claude-agent
echo ""
