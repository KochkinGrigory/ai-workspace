FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей:
# - Node.js (для Claude CLI)
# - sudo (для запуска от claude-agent)
# - postgresql-client (для доступа к БД)
# - procps (для команды ps, нужна Claude CLI)
# - docker.io (для docker команд из контейнера)
# - ffmpeg (для конвертации аудио .oga -> .mp3 для Whisper API)
RUN apt-get update && \
    apt-get install -y curl sudo postgresql-client procps docker.io ffmpeg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка docker-compose (standalone binary)
RUN curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Аргументы сборки для UID/GID (по умолчанию 5001)
ARG CLAUDE_UID=5001
ARG CLAUDE_GID=5001

# Создание claude-agent пользователя с тем же UID/GID что на хосте
# Добавляем в группу docker (создается автоматически пакетом docker.io) для доступа к docker.sock
RUN groupadd -g ${CLAUDE_GID} claude-agent && \
    useradd -r -u ${CLAUDE_UID} -g ${CLAUDE_GID} -G docker -s /bin/bash -d /home/claude-agent -m claude-agent && \
    echo "claude-agent ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/claude-agent && \
    chmod 440 /etc/sudoers.d/claude-agent

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходников
COPY src/ ./src/

# Создание директории для логов
RUN mkdir -p /app/logs

# Переменные окружения по умолчанию
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Запуск бота
CMD ["python", "src/bot.py"]
