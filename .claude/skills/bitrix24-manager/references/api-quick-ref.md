# API Quick Reference

## Формат вызова

```python
from scripts.client import BitrixClient
client = BitrixClient()
result = client.call('method.name', {'param': 'value'})
```

---

## Tasks (tasks.py)

| Метод | API | Описание |
|-------|-----|----------|
| `create()` | `tasks.task.add` | Создать задачу |
| `get()` | `tasks.task.get` | Получить задачу |
| `update()` | `tasks.task.update` | Обновить задачу |
| `delete()` | `tasks.task.delete` | Удалить задачу |
| `list()` | `tasks.task.list` | Список задач |
| `start()` | `tasks.task.start` | Начать выполнение |
| `complete()` | `tasks.task.complete` | Завершить |
| `defer()` | `tasks.task.defer` | Отложить |
| `renew()` | `tasks.task.renew` | Возобновить |
| `add_comment()` | `task.commentitem.add` | Добавить комментарий |
| `get_comments()` | `task.commentitem.getlist` | Получить комментарии |

### Статусы задач

| Код | Статус | Допустимые переходы |
|-----|--------|---------------------|
| 2 | Новая | → start → 3 |
| 3 | В работе | → complete → 5, pause |
| 4 | Ожидает контроля | → approve → 5, disapprove → 3 |
| 5 | Завершена | → renew → 2 |
| 6 | Отложена | → renew → 2 |

### Чеклист (отдельные методы!)

| API метод | Описание |
|-----------|----------|
| `task.checklistitem.add` | Добавить пункт |
| `task.checklistitem.getlist` | Получить список |
| `task.checklistitem.complete` | Отметить выполненным |
| `task.checklistitem.delete` | Удалить пункт |

---

## Calendar (calendar.py)

| Метод | API | Описание |
|-------|-----|----------|
| `create()` | `calendar.event.add` | Создать событие |
| `get()` | `calendar.event.getbyid` | Получить по ID |
| `update()` | `calendar.event.update` | Обновить |
| `delete()` | `calendar.event.delete` | Удалить |
| `list()` | `calendar.event.get` | События за период |
| `get_nearest()` | `calendar.event.get.nearest` | Ближайшие события |
| `get_sections()` | `calendar.section.get` | Календари (секции) |
| `get_accessibility()` | `calendar.accessibility.get` | Занятость пользователей |

### Типы календарей

| Тип | Описание |
|-----|----------|
| `user` | Личный календарь пользователя |
| `group` | Календарь рабочей группы |
| `company_calendar` | Общий календарь компании |

---

## Messenger (messenger.py)

| Метод | API | Описание |
|-------|-----|----------|
| `notify()` | `im.notify.personal.add` | Личное уведомление |
| `notify_system()` | `im.notify.system.add` | Системное уведомление |
| `send_message()` | `im.message.add` | Отправить сообщение |
| `update_message()` | `im.message.update` | Редактировать |
| `delete_message()` | `im.message.delete` | Удалить |
| `get_messages()` | `im.dialog.messages.get` | История сообщений |
| `create_chat()` | `im.chat.add` | Создать чат |
| `get_recent()` | `im.recent.list` | Недавние чаты |
| `get_counters()` | `im.counters.get` | Счётчики непрочитанных |

### Формат dialog_id

| Формат | Описание |
|--------|----------|
| `123` | Личный диалог с пользователем ID=123 |
| `chat456` | Групповой чат ID=456 |

---

## Users (users.py)

| Метод | API | Описание |
|-------|-----|----------|
| `get_current()` | `user.current` | Текущий пользователь |
| `get()` | `user.get` | Получить пользователей |
| `search()` | `user.search` | Поиск по имени/email |
| `get_by_id()` | `user.get` | По ID |
| `get_active()` | `user.get` | Активные сотрудники |
| `add()` | `user.add` | Создать пользователя |
| `update()` | `user.update` | Обновить |

### Ключевые поля пользователя

