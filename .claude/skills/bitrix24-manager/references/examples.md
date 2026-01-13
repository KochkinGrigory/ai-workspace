# Примеры использования

## Быстрый старт

```python
from scripts import (
    TasksManager, CalendarManager, MessengerManager,
    UsersManager, DiskManager, DepartmentsManager,
    WorkgroupsManager, BizprocManager, SmartProcessesManager
)

# Инициализация (автоматически берёт BITRIX24_WEBHOOK_URL из .env)
tasks = TasksManager()
calendar = CalendarManager()
messenger = MessengerManager()
users = UsersManager()
```

---

## Задачи (Tasks)

### Создание задачи

```python
task_id = tasks.create(
    title='Подготовить отчёт',
    responsible_id=1,
    description='Описание задачи',
    deadline='2026-01-15T18:00:00+03:00'
)
# Возвращает: {'task': {'id': '5160', ...}}
```

### Получение и фильтрация

```python
# Мои задачи (ответственный)
my_tasks = tasks.list(filter_params={'RESPONSIBLE_ID': 1}, limit=10)

# Задачи в работе
in_progress = tasks.list(filter_params={'STATUS': 3})

# Задачи с дедлайном на этой неделе
from datetime import datetime, timedelta
week_end = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%dT23:59:59')
urgent = tasks.list(filter_params={'<=DEADLINE': week_end})
```

### Смена статуса задачи

```python
# Статусы: 2=новая, 3=в работе, 4=ждёт контроля, 5=завершена, 6=отложена
tasks.start(task_id)      # Начать выполнение (2→3)
tasks.complete(task_id)   # Завершить (3→5)
tasks.defer(task_id)      # Отложить
tasks.renew(task_id)      # Возобновить

# ВАЖНО: не все переходы разрешены!
# Проверить доступные действия: tasks.get(task_id)['action']
```

### Комментарии к задаче

```python
# Добавить комментарий
comment_id = tasks.add_comment(task_id, 'Текст комментария')

# Получить комментарии
comments = tasks.get_comments(task_id)
```

### Чеклист

```python
from scripts.client import BitrixClient
client = BitrixClient()

# Создать пункт чеклиста (правильный метод!)
item_id = client.call('task.checklistitem.add', {
    'TASKID': task_id,
    'FIELDS': {'TITLE': 'Пункт чеклиста'}
})

# Получить чеклист
checklist = client.call('task.checklistitem.getlist', {'TASKID': task_id})

# Отметить выполненным
client.call('task.checklistitem.complete', {'TASKID': task_id, 'ITEMID': item_id})
```

---

## Календарь (Calendar)

### Создание события

```python
event_id = calendar.create(
    name='Встреча с клиентом',
    from_time='2026-01-10T14:00:00',
    to_time='2026-01-10T15:00:00',
    type='user',
    owner_id=1,
    description='Обсуждение проекта',
    attendees=[1, 458]  # ID участников
)
```

### Получение событий

```python
# Ближайшие события (до 60 дней)
events = calendar.get_nearest(type='user', owner_id=1, days=30)

# События за период
events = calendar.list(
    type='user',
    owner_id=1,
    from_date='2026-01-01',
    to_date='2026-01-31'
)

# Календари (секции) пользователя
sections = calendar.get_sections(type='user', owner_id=1)
```

### Проверка занятости

```python
# Занятость пользователей
accessibility = calendar.get_accessibility(
    users=[1, 458],
    from_date='2026-01-10',
    to_date='2026-01-10'
)
```

---

## Мессенджер (Messenger)

### Уведомления

```python
# Личное уведомление (колокольчик)
notify_id = messenger.notify(
    user_id=1,
    message='Важное уведомление!',
    tag='my_app'  # для группировки
)

# Системное уведомление
messenger.notify_system(user_id=1, message='Системное сообщение')
```

### Сообщения

```python
# Личное сообщение пользователю
msg_id = messenger.send_message(
    dialog_id='458',  # ID пользователя
    message='Привет! Как дела с проектом?'
)

# Сообщение в групповой чат
msg_id = messenger.send_message(
    dialog_id='chat123',  # chat + ID чата
    message='Всем привет!'
)
```

### Чаты

```python
# Создать групповой чат
chat_id = messenger.create_chat(
    title='Проект X',
    users=[1, 458],
    message='Чат для обсуждения проекта'
)

# Недавние чаты
recent = messenger.get_recent(limit=20)

# Счётчики непрочитанных
counters = messenger.get_counters()
```

---

## Пользователи (Users)

```python
# Текущий пользователь (от чьего имени webhook)
current = users.get_current()

# Поиск пользователей
found = users.search('Кочкин')

# Все активные сотрудники
active = users.get_active()

# Пользователи отдела
dept_users = users.get_by_department(department_id=1)

# Получить должность
user = users.get_by_id(458)
position = user.get('WORK_POSITION')  # Должность
```

---

## Batch-запросы (оптимизация)

Выполнение нескольких запросов за один вызов:

```python
from scripts.client import BitrixClient
client = BitrixClient()

result = client.call('batch', {
    'halt': 0,  # 0=продолжать при ошибках, 1=остановиться
    'cmd': {
        'user': 'user.current',
        'tasks': 'tasks.task.list?filter[RESPONSIBLE_ID]=1&limit=5',
        'events': 'calendar.event.get.nearest?type=user&ownerId=1&days=7'
    }
})

# Результаты
user_data = result['result']['user']
tasks_data = result['result']['tasks']
events_data = result['result']['events']

# Ошибки (если были)
errors = result['result_error']
```

---

## Типичные сценарии

### Создать задачу с уведомлением

```python
# 1. Создать задачу
task = tasks.create(
    title='Срочно: проверить отчёт',
    responsible_id=458,  # Вячеслав
    deadline='2026-01-10T18:00:00+03:00'
)
task_id = task['task']['id']

# 2. Уведомить ответственного
messenger.notify(
    user_id=458,
    message=f'Вам назначена новая задача: [URL=/company/personal/user/1/tasks/task/view/{task_id}/]Проверить отчёт[/URL]'
)
```

### Найти свободное время для встречи

```python
# 1. Получить участников
participants = [1, 458]

# 2. Проверить занятость
accessibility = calendar.get_accessibility(
    users=participants,
    from_date='2026-01-10',
    to_date='2026-01-10'
)

# 3. Создать событие в свободный слот
event_id = calendar.create(
    name='Планёрка',
    from_time='2026-01-10T10:00:00',
    to_time='2026-01-10T11:00:00',
    attendees=participants
)
```

### Массовое обновление через batch

```python
# Завершить несколько задач за один запрос
task_ids = [100, 101, 102]
commands = {
    f'complete_{tid}': f'tasks.task.complete?taskId={tid}'
    for tid in task_ids
}

result = client.call('batch', {'halt': 0, 'cmd': commands})
```
