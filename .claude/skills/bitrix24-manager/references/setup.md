# Настройка Webhook для Bitrix24 Manager

## Шаг 1: Создание вебхука

1. Зайди в **Битрикс24**
2. Перейди в **Приложения** → **Вебхуки**
3. Нажми **Добавить вебхук** → **Входящий вебхук**

## Шаг 2: Права доступа (Scopes)

### Обязательные права:

| Scope | Назначение |
|-------|-----------|
| **task** | Задачи, комментарии, чеклисты |
| **calendar** | События, встречи |
| **im** | Чаты, уведомления |
| **disk** | Файлы |
| **user** | Информация о пользователях |
| **department** | Структура компании, отделы |
| **sonet_group** | Рабочие группы (проекты) |
| **bizproc** | Бизнес-процессы |
| **crm** | Смарт-процессы |

## Шаг 3: Добавление в .env

```bash
# /opt/ai-workspace/.env
BITRIX24_WEBHOOK_URL=https://your-portal.bitrix24.ru/rest/1/xxxxxxxxxxxxx/
```

## Шаг 4: Проверка

```python
from scripts import TasksManager
tasks = TasksManager()
print(tasks.list(limit=1))
```

## Troubleshooting

### BITRIX24_WEBHOOK_URL не установлен
- Проверь файл `.env`
- URL должен заканчиваться на `/`

### ACCESS_DENIED
- Проверь права (scopes) в вебхуке
- Пересоздай webhook с нужными правами

### QUERY_LIMIT_EXCEEDED
- Лимит запросов
- Используй batch запросы
