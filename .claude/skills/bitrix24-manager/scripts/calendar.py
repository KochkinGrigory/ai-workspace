"""
Операции с календарем Bitrix24 (11 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class CalendarManager:
    """Менеджер для работы с календарем Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== EVENTS CRUD ====================

    def create(
        self,
        name: str,
        from_time: str,
        to_time: str,
        type: str = 'user',
        owner_id: Optional[int] = None,
        description: Optional[str] = None,
        attendees: Optional[List[int]] = None,
        **kwargs
    ) -> int:
        """
        Создать событие в календаре

        Args:
            name: Название события
            from_time: Начало (формат: 2024-12-20T14:00:00)
            to_time: Окончание (формат: 2024-12-20T15:00:00)
            type: Тип календаря ('user', 'group', 'company_calendar')
            owner_id: ID владельца календаря
            description: Описание
            attendees: Список ID участников

        Returns:
            ID созданного события
        """
        params = {'type': type, 'name': name, 'from': from_time, 'to': to_time}
        if owner_id:
            params['ownerId'] = owner_id
        if description:
            params['description'] = description
        if attendees:
            params['attendees'] = attendees
        params.update(kwargs)

        return self.client.call('calendar.event.add', params)

    def get(self, event_id: int) -> Dict[str, Any]:
        """
        Получить событие по ID

        Note: Использует calendar.event.getbyid (не calendar.event.get)
        """
        return self.client.call('calendar.event.getbyid', {'id': event_id})

    def update(
        self,
        event_id: int,
        type: str = 'user',
        owner_id: int = None,
        **params
    ) -> int:
        """
        Обновить событие

        Args:
            event_id: ID события
            type: Тип календаря (обязательно!)
            owner_id: ID владельца календаря (обязательно!)
            **params: name, from, to, description и т.д.
        """
        update_params = {
            'id': event_id,
            'type': type,
            'ownerId': owner_id if owner_id is not None else 1,
        }
        update_params.update(params)

        return self.client.call('calendar.event.update', update_params)

    def delete(self, event_id: int) -> bool:
        """Удалить событие"""
        return self.client.call('calendar.event.delete', {'id': event_id})

    def list(
        self,
        type: str = 'user',
        owner_id: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Получить список событий за период"""
        params = {'type': type}
        if owner_id:
            params['ownerId'] = owner_id
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date

        result = self.client.call('calendar.event.get', params)
        if isinstance(result, list):
            return result
        return [result] if result else []

    def get_nearest(
        self,
        type: str = 'user',
        owner_id: Optional[int] = None,
        days: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Получить ближайшие события

        Args:
            type: Тип календаря
            owner_id: ID владельца
            days: Количество дней вперёд (макс 60)
        """
        params = {'type': type, 'days': min(days, 60)}
        if owner_id:
            params['ownerId'] = owner_id

        result = self.client.call('calendar.event.get.nearest', params)
        return result if isinstance(result, list) else []

    # ==================== SECTIONS (CALENDARS) ====================

    def get_sections(
        self,
        type: str = 'user',
        owner_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список календарей (секций)

        Args:
            type: Тип ('user', 'group', 'company_calendar')
            owner_id: ID владельца
        """
        params = {'type': type}
        if owner_id:
            params['ownerId'] = owner_id

        result = self.client.call('calendar.section.get', params)
        return result if isinstance(result, list) else []

    def create_section(
        self,
        name: str,
        type: str = 'user',
        owner_id: Optional[int] = None,
        color: Optional[str] = None,
        description: Optional[str] = None
    ) -> int:
        """
        Создать календарь (секцию)

        Args:
            name: Название календаря
            type: Тип
            owner_id: ID владельца
            color: Цвет (#FF0000)
            description: Описание

        Returns:
            ID созданного календаря
        """
        params = {'type': type, 'name': name}
        if owner_id:
            params['ownerId'] = owner_id
        if color:
            params['color'] = color
        if description:
            params['description'] = description

        return self.client.call('calendar.section.add', params)

    def delete_section(self, section_id: int) -> bool:
        """Удалить календарь (секцию)"""
        return self.client.call('calendar.section.delete', {'id': section_id})

    # ==================== MEETING STATUS ====================

    def set_meeting_status(self, event_id: int, status: str) -> bool:
        """
        Установить статус участия во встрече

        Args:
            event_id: ID события
            status: 'Y' (приму), 'N' (отклоню), 'Q' (под вопросом)
        """
        return self.client.call('calendar.meeting.status.set', {
            'eventId': event_id,
            'status': status
        })

    def get_meeting_status(self, event_id: int) -> Dict[str, Any]:
        """Получить статус участия во встрече"""
        return self.client.call('calendar.meeting.status.get', {'eventId': event_id})

    # ==================== SETTINGS & ACCESSIBILITY ====================

    def get_settings(self) -> Dict[str, Any]:
        """Получить настройки календаря пользователя"""
        return self.client.call('calendar.settings.get')

    def get_accessibility(
        self,
        users: List[int],
        from_date: str,
        to_date: str
    ) -> Dict[str, Any]:
        """
        Получить занятость пользователей

        Args:
            users: Список ID пользователей
            from_date: Начало периода
            to_date: Конец периода

        Returns:
            Занятость по пользователям
        """
        return self.client.call('calendar.accessibility.get', {
            'users': users,
            'from': from_date,
            'to': to_date
        })
