"""
Операции с рабочими группами (проектами) Bitrix24 (15 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class WorkgroupsManager:
    """Менеджер для работы с рабочими группами Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== GROUPS CRUD ====================

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        visible: bool = True,
        opened: bool = True,
        project: bool = False,
        subject_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        keywords: Optional[str] = None,
        **kwargs
    ) -> int:
        """
        Создать рабочую группу

        Args:
            name: Название группы
            description: Описание
            visible: Видимость в списке групп
            opened: Открытая группа (можно вступить без приглашения)
            project: Это проект (не группа)
            subject_id: ID темы группы
            owner_id: ID владельца
            keywords: Ключевые слова

        Returns:
            ID созданной группы
        """
        params = {
            'NAME': name,
            'VISIBLE': 'Y' if visible else 'N',
            'OPENED': 'Y' if opened else 'N',
            'PROJECT': 'Y' if project else 'N',
        }

        if description:
            params['DESCRIPTION'] = description
        if subject_id:
            params['SUBJECT_ID'] = subject_id
        if owner_id:
            params['OWNER_ID'] = owner_id
        if keywords:
            params['KEYWORDS'] = keywords

        params.update(kwargs)

        return self.client.call('sonet_group.create', params)

    def get(self, group_id: int) -> Dict[str, Any]:
        """Получить группу по ID"""
        result = self.client.call('sonet_group.get', {'FILTER': {'ID': group_id}})
        if isinstance(result, list) and result:
            return result[0]
        elif isinstance(result, dict):
            return result.get(str(group_id), {})
        return {}

    def list(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        order: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список групп

        Args:
            filter_params: Фильтры (OWNER_ID, VISIBLE, OPENED и др.)
            order: Сортировка {'ID': 'DESC'}

        Примеры filter_params:
            {'VISIBLE': 'Y'} - только видимые
            {'PROJECT': 'Y'} - только проекты
            {'OWNER_ID': 1} - группы пользователя
        """
        params = {}
        if filter_params:
            params['FILTER'] = filter_params
        if order:
            params['ORDER'] = order

        result = self.client.call('sonet_group.get', params)
        if isinstance(result, dict):
            return list(result.values())
        return result if isinstance(result, list) else []

    def update(self, group_id: int, **fields) -> bool:
        """
        Обновить группу

        Args:
            group_id: ID группы
            **fields: Поля (NAME, DESCRIPTION, VISIBLE, OPENED и др.)
        """
        fields['GROUP_ID'] = group_id
        return self.client.call('sonet_group.update', fields)

    def delete(self, group_id: int) -> bool:
        """Удалить группу"""
        return self.client.call('sonet_group.delete', {'GROUP_ID': group_id})

    def set_owner(self, group_id: int, user_id: int) -> bool:
        """Сменить владельца группы"""
        return self.client.call('sonet_group.setowner', {
            'GROUP_ID': group_id,
            'USER_ID': user_id
        })

    def get_features(self, group_id: int) -> Dict[str, Any]:
        """Получить доступ к функциям группы"""
        return self.client.call('sonet_group.feature.access', {'GROUP_ID': group_id})

    # ==================== MEMBERS ====================

    def get_members(
        self,
        group_id: int,
        role: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить участников группы

        Args:
            group_id: ID группы
            role: Фильтр по роли (A=owner, E=moderator, K=member, etc.)
        """
        params = {'ID': group_id}
        if role:
            params['ROLE'] = role

        result = self.client.call('sonet_group.user.get', params)
        return result if isinstance(result, list) else []

    def add_member(
        self,
        group_id: int,
        user_id: int,
        role: str = 'K',
        message: Optional[str] = None
    ) -> bool:
        """
        Добавить участника в группу

        Args:
            group_id: ID группы
            user_id: ID пользователя
            role: Роль (K=участник, E=модератор)
            message: Сообщение приглашения
        """
        params = {
            'GROUP_ID': group_id,
            'USER_ID': user_id,
            'ROLE': role,
        }
        if message:
            params['MESSAGE'] = message

        return self.client.call('sonet_group.user.add', params)

    def remove_member(self, group_id: int, user_id: int) -> bool:
        """Удалить участника из группы"""
        return self.client.call('sonet_group.user.delete', {
            'GROUP_ID': group_id,
            'USER_ID': user_id
        })

    def invite_member(
        self,
        group_id: int,
        user_id: int,
        message: Optional[str] = None
    ) -> bool:
        """
        Пригласить пользователя в группу

        Args:
            group_id: ID группы
            user_id: ID пользователя
            message: Текст приглашения
        """
        params = {'GROUP_ID': group_id, 'USER_ID': user_id}
        if message:
            params['MESSAGE'] = message

        return self.client.call('sonet_group.user.invite', params)

    def update_member(
        self,
        group_id: int,
        user_id: int,
        role: str
    ) -> bool:
        """
        Изменить роль участника

        Args:
            group_id: ID группы
            user_id: ID пользователя
            role: Новая роль (K=участник, E=модератор)
        """
        return self.client.call('sonet_group.user.update', {
            'GROUP_ID': group_id,
            'USER_ID': user_id,
            'ROLE': role
        })

    def request_membership(
        self,
        group_id: int,
        message: Optional[str] = None
    ) -> bool:
        """
        Запросить вступление в группу (от текущего пользователя)

        Args:
            group_id: ID группы
            message: Сообщение модераторам
        """
        params = {'GROUP_ID': group_id}
        if message:
            params['MESSAGE'] = message

        return self.client.call('sonet_group.user.request', params)

    def get_user_groups(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Получить группы пользователя

        Args:
            user_id: ID пользователя (None = текущий)
        """
        params = {}
        if user_id:
            params['USER_ID'] = user_id

        result = self.client.call('sonet_group.user.groups', params)
        return result if isinstance(result, list) else []

    # ==================== EXTENDED API ====================

    def list_extended(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Расширенный список групп (socialnetwork.api.workgroup.list)

        Args:
            filter_params: Фильтры
            select: Поля для выборки
        """
        params = {}
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select

        result = self.client.call('socialnetwork.api.workgroup.list', params)
        return result.get('workgroups', []) if isinstance(result, dict) else []

    def get_extended(self, group_id: int, select: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Расширенная информация о группе (socialnetwork.api.workgroup.get)

        Args:
            group_id: ID группы
            select: Поля для выборки
        """
        params = {'groupId': group_id}
        if select:
            params['select'] = select

        return self.client.call('socialnetwork.api.workgroup.get', params)
