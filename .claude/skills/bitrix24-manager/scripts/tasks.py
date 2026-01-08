"""
Операции с задачами Bitrix24 (18 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class TasksManager:
    """Менеджер для работы с задачами Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== TASKS CRUD ====================

    def create(
        self,
        title: str,
        responsible_id: int,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создать задачу

        Args:
            title: Название задачи
            responsible_id: ID ответственного
            description: Описание
            deadline: Дедлайн (формат: 2024-12-31T23:59:59+03:00)
        """
        fields = {'TITLE': title, 'RESPONSIBLE_ID': responsible_id}
        if description:
            fields['DESCRIPTION'] = description
        if deadline:
            fields['DEADLINE'] = deadline
        fields.update(kwargs)

        return self.client.call('tasks.task.add', {'fields': fields})

    def get(self, task_id: int) -> Dict[str, Any]:
        """Получить задачу по ID"""
        result = self.client.call('tasks.task.get', {'taskId': task_id})
        return result.get('task', {})

    def update(self, task_id: int, **fields) -> Dict[str, Any]:
        """Обновить задачу"""
        return self.client.call('tasks.task.update', {
            'taskId': task_id,
            'fields': fields
        })

    def delete(self, task_id: int) -> Dict[str, Any]:
        """Удалить задачу"""
        return self.client.call('tasks.task.delete', {'taskId': task_id})

    def list(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Получить список задач"""
        params = {}
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select
        if order:
            params['order'] = order
        params['limit'] = limit

        result = self.client.call('tasks.task.list', params)
        return result.get('tasks', [])

    # ==================== TASK STATUS ====================

    def complete(self, task_id: int) -> bool:
        """Завершить задачу"""
        return self.client.call('tasks.task.complete', {'taskId': task_id})

    def renew(self, task_id: int) -> bool:
        """Возобновить задачу (снять завершение)"""
        return self.client.call('tasks.task.renew', {'taskId': task_id})

    def defer(self, task_id: int) -> bool:
        """Отложить задачу"""
        return self.client.call('tasks.task.defer', {'taskId': task_id})

    def start(self, task_id: int) -> bool:
        """Начать выполнение задачи"""
        return self.client.call('tasks.task.start', {'taskId': task_id})

    def pause(self, task_id: int) -> bool:
        """Приостановить задачу"""
        return self.client.call('tasks.task.pause', {'taskId': task_id})

    def delegate(self, task_id: int, user_id: int) -> bool:
        """Делегировать задачу другому пользователю"""
        return self.client.call('tasks.task.delegate', {
            'taskId': task_id,
            'userId': user_id
        })

    def approve(self, task_id: int) -> bool:
        """Принять задачу (для задач с подтверждением)"""
        return self.client.call('tasks.task.approve', {'taskId': task_id})

    def disapprove(self, task_id: int) -> bool:
        """Отклонить задачу"""
        return self.client.call('tasks.task.disapprove', {'taskId': task_id})

    # ==================== COMMENTS ====================

    def add_comment(
        self,
        task_id: int,
        message: str,
        author_id: Optional[int] = None,
        files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Добавить комментарий к задаче

        Args:
            task_id: ID задачи
            message: Текст комментария
            author_id: ID автора (опционально)
            files: Список ID файлов с префиксом 'n' (['n123'])
        """
        fields = {'POST_MESSAGE': message}
        if author_id:
            fields['AUTHOR_ID'] = author_id
        if files:
            fields['UF_FORUM_MESSAGE_DOC'] = files

        return self.client.call('task.commentitem.add', {
            'TASKID': task_id,
            'FIELDS': fields
        })

    def get_comments(self, task_id: int) -> List[Dict[str, Any]]:
        """Получить список комментариев к задаче"""
        result = self.client.call('task.commentitem.getlist', {'TASKID': task_id})
        return result if isinstance(result, list) else []

    def delete_comment(self, task_id: int, comment_id: int) -> bool:
        """Удалить комментарий"""
        return self.client.call('task.commentitem.delete', {
            'TASKID': task_id,
            'ITEMID': comment_id
        })

    def update_comment(self, task_id: int, comment_id: int, message: str) -> bool:
        """Обновить комментарий"""
        return self.client.call('task.commentitem.update', {
            'TASKID': task_id,
            'ITEMID': comment_id,
            'FIELDS': {'POST_MESSAGE': message}
        })

    # ==================== CHECKLIST ====================
    # Правильный API: task.checklistitem.* (не tasks.task.checklist.*)

    def add_checklist_item(self, task_id: int, title: str, parent_id: int = 0) -> int:
        """
        Добавить пункт в чеклист задачи

        Args:
            task_id: ID задачи
            title: Текст пункта
            parent_id: ID родительского пункта (0 = создать группу чеклиста)

        Returns:
            ID созданного пункта
        """
        return self.client.call('task.checklistitem.add', {
            'TASKID': task_id,
            'FIELDS': {'TITLE': title, 'PARENT_ID': parent_id}
        })

    def get_checklist(self, task_id: int) -> List[Dict[str, Any]]:
        """Получить чеклист задачи"""
        result = self.client.call('task.checklistitem.getlist', {'TASKID': task_id})
        return result if isinstance(result, list) else []

    def complete_checklist_item(self, task_id: int, item_id: int) -> bool:
        """Отметить пункт чеклиста выполненным"""
        return self.client.call('task.checklistitem.complete', {
            'TASKID': task_id,
            'ITEMID': item_id
        })

    def renew_checklist_item(self, task_id: int, item_id: int) -> bool:
        """Снять отметку выполнения с пункта чеклиста"""
        return self.client.call('task.checklistitem.renew', {
            'TASKID': task_id,
            'ITEMID': item_id
        })

    def delete_checklist_item(self, task_id: int, item_id: int) -> bool:
        """Удалить пункт чеклиста"""
        return self.client.call('task.checklistitem.delete', {
            'TASKID': task_id,
            'ITEMID': item_id
        })

    def update_checklist_item(self, task_id: int, item_id: int, title: str) -> bool:
        """Обновить пункт чеклиста"""
        return self.client.call('task.checklistitem.update', {
            'TASKID': task_id,
            'ITEMID': item_id,
            'FIELDS': {'TITLE': title}
        })

    # ==================== FILES ====================

    def attach_file(self, task_id: int, file_id: int) -> bool:
        """Прикрепить файл к задаче"""
        return self.client.call('tasks.task.files.attach', {
            'taskId': task_id,
            'fileId': file_id
        })

    def get_files(self, task_id: int) -> List[Dict[str, Any]]:
        """Получить список файлов задачи"""
        result = self.client.call('tasks.task.getfiles', {'taskId': task_id})
        return result if isinstance(result, list) else []

    # ==================== CHAT (REST v3) ====================

    def send_chat_message(self, task_id: int, text: str) -> bool:
        """
        Отправить сообщение в чат задачи (REST v3 API)

        Note: REST v3 может быть недоступен (404). Используй add_comment() как fallback.
        """
        result = self.client.call_v3('tasks.task.chat.message.send', {
            'fields': {'taskId': task_id, 'text': text}
        })
        return result is True or result == {'result': True}
