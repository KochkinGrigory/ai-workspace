"""
Конфигурация для Bitrix24 Manager
"""
import os
from pathlib import Path


def load_env():
    """Загрузка переменных окружения из .env файла"""
    possible_paths = [
        Path(__file__).parent.parent.parent.parent / '.env',
        Path('/opt/ai-workspace/.env'),
        Path.cwd() / '.env',
    ]

    for env_path in possible_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
            break


load_env()

BITRIX24_WEBHOOK_URL = os.getenv('BITRIX24_WEBHOOK_URL', '')

if not BITRIX24_WEBHOOK_URL:
    raise ValueError(
        "BITRIX24_WEBHOOK_URL не установлен. "
        "См. references/setup.md для настройки."
    )

if not BITRIX24_WEBHOOK_URL.endswith('/'):
    BITRIX24_WEBHOOK_URL += '/'
