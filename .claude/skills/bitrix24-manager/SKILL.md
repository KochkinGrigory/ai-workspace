---
name: bitrix24-manager
description: "Управление Bitrix24 через REST API (138 методов) - задачи, календарь, мессенджер, пользователи, файлы, отделы, рабочие группы, бизнес-процессы, смарт-процессы. ИСПОЛЬЗОВАТЬ КОГДА - создать задачу в битрикс, отправить уведомление, написать в чат, создать встречу, найти сотрудника, загрузить файл, запустить бизнес-процесс, создать элемент смарт-процесса. Триггеры - задача битрикс, уведомление битрикс, событие календарь, чат битрикс."
---

# Bitrix24 Manager

Skill для работы с Bitrix24 через REST API (webhook).

## Когда использовать

- Создание/обновление задач в Bitrix24
- Отправка уведомлений и сообщений сотрудникам
- Работа с календарём (события, встречи)
- Поиск информации о пользователях и отделах
- Управление файлами на диске
- Работа со смарт-процессами
- Запуск бизнес-процессов

## Быстрый старт

```python
from scripts import TasksManager, MessengerManager, UsersManager

tasks = TasksManager()
messenger = MessengerManager()
users = UsersManager()

# Создать задачу
tasks.create(title='Новая задача', responsible_id=1)

# Отправить уведомление
messenger.notify(user_id=1, message='Важное уведомление!')

# Найти пользователя
found = users.search('Иванов')
```

## Выбор модуля

| Задача | Модуль | Пример |
|--------|--------|--------|
| Задачи, комментарии, чеклисты | `TasksManager` | `tasks.create()` |
| События, встречи | `CalendarManager` | `calendar.create()` |
| Уведомления, сообщения | `MessengerManager` | `messenger.notify()` |
| Информация о сотрудниках | `UsersManager` | `users.search()` |
| Файлы и папки | `DiskManager` | `disk.get_file()` |
| Структура компании | `DepartmentsManager` | `departments.get()` |
| Рабочие группы | `WorkgroupsManager` | `workgroups.list()` |
| Бизнес-процессы | `BizprocManager` | `bizproc.start()` |
| Смарт-процессы | `SmartProcessesManager` | `smart.get_items()` |

## Инструкции

### 1. Найти пользователя перед операцией

```python
users = UsersManager()
found = users.search('Кочкин')
user_id = found[0]['ID'] if found else None
```

### 2. Проверять доступные действия для задач

```python
task = tasks.get(task_id)
if task.get('action', {}).get('complete'):
    tasks.complete(task_id)
```

### 3. Использовать batch для массовых операций

```python
from scripts.client import BitrixClient
client = BitrixClient()
result = client.call('batch', {
    'halt': 0,
    'cmd': {'task1': 'tasks.task.complete?taskId=100', ...}
})
```

### 4. Обрабатывать пустые результаты

```python
result = tasks.get(task_id)
if not result or result == []:
    print('Задача не найдена')
```

## Важные особенности

- **Чеклист задач:** метод `task.checklistitem.add` (не `tasks.task.checklist.add`)
- **Статусы задач:** 2=новая, 3=в работе, 5=завершена, 6=отложена
- **Формат дат:** ISO 8601 `2026-01-15T14:30:00+03:00`
- **dialog_id:** `"123"` для личного, `"chat456"` для группового чата
- **Лимит:** 2 запроса/сек, использовать batch для массовых операций

## Документация

| Файл | Содержимое |
|------|------------|
| [examples.md](references/examples.md) | Примеры кода и типичные сценарии |
| [errors.md](references/errors.md) | Ошибки и их решения |
| [api-quick-ref.md](references/api-quick-ref.md) | Справочник методов API |
| [setup.md](references/setup.md) | Настройка webhook |

## Конфигурация

Требуется webhook URL в `/opt/ai-workspace/.env`:

```
BITRIX24_WEBHOOK_URL=https://your-portal.bitrix24.ru/rest/1/xxxxx/
```

## Модули

| Модуль | Методов | Описание |
|--------|---------|----------|
| **tasks** | 24 | Задачи, статусы, комментарии, чеклисты |
| **calendar** | 13 | События, секции, встречи, доступность |
| **messenger** | 20 | Уведомления, сообщения, чаты |
| **users** | 15 | Пользователи, поиск, должности |
| **disk** | 14 | Хранилища, папки, файлы |
| **departments** | 8 | Структура компании, отделы |
| **workgroups** | 15 | Рабочие группы, проекты |
| **bizproc** | 11 | Бизнес-процессы, шаблоны |
| **smart_processes** | 18 | Смарт-процессы, элементы, стадии |

**Итого: 138 методов**
