"""
Операции с пользователями Bitrix24 (12 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class UsersManager:
    """Менеджер для работы с пользователями Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== USERS ====================

    def get_current(self) -> Dict[str, Any]:
        """Получить текущего пользователя (от чьего имени webhook)"""
        return self.client.call('user.current')

    def get(
        self,
        user_id: Optional[int] = None,
        filter_params: Optional[Dict[str, Any]] = None,
        sort: str = 'ID',
        order: str = 'ASC'
    ) -> List[Dict[str, Any]]:
        """
        Получить пользователей

        Args:
            user_id: ID конкретного пользователя
            filter_params: Фильтры (UF_DEPARTMENT, ACTIVE, USER_TYPE и др.)
            sort: Поле сортировки
            order: ASC или DESC

        Returns:
            Список пользователей

        Примеры filter_params:
            {'ACTIVE': True} - только активные
            {'UF_DEPARTMENT': 1} - из отдела 1
            {'USER_TYPE': 'employee'} - только сотрудники
            {'NAME_SEARCH': 'Иван'} - поиск по имени
        """
        params = {'SORT': sort, 'ORDER': order}

        if user_id:
            params['ID'] = user_id
        if filter_params:
            params.update(filter_params)

        result = self.client.call('user.get', params)
        return result if isinstance(result, list) else []

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить пользователя по ID"""
        result = self.get(user_id=user_id)
        return result[0] if result else None

    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Поиск пользователей по имени/email

        Args:
            query: Строка поиска
        """
        result = self.client.call('user.search', {'FIND': query})
        return result if isinstance(result, list) else []

    def get_by_department(self, department_id: int) -> List[Dict[str, Any]]:
        """Получить пользователей отдела"""
        return self.get(filter_params={'UF_DEPARTMENT': department_id})

    def get_active(self) -> List[Dict[str, Any]]:
        """Получить только активных пользователей"""
        return self.get(filter_params={'ACTIVE': True, 'USER_TYPE': 'employee'})

    def get_online(self) -> List[Dict[str, Any]]:
        """Получить онлайн пользователей"""
        return self.get(filter_params={'IS_ONLINE': 'Y'})

    def add(
        self,
        email: str,
        name: str,
        last_name: str,
        password: Optional[str] = None,
        work_position: Optional[str] = None,
        uf_department: Optional[List[int]] = None,
        **kwargs
    ) -> int:
        """
        Создать пользователя

        Args:
            email: Email (обязательно)
            name: Имя
            last_name: Фамилия
            password: Пароль
            work_position: Должность
            uf_department: Список ID отделов

        Returns:
            ID созданного пользователя
        """
        params = {
            'EMAIL': email,
            'NAME': name,
            'LAST_NAME': last_name,
        }

        if password:
            params['PASSWORD'] = password
        if work_position:
            params['WORK_POSITION'] = work_position
        if uf_department:
            params['UF_DEPARTMENT'] = uf_department

        params.update(kwargs)

        return self.client.call('user.add', params)

    def update(self, user_id: int, **fields) -> bool:
        """
        Обновить пользователя

        Args:
            user_id: ID пользователя
            **fields: Поля для обновления (NAME, WORK_POSITION и др.)
        """
        fields['ID'] = user_id
        return self.client.call('user.update', fields)

    def get_fields(self) -> Dict[str, Any]:
        """Получить описание полей пользователя"""
        return self.client.call('user.fields')

    # ==================== USER FIELDS (Custom) ====================

    def get_userfields(self) -> List[Dict[str, Any]]:
        """Получить список пользовательских полей"""
        result = self.client.call('user.userfield.list')
        return result if isinstance(result, list) else []

    def add_userfield(
        self,
        field_name: str,
        user_type_id: str = 'string',
        label: Optional[str] = None,
        **kwargs
    ) -> int:
        """
        Создать пользовательское поле

        Args:
            field_name: Название поля (без UF_)
            user_type_id: Тип (string, integer, date, file и др.)
            label: Подпись

        Returns:
            ID поля
        """
        params = {
            'FIELD_NAME': field_name,
            'USER_TYPE_ID': user_type_id,
        }
        if label:
            params['LABEL'] = label
        params.update(kwargs)

        return self.client.call('user.userfield.add', params)

    def update_userfield(self, field_id: int, **fields) -> bool:
        """Обновить пользовательское поле"""
        fields['ID'] = field_id
        return self.client.call('user.userfield.update', fields)

    def delete_userfield(self, field_id: int) -> bool:
        """Удалить пользовательское поле"""
        return self.client.call('user.userfield.delete', {'ID': field_id})
