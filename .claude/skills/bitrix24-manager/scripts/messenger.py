"""
Операции с мессенджером и уведомлениями Bitrix24 (20 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class MessengerManager:
    """Менеджер для работы с мессенджером Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== NOTIFICATIONS ====================

    def notify(
        self,
        user_id: int,
        message: str,
        tag: Optional[str] = None
    ) -> int:
        """
        Отправить личное уведомление пользователю

        Args:
            user_id: ID пользователя
            message: Текст уведомления
            tag: Тег для группировки

        Returns:
            ID уведомления
        """
        params = {'USER_ID': user_id, 'MESSAGE': message}
        if tag:
            params['TAG'] = tag

        return self.client.call('im.notify.personal.add', params)

    def notify_system(
        self,
        user_id: int,
        message: str,
        tag: Optional[str] = None
    ) -> int:
        """Отправить системное уведомление"""
        params = {'USER_ID': user_id, 'MESSAGE': message}
        if tag:
            params['TAG'] = tag

        return self.client.call('im.notify.system.add', params)

    def notify_delete(self, notification_id: int) -> bool:
        """Удалить уведомление"""
        return self.client.call('im.notify.delete', {'ID': notification_id})

    # ==================== MESSAGES ====================

    def send_message(
        self,
        dialog_id: str,
        message: str,
        system: bool = False,
        attach: Optional[List[Dict[str, Any]]] = None
    ) -> int:
        """
        Отправить сообщение в чат

        Args:
            dialog_id: chatXXX для группового чата, XXX для личного
            message: Текст (поддерживает BB-коды)
            system: Системное сообщение
            attach: Вложения (rich-контент)

        Returns:
            ID сообщения
        """
        params = {
            'DIALOG_ID': dialog_id,
            'MESSAGE': message,
            'SYSTEM': 'Y' if system else 'N'
        }
        if attach:
            params['ATTACH'] = attach

        return self.client.call('im.message.add', params)

    def update_message(self, message_id: int, message: str) -> bool:
        """Редактировать сообщение"""
        return self.client.call('im.message.update', {
            'MESSAGE_ID': message_id,
            'MESSAGE': message
        })

    def delete_message(self, message_id: int) -> bool:
        """Удалить сообщение"""
        return self.client.call('im.message.delete', {'MESSAGE_ID': message_id})

    def get_messages(
        self,
        dialog_id: str,
        limit: int = 20,
        last_id: Optional[int] = None,
        first_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить историю сообщений диалога

        Args:
            dialog_id: ID диалога (chatXXX или user_id)
            limit: Количество сообщений (макс 200)
            last_id: Получить сообщения до этого ID
            first_id: Получить сообщения после этого ID
        """
        params = {'DIALOG_ID': dialog_id, 'LIMIT': min(limit, 200)}
        if last_id:
            params['LAST_ID'] = last_id
        if first_id:
            params['FIRST_ID'] = first_id

        result = self.client.call('im.dialog.messages.get', params)
        return result.get('messages', []) if isinstance(result, dict) else []

    # ==================== CHATS ====================

    def create_chat(
        self,
        title: str,
        users: List[int],
        description: Optional[str] = None,
        message: Optional[str] = None,
        type: str = 'CHAT'
    ) -> int:
        """
        Создать групповой чат

        Args:
            title: Название чата
            users: Список ID пользователей
            description: Описание чата
            message: Первое сообщение
            type: CHAT (обычный), OPEN (открытый)

        Returns:
            ID созданного чата
        """
        params = {'TYPE': type, 'TITLE': title, 'USERS': users}
        if description:
            params['DESCRIPTION'] = description
        if message:
            params['MESSAGE'] = message

        return self.client.call('im.chat.add', params)

    def get_chat(self, chat_id: int) -> Dict[str, Any]:
        """Получить информацию о чате"""
        return self.client.call('im.chat.get', {'CHAT_ID': chat_id})

    def get_dialog(self, dialog_id: str) -> Dict[str, Any]:
        """Получить информацию о диалоге"""
        return self.client.call('im.dialog.get', {'DIALOG_ID': dialog_id})

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить список недавних чатов"""
        result = self.client.call('im.recent.list', {'LIMIT': min(limit, 200)})
        return result.get('items', []) if isinstance(result, dict) else result

    def get_counters(self) -> Dict[str, Any]:
        """Получить счётчики непрочитанных"""
        return self.client.call('im.counters.get')

    def update_chat_title(self, chat_id: int, title: str) -> bool:
        """Изменить название чата"""
        return self.client.call('im.chat.updateTitle', {
            'CHAT_ID': chat_id,
            'TITLE': title
        })

    def add_user_to_chat(self, chat_id: int, users: List[int]) -> bool:
        """Добавить пользователей в чат"""
        return self.client.call('im.chat.user.add', {
            'CHAT_ID': chat_id,
            'USERS': users
        })

    def remove_user_from_chat(self, chat_id: int, user_id: int) -> bool:
        """Удалить пользователя из чата"""
        return self.client.call('im.chat.user.delete', {
            'CHAT_ID': chat_id,
            'USER_ID': user_id
        })

    def get_chat_users(self, chat_id: int) -> List[Dict[str, Any]]:
        """Получить список пользователей чата"""
        return self.client.call('im.chat.user.list', {'CHAT_ID': chat_id})

    def leave_chat(self, chat_id: int) -> bool:
        """Покинуть чат"""
        return self.client.call('im.chat.leave', {'CHAT_ID': chat_id})

    # ==================== FILES ====================

    def send_file(
        self,
        chat_id: int,
        disk_id: Optional[int] = None,
        upload_id: Optional[str] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Отправить файл в чат

        Args:
            chat_id: ID чата
            disk_id: ID файла с диска
            upload_id: ID загруженного файла
            message: Описание файла
        """
        params = {'CHAT_ID': chat_id}
        if disk_id:
            params['DISK_ID'] = disk_id
        if upload_id:
            params['UPLOAD_ID'] = upload_id
        if message:
            params['MESSAGE'] = message

        return self.client.call('im.disk.file.commit', params)

    def delete_file(self, file_id: int) -> bool:
        """Удалить файл из чата"""
        return self.client.call('im.disk.file.delete', {'FILE_ID': file_id})

    def save_file_to_disk(self, file_id: int) -> Dict[str, Any]:
        """Сохранить файл из чата на диск"""
        return self.client.call('im.disk.file.save', {'FILE_ID': file_id})

    def get_chat_folder(self, chat_id: int) -> Dict[str, Any]:
        """Получить папку чата на диске"""
        return self.client.call('im.disk.folder.get', {'CHAT_ID': chat_id})
