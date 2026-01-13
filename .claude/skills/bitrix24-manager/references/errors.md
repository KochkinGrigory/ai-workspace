# Ошибки и их решения

## Типы ответов API

### Успешный ответ

```python
# Для методов возвращающих объект
{'task': {'id': '123', 'title': '...'}}

# Для методов возвращающих список
[{'id': '1', ...}, {'id': '2', ...}]

# Для методов возвращающих boolean
True
```

### Ошибка в ответе

```python
# API вернул ошибку в теле ответа
{
    'error': 'ERROR_CODE',
    'error_description': 'Описание ошибки'
}
```

### HTTP ошибки

| Код | Причина | Решение |
|-----|---------|---------|
| **400** | Неверные параметры | Проверить формат параметров |
| **401** | Неавторизован | Проверить webhook URL |
| **403** | Доступ запрещён | Проверить scopes webhook |
| **404** | Метод не найден | Проверить название метода |
| **500** | Ошибка сервера | Повторить позже |

---

## Частые ошибки

### ERROR: ACCESS_DENIED

**Причина:** Недостаточно прав в webhook

**Решение:**
1. Открыть настройки webhook в Bitrix24
2. Добавить необходимый scope (task, calendar, im, disk, user, crm и т.д.)
3. Пересоздать webhook если нельзя изменить

### ERROR: QUERY_LIMIT_EXCEEDED

**Причина:** Превышен лимит запросов (2 запроса/сек)

**Решение:**
```python
import time

def safe_call(client, method, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.call(method, params)
        except Exception as e:
            if 'QUERY_LIMIT' in str(e):
                time.sleep(1)  # Подождать 1 секунду
                continue
            raise
    raise Exception('Max retries exceeded')
```

**Лучше:** Использовать batch-запросы для массовых операций

### Пустой список вместо ошибки

**Ситуация:** Запрос несуществующей сущности возвращает `[]`

```python
# Задача не существует - вернёт []
result = client.call('tasks.task.get', {'taskId': 999999})
# result = []  (не ошибка!)

# Правильная проверка
task = tasks.get(task_id)
if not task or task == []:
    print('Задача не найдена')
```

### Неверный формат даты

**Ошибка:** `Invalid datetime format`

**Правильный формат:**
```python
# ISO 8601 с timezone
'2026-01-15T14:30:00+03:00'

# Без времени (для некоторых методов)
'2026-01-15'

# Генерация в Python
from datetime import datetime
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')
```

### Недоступное действие над задачей

**Ситуация:** Нельзя выполнить `defer` для задачи в статусе 3

```python
# Сначала проверить доступные действия
task = tasks.get(task_id)
actions = task.get('action', {})

if actions.get('defer'):
    tasks.defer(task_id)
else:
    print('Действие defer недоступно для этой задачи')
```

**Статусы задач и переходы:**
- 2 (новая) → start → 3
- 3 (в работе) → complete → 5, pause → 3
- 5 (завершена) → renew → 2
- 6 (отложена) → renew → 2

---

## Обработка ошибок в коде

### Базовая обработка

```python
from scripts.client import BitrixClient, BitrixAPIError

client = BitrixClient()

try:
    result = client.call('tasks.task.get', {'taskId': task_id})
except BitrixAPIError as e:
    if '404' in str(e):
        print('Метод не найден')
    elif '403' in str(e):
        print('Доступ запрещён')
    else:
        print(f'Ошибка API: {e}')
```

### Проверка результата

```python
def get_task_safe(task_id):
    """Безопасное получение задачи с проверкой"""
    result = client.call('tasks.task.get', {'taskId': task_id})

    # API может вернуть [] для несуществующей задачи
    if isinstance(result, list):
        return None

    # API может вернуть ошибку в теле
    if isinstance(result, dict) and 'error' in result:
        raise Exception(result.get('error_description', result['error']))

    return result.get('task', {})
```

---

## Лимиты API

| Параметр | Значение |
|----------|----------|
| Запросов в секунду | 2 |
| Запросов в batch | до 50 |
| Элементов в списке | обычно 50, макс 200 |
| Размер запроса | ~1MB |

### Работа с большими списками (пагинация)

```python
def get_all_tasks(filter_params=None):
    """Получить все задачи с пагинацией"""
    all_tasks = []
    start = 0

    while True:
        result = tasks.list(
            filter_params=filter_params,
            limit=50,
            start=start
        )

        if not result:
            break

        all_tasks.extend(result)

        # Проверяем есть ли ещё
        if len(result) < 50:
            break

        start += 50

    return all_tasks
```

---

## Отладка

### Логирование запросов

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# В client.py можно добавить:
# print(f'Calling: {method} with {params}')
# print(f'Response: {response.json()}')
```

### Проверка webhook

```python
from scripts import UsersManager

users = UsersManager()
try:
    current = users.get_current()
    print(f'Webhook работает от имени: {current.get("NAME")} {current.get("LAST_NAME")}')
except Exception as e:
    print(f'Ошибка webhook: {e}')
```
