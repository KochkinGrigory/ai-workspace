"""
Операции со смарт-процессами Bitrix24 (18 методов)

Смарт-процессы — гибкие сущности с настраиваемыми стадиями и полями.
Используются для внутренних процессов: согласования, заявки, обращения.

Технически это часть CRM (crm.item.*, crm.type.*), но логически —
отдельный инструмент для автоматизации бизнес-процессов.
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class SmartProcessesManager:
    """Менеджер для работы со смарт-процессами Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== TYPES (Смарт-процессы) ====================

    def get_types(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список смарт-процессов

        Args:
            filter_params: Фильтры (id, title, entityTypeId)
            select: Поля для выборки

        Returns:
            Список смарт-процессов
        """
        params = {}
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select

        result = self.client.call('crm.type.list', params)
        if isinstance(result, dict):
            return result.get('types', [])
        return result if isinstance(result, list) else []

    def get_type(self, type_id: int) -> Dict[str, Any]:
        """
        Получить смарт-процесс по ID

        Args:
            type_id: ID смарт-процесса (не entityTypeId!)
        """
        result = self.client.call('crm.type.get', {'id': type_id})
        return result.get('type', result) if isinstance(result, dict) else {}

    def get_type_by_entity_id(self, entity_type_id: int) -> Dict[str, Any]:
        """
        Получить смарт-процесс по entityTypeId

        Args:
            entity_type_id: ID типа сущности (128, 130, 132...)

        Note:
            entityTypeId — это числовой идентификатор типа в CRM.
            Стандартные: 1=Lead, 2=Deal, 3=Contact, 4=Company
            Смарт-процессы: 128+
        """
        result = self.client.call('crm.type.get', {'entityTypeId': entity_type_id})
        return result.get('type', result) if isinstance(result, dict) else {}

    def add_type(
        self,
        title: str,
        code: Optional[str] = None,
        is_categories_enabled: bool = True,
        is_stages_enabled: bool = True,
        is_begin_close_dates_enabled: bool = True,
        is_client_enabled: bool = False,
        is_use_in_userfieldset_enabled: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Создать смарт-процесс

        Args:
            title: Название
            code: Символьный код (латиница, уникальный)
            is_categories_enabled: Использовать направления (воронки)
            is_stages_enabled: Использовать стадии
            is_begin_close_dates_enabled: Даты начала/завершения
            is_client_enabled: Привязка к клиенту (контакт/компания)
            is_use_in_userfieldset_enabled: В наборах полей

        Returns:
            Созданный смарт-процесс
        """
        fields = {
            'title': title,
            'isCategoriesEnabled': 'Y' if is_categories_enabled else 'N',
            'isStagesEnabled': 'Y' if is_stages_enabled else 'N',
            'isBeginCloseDatesEnabled': 'Y' if is_begin_close_dates_enabled else 'N',
            'isClientEnabled': 'Y' if is_client_enabled else 'N',
            'isUseInUserfieldEnabled': 'Y' if is_use_in_userfieldset_enabled else 'N',
        }
        if code:
            fields['code'] = code

        fields.update(kwargs)

        result = self.client.call('crm.type.add', {'fields': fields})
        return result.get('type', result) if isinstance(result, dict) else result

    def update_type(self, type_id: int, **fields) -> Dict[str, Any]:
        """
        Обновить смарт-процесс

        Args:
            type_id: ID смарт-процесса
            **fields: Поля для обновления (title, code и др.)
        """
        result = self.client.call('crm.type.update', {
            'id': type_id,
            'fields': fields
        })
        return result.get('type', result) if isinstance(result, dict) else result

    def delete_type(self, type_id: int) -> bool:
        """Удалить смарт-процесс"""
        return self.client.call('crm.type.delete', {'id': type_id})

    def get_type_fields(self) -> Dict[str, Any]:
        """Получить описание полей смарт-процесса"""
        return self.client.call('crm.type.fields')

    # ==================== ITEMS (Элементы) ====================

    def get_items(
        self,
        entity_type_id: int,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None,
        start: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Получить элементы смарт-процесса

        Args:
            entity_type_id: ID типа сущности (128, 130...)
            filter_params: Фильтры (stageId, assignedById, categoryId и др.)
            select: Поля для выборки
            order: Сортировка {'id': 'DESC'}
            start: Смещение для пагинации

        Returns:
            Список элементов
        """
        params = {'entityTypeId': entity_type_id}
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select
        if order:
            params['order'] = order
        if start:
            params['start'] = start

        result = self.client.call('crm.item.list', params)
        if isinstance(result, dict):
            return result.get('items', [])
        return result if isinstance(result, list) else []

    def get_item(
        self,
        entity_type_id: int,
        item_id: int
    ) -> Dict[str, Any]:
        """
        Получить элемент по ID

        Args:
            entity_type_id: ID типа сущности
            item_id: ID элемента
        """
        result = self.client.call('crm.item.get', {
            'entityTypeId': entity_type_id,
            'id': item_id
        })
        return result.get('item', result) if isinstance(result, dict) else {}

    def add_item(
        self,
        entity_type_id: int,
        title: str,
        stage_id: Optional[str] = None,
        assigned_by_id: Optional[int] = None,
        category_id: Optional[int] = None,
        begin_date: Optional[str] = None,
        close_date: Optional[str] = None,
        **fields
    ) -> Dict[str, Any]:
        """
        Создать элемент смарт-процесса

        Args:
            entity_type_id: ID типа сущности
            title: Название
            stage_id: ID стадии (например 'DT128_1:NEW')
            assigned_by_id: ID ответственного
            category_id: ID направления (воронки)
            begin_date: Дата начала (2024-12-20T10:00:00)
            close_date: Дата завершения
            **fields: Дополнительные поля (ufCrm...)

        Returns:
            Созданный элемент
        """
        item_fields = {'title': title}

        if stage_id:
            item_fields['stageId'] = stage_id
        if assigned_by_id:
            item_fields['assignedById'] = assigned_by_id
        if category_id:
            item_fields['categoryId'] = category_id
        if begin_date:
            item_fields['begindate'] = begin_date
        if close_date:
            item_fields['closedate'] = close_date

        item_fields.update(fields)

        result = self.client.call('crm.item.add', {
            'entityTypeId': entity_type_id,
            'fields': item_fields
        })
        return result.get('item', result) if isinstance(result, dict) else result

    def update_item(
        self,
        entity_type_id: int,
        item_id: int,
        **fields
    ) -> Dict[str, Any]:
        """
        Обновить элемент

        Args:
            entity_type_id: ID типа сущности
            item_id: ID элемента
            **fields: Поля для обновления
        """
        result = self.client.call('crm.item.update', {
            'entityTypeId': entity_type_id,
            'id': item_id,
            'fields': fields
        })
        return result.get('item', result) if isinstance(result, dict) else result

    def delete_item(self, entity_type_id: int, item_id: int) -> bool:
        """Удалить элемент"""
        return self.client.call('crm.item.delete', {
            'entityTypeId': entity_type_id,
            'id': item_id
        })

    def get_item_fields(self, entity_type_id: int) -> Dict[str, Any]:
        """
        Получить описание полей элементов смарт-процесса

        Args:
            entity_type_id: ID типа сущности
        """
        result = self.client.call('crm.item.fields', {'entityTypeId': entity_type_id})
        return result.get('fields', result) if isinstance(result, dict) else result

    # ==================== STAGES (Стадии) ====================

    def get_stages(
        self,
        entity_type_id: int,
        category_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить стадии смарт-процесса

        Args:
            entity_type_id: ID типа сущности
            category_id: ID направления (воронки)

        Note:
            Использует crm.status.list с фильтром по ENTITY_ID
        """
        # Формируем ENTITY_ID для смарт-процесса
        # Формат: DYNAMIC_{entityTypeId}_STAGE_{categoryId}
        if category_id:
            entity_id = f'DYNAMIC_{entity_type_id}_STAGE_{category_id}'
        else:
            entity_id = f'DYNAMIC_{entity_type_id}_STAGE_0'

        result = self.client.call('crm.status.list', {
            'filter': {'ENTITY_ID': entity_id},
            'order': {'SORT': 'ASC'}
        })
        return result if isinstance(result, list) else []

    def move_to_stage(
        self,
        entity_type_id: int,
        item_id: int,
        stage_id: str
    ) -> Dict[str, Any]:
        """
        Переместить элемент на стадию

        Args:
            entity_type_id: ID типа сущности
            item_id: ID элемента
            stage_id: ID стадии (например 'DT128_1:SUCCESS')
        """
        return self.update_item(entity_type_id, item_id, stageId=stage_id)

    # ==================== CATEGORIES (Направления/воронки) ====================

    def get_categories(self, entity_type_id: int) -> List[Dict[str, Any]]:
        """
        Получить направления (воронки) смарт-процесса

        Args:
            entity_type_id: ID типа сущности
        """
        result = self.client.call('crm.category.list', {
            'entityTypeId': entity_type_id
        })
        if isinstance(result, dict):
            return result.get('categories', [])
        return result if isinstance(result, list) else []

    def add_category(
        self,
        entity_type_id: int,
        name: str,
        sort: int = 500,
        is_default: bool = False
    ) -> Dict[str, Any]:
        """
        Создать направление (воронку)

        Args:
            entity_type_id: ID типа сущности
            name: Название
            sort: Сортировка
            is_default: По умолчанию
        """
        result = self.client.call('crm.category.add', {
            'entityTypeId': entity_type_id,
            'fields': {
                'name': name,
                'sort': sort,
                'isDefault': 'Y' if is_default else 'N'
            }
        })
        return result.get('category', result) if isinstance(result, dict) else result

    # ==================== HELPERS ====================

    def find_type_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Найти смарт-процесс по названию"""
        types = self.get_types()
        for t in types:
            if t.get('title', '').lower() == title.lower():
                return t
        return None

    def get_items_by_stage(
        self,
        entity_type_id: int,
        stage_id: str
    ) -> List[Dict[str, Any]]:
        """Получить элементы на определённой стадии"""
        return self.get_items(entity_type_id, filter_params={'stageId': stage_id})

    def get_my_items(self, entity_type_id: int) -> List[Dict[str, Any]]:
        """Получить мои элементы (где я ответственный)"""
        # assignedById = 0 означает текущего пользователя в некоторых методах
        # но лучше сначала получить current user
        from .users import UsersManager
        users = UsersManager(self.client)
        current = users.get_current()
        user_id = current.get('ID')
        if user_id:
            return self.get_items(entity_type_id, filter_params={'assignedById': user_id})
        return []