| Поле | Описание |
|------|----------|
| `ID` | Идентификатор |
| `NAME`, `LAST_NAME` | Имя, Фамилия |
| `EMAIL` | Email |
| `WORK_POSITION` | Должность |
| `UF_DEPARTMENT` | ID отделов (массив) |
| `ACTIVE` | Активен (true/false) |

---

## Departments (departments.py)

| Метод | API | Описание |
|-------|-----|----------|
| `get()` | `department.get` | Получить отделы |
| `get_root()` | `department.get` | Корневые отделы |
| `get_children()` | `department.get` | Дочерние отделы |
| `add()` | `department.add` | Создать отдел |
| `update()` | `department.update` | Обновить |
| `delete()` | `department.delete` | Удалить |

---

## Workgroups (workgroups.py)

| Метод | API | Описание |
|-------|-----|----------|
| `create()` | `sonet_group.create` | Создать группу |
| `get()` | `sonet_group.get` | Получить по ID |
| `list()` | `sonet_group.get` | Список групп |
| `update()` | `sonet_group.update` | Обновить |
| `delete()` | `sonet_group.delete` | Удалить |
| `get_members()` | `sonet_group.user.get` | Участники |
| `add_member()` | `sonet_group.user.add` | Добавить участника |
| `remove_member()` | `sonet_group.user.delete` | Удалить участника |

---

## Disk (disk.py)

| Метод | API | Описание |
|-------|-----|----------|
| `get_storages()` | `disk.storage.getlist` | Список хранилищ |
| `get_folder()` | `disk.folder.get` | Получить папку |
| `create_folder()` | `disk.folder.addsubfolder` | Создать папку |
| `get_file()` | `disk.file.get` | Получить файл |
| `delete_file()` | `disk.file.delete` | Удалить файл |
| `move_file()` | `disk.file.moveto` | Переместить |
| `get_download_url()` | `disk.file.get` | URL скачивания |

---

## Smart Processes (smart_processes.py)

| Метод | API | Описание |
|-------|-----|----------|
| `get_types()` | `crm.type.list` | Список смарт-процессов |
| `get_type()` | `crm.type.get` | Получить по ID |
| `add_type()` | `crm.type.add` | Создать смарт-процесс |
| `get_items()` | `crm.item.list` | Элементы процесса |
| `get_item()` | `crm.item.get` | Элемент по ID |
| `add_item()` | `crm.item.add` | Создать элемент |
| `update_item()` | `crm.item.update` | Обновить |
| `delete_item()` | `crm.item.delete` | Удалить |
| `get_stages()` | `crm.status.list` | Стадии |
| `move_to_stage()` | `crm.item.update` | Переместить на стадию |

---

## Bizproc (bizproc.py)

| Метод | API | Описание |
|-------|-----|----------|
| `start()` | `bizproc.workflow.start` | Запустить БП |
| `terminate()` | `bizproc.workflow.terminate` | Остановить |
| `kill()` | `bizproc.workflow.kill` | Принудительно удалить |
| `get_instances()` | `bizproc.workflow.instances` | Запущенные процессы |
| `get_templates()` | `bizproc.workflow.template.list` | Шаблоны БП |

---

## Batch (оптимизация)

```python
result = client.call('batch', {
    'halt': 0,  # 0=продолжать при ошибках
    'cmd': {
        'name1': 'method1?param=value',
        'name2': 'method2?param=value'
    }
})

# Результат
result['result']['name1']  # Данные
result['result_error']     # Ошибки
```

---

## Форматы данных

### Дата и время

```python
# ISO 8601 с timezone (рекомендуется)
'2026-01-15T14:30:00+03:00'

# Только дата
'2026-01-15'
```

### Фильтры

```python
# Точное совпадение
{'STATUS': 5}

# Сравнение
{'>=DEADLINE': '2026-01-01'}
{'<=DEADLINE': '2026-01-31'}

# Поиск по подстроке
{'%NAME': 'отчёт'}
```

### Boolean в API

```python
# Некоторые методы принимают
'Y' / 'N'

# Другие принимают
True / False
```
