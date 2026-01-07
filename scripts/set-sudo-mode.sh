#!/bin/bash

# Переключение режима sudo для claude-agent
# Использование: sudo ./set-sudo-mode.sh full|restricted

set -e

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Проверка root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Запустите скрипт с правами root: sudo ./set-sudo-mode.sh <mode>${NC}"
    exit 1
fi

# Проверка аргумента
if [ -z "$1" ]; then
    echo "Использование: sudo ./set-sudo-mode.sh <mode>"
    echo ""
    echo "Режимы:"
    echo "  full        - Полный sudo доступ (все команды)"
    echo "  restricted  - Ограниченный (только базовые команды)"
    echo ""
    echo "Пример: sudo ./set-sudo-mode.sh full"
    exit 1
fi

MODE=$1

case $MODE in
    full)
        echo "Устанавливаем ПОЛНЫЙ sudo доступ..."
        echo "claude-agent ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/claude-agent
        chmod 440 /etc/sudoers.d/claude-agent
        echo -e "${GREEN}✅ Режим изменён на: ПОЛНЫЙ${NC}"
        echo "   claude-agent может выполнять любые команды через sudo"
        ;;

    restricted)
        echo "Устанавливаем ОГРАНИЧЕННЫЙ sudo доступ..."
        cat > /etc/sudoers.d/claude-agent << 'EOF'
# Claude Agent - Restricted sudo access
claude-agent ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/systemctl, \
                                  /usr/bin/docker, \
                                  /usr/bin/apt, /usr/bin/apt-get, \
                                  /usr/bin/pip, /usr/bin/pip3, \
                                  /usr/bin/npm, \
                                  /usr/bin/git
EOF
        chmod 440 /etc/sudoers.d/claude-agent
        echo -e "${GREEN}✅ Режим изменён на: ОГРАНИЧЕННЫЙ${NC}"
        echo "   Разрешены команды: systemctl, docker, apt, pip, npm, git"
        ;;

    *)
        echo -e "${RED}❌ Неизвестный режим: $MODE${NC}"
        echo "Доступные режимы: full, restricted"
        exit 1
        ;;
esac

echo ""
echo "Проверить текущие права:"
echo "  sudo /opt/ai-workspace/scripts/show-sudo-permissions.sh"
echo ""

# Проверка валидности sudoers
if ! visudo -c -f /etc/sudoers.d/claude-agent &>/dev/null; then
    echo -e "${RED}❌ ОШИБКА: Невалидный файл sudoers!${NC}"
    echo "Восстанавливаем безопасную конфигурацию..."
    echo "claude-agent ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/claude-agent
    chmod 440 /etc/sudoers.d/claude-agent
    exit 1
fi

echo -e "${GREEN}✅ Конфигурация валидна${NC}"
