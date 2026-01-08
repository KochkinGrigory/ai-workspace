"""
Операции с отделами Bitrix24 (5 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class DepartmentsManager:
    """Менеджер для работы со структурой компании Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    def get(
        self,
        department_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        name: Optional[str] = None,
        sort: str = 'ID',
        order: str = 'ASC'
    ) -> List[Dict[str, Any]]:
        """
        Получить список отделов

        Args:
            department_id: ID конкретного отдела
            parent_id: ID родительского отдела (0 = корневые)
            name: Фильтр по названию
            sort: Поле сортировки (ID, NAME, SORT)
            order: ASC или DESC

        Returns:
            Список отделов
        """
        params = {'SORT': sort, 'ORDER': order}

        if department_id:
            params['ID'] = department_id
        if parent_id is not None:
            params['PARENT'] = parent_id
        if name:
            params['NAME'] = name

        result = self.client.call('department.get', params)
        return result if isinstance(result, list) else []

    def get_by_id(self, department_id: int) -> Optional[Dict[str, Any]]:
        """Получить отдел по ID"""
        result = self.get(department_id=department_id)
        return result[0] if result else None

    def get_root(self) -> List[Dict[str, Any]]:
        """Получить корневые отделы (верхний уровень)"""
        return self.get(parent_id=0)

    def get_children(self, parent_id: int) -> List[Dict[str, Any]]:
        """Получить дочерние отделы"""
        return self.get(parent_id=parent_id)

    def get_tree(self, parent_id: int = 0) -> List[Dict[str, Any]]:
        """
        Получить дерево отделов рекурсивно

        Args:
            parent_id: ID родительского отдела (0 = с корня)

        Returns:
            Список отделов с вложенными children
        """
        departments = self.get(parent_id=parent_id)
        for dept in departments:
            dept_id = dept.get('ID')
            if dept_id:
                dept['children'] = self.get_tree(int(dept_id))
        return departments

    def add(
        self,
        name: str,
        parent_id: Optional[int] = None,
        sort: int = 500,
        head_id: Optional[int] = None
    ) -> int:
        """
        Создать отдел

        Args:
            name: Название отдела
            parent_id: ID родительского отдела
            sort: Порядок сортировки
            head_id: ID руководителя отдела

        Returns:
            ID созданного отдела
        """
        params = {'NAME': name, 'SORT': sort}

        if parent_id:
            params['PARENT'] = parent_id
        if head_id:
            params['UF_HEAD'] = head_id

        return self.client.call('department.add', params)

    def update(self, department_id: int, **fields) -> bool:
        """
        Обновить отдел

        Args:
            department_id: ID отдела
            **fields: Поля для обновления (NAME, PARENT, SORT, UF_HEAD)
        """
        fields['ID'] = department_id
        return self.client.call('department.update', fields)

    def delete(self, department_id: int) -> bool:
        """Удалить отдел"""
        return self.client.call('department.delete', {'ID': department_id})

    def get_fields(self) -> Dict[str, Any]:
        """Получить описание полей отдела"""
        return self.client.call('department.fields')
