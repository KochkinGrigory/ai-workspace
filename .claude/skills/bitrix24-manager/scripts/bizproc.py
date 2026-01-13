"""
Операции с бизнес-процессами Bitrix24 (8 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class BizprocManager:
    """Менеджер для работы с бизнес-процессами Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== WORKFLOW ====================

    def start(
        self,
        template_id: int,
        document_id: List[str],
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Запустить бизнес-процесс

        Args:
            template_id: ID шаблона БП
            document_id: ID документа в формате ['module', 'entity', 'id']
                        Примеры:
                        - ['crm', 'CCrmDocumentDeal', 'DEAL_123']
                        - ['crm', 'CCrmDocumentLead', 'LEAD_456']
                        - ['lists', 'BizprocDocument', 'iblock_123_789']
                        - ['disk', 'Bitrix\\Disk\\BizProcDocument', '123']
            parameters: Параметры для запуска БП

        Returns:
            ID запущенного процесса (workflow_id)
        """
        params = {
            'TEMPLATE_ID': template_id,
            'DOCUMENT_ID': document_id,
        }
        if parameters:
            params['PARAMETERS'] = parameters

        return self.client.call('bizproc.workflow.start', params)

    def terminate(self, workflow_id: str, status: str = '') -> bool:
        """
        Остановить бизнес-процесс (мягко)

        Args:
            workflow_id: ID процесса
            status: Статус/сообщение завершения
        """
        params = {'ID': workflow_id}
        if status:
            params['STATUS'] = status

        return self.client.call('bizproc.workflow.terminate', params)

    def kill(self, workflow_id: str) -> bool:
        """
        Принудительно удалить бизнес-процесс

        Args:
            workflow_id: ID процесса

        Note:
            Используйте terminate() для мягкой остановки
        """
        return self.client.call('bizproc.workflow.kill', {'ID': workflow_id})

    def get_instances(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None,
        order: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список запущенных процессов

        Args:
            filter_params: Фильтры
                - DOCUMENT_ID: ID документа
                - TEMPLATE_ID: ID шаблона
                - MODULE_ID: ID модуля
                - ENTITY: Сущность
                - STARTED: Дата запуска
                - STARTED_BY: Кто запустил
            select: Поля для выборки
            order: Сортировка

        Returns:
            Список запущенных БП
        """
        params = {}
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select
        if order:
            params['order'] = order

        result = self.client.call('bizproc.workflow.instances', params)
        return result if isinstance(result, list) else []

    # ==================== TEMPLATES ====================

    def get_templates(
        self,
        filter_params: Optional[Dict[str, Any]] = None,
        select: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список шаблонов БП

        Args:
            filter_params: Фильтры
                - MODULE_ID: crm, lists, disk и др.
                - ENTITY: CCrmDocumentDeal, CCrmDocumentLead и др.
                - DOCUMENT_TYPE: Тип документа
                - NAME: Название шаблона
                - ACTIVE: Y/N
            select: Поля для выборки

        Returns:
            Список шаблонов
        """
        params = {}
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select

        result = self.client.call('bizproc.workflow.template.list', params)
        return result if isinstance(result, list) else []

    def add_template(
        self,
        document_type: List[str],
        name: str,
        template_data: str,
        auto_execute: int = 0,
        description: Optional[str] = None
    ) -> int:
        """
        Создать шаблон БП

        Args:
            document_type: Тип документа ['module', 'entity', 'type']
                          Пример: ['crm', 'CCrmDocumentDeal', 'DEAL']
            name: Название шаблона
            template_data: Данные шаблона в формате Base64 (экспорт из конструктора)
            auto_execute: Автозапуск
                - 0: не запускать
                - 1: при создании
                - 2: при изменении
                - 3: при создании и изменении
            description: Описание

        Returns:
            ID созданного шаблона
        """
        params = {
            'DOCUMENT_TYPE': document_type,
            'NAME': name,
            'TEMPLATE_DATA': template_data,
            'AUTO_EXECUTE': auto_execute,
        }
        if description:
            params['DESCRIPTION'] = description

        return self.client.call('bizproc.workflow.template.add', params)

    def update_template(self, template_id: int, **fields) -> bool:
        """
        Обновить шаблон БП

        Args:
            template_id: ID шаблона
            **fields: Поля для обновления (NAME, TEMPLATE_DATA, AUTO_EXECUTE и др.)
        """
        fields['ID'] = template_id
        return self.client.call('bizproc.workflow.template.update', fields)

    def delete_template(self, template_id: int) -> bool:
        """Удалить шаблон БП"""
        return self.client.call('bizproc.workflow.template.delete', {'ID': template_id})

    # ==================== HELPERS ====================

    def get_crm_templates(self, entity: str = 'CCrmDocumentDeal') -> List[Dict[str, Any]]:
        """
        Получить шаблоны для CRM сущности

        Args:
            entity: CCrmDocumentDeal, CCrmDocumentLead, CCrmDocumentContact и др.
        """
        return self.get_templates(filter_params={
            'MODULE_ID': 'crm',
            'ENTITY': entity
        })

    def start_for_deal(
        self,
        template_id: int,
        deal_id: int,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Запустить БП для сделки

        Args:
            template_id: ID шаблона
            deal_id: ID сделки
            parameters: Параметры
        """
        return self.start(
            template_id=template_id,
            document_id=['crm', 'CCrmDocumentDeal', f'DEAL_{deal_id}'],
            parameters=parameters
        )

    def start_for_lead(
        self,
        template_id: int,
        lead_id: int,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Запустить БП для лида

        Args:
            template_id: ID шаблона
            lead_id: ID лида
            parameters: Параметры
        """
        return self.start(
            template_id=template_id,
            document_id=['crm', 'CCrmDocumentLead', f'LEAD_{lead_id}'],
            parameters=parameters
        )
