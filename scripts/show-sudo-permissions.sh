#!/bin/bash

# Показывает текущие sudo права пользователя claude-agent

# Цвета
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Claude Agent - Sudo права${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Проверка существования пользователя
if ! id -u claude-agent &>/dev/null; then
    echo -e "${RED}❌ Пользователь claude-agent не существует${NC}"
    exit 1
fi

# Проверка файла sudoers
if [ ! -f "/etc/sudoers.d/claude-agent" ]; then
    echo -e "${RED}❌ Файл /etc/sudoers.d/claude-agent не найден${NC}"
    exit 1
fi

echo "Пользователь: claude-agent"
echo "UID: $(id -u claude-agent)"
echo "GID: $(id -g claude-agent)"
echo "Группы: $(id -Gn claude-agent)"
echo ""

echo "Sudo права:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat /etc/sudoers.d/claude-agent
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Определение режима
if grep -q "ALL=(ALL) NOPASSWD: ALL" /etc/sudoers.d/claude-agent; then
    echo -e "${GREEN}✅ Режим: ПОЛНЫЙ ДОСТУП${NC}"
    echo "   claude-agent может выполнять любые команды через sudo"
elif grep -q "NOPASSWD:" /etc/sudoers.d/claude-agent; then
    echo -e "${GREEN}✅ Режим: ОГРАНИЧЕННЫЙ${NC}"
    echo "   Разрешены только указанные команды"
else
    echo -e "${RED}⚠️  Неизвестная конфигурация${NC}"
fi

echo ""
