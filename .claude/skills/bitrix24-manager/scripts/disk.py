"""
Операции с диском Bitrix24 (14 методов)
"""
from typing import Dict, Any, Optional, List
from .client import BitrixClient


class DiskManager:
    """Менеджер для работы с диском Bitrix24"""

    def __init__(self, client: Optional[BitrixClient] = None):
        self.client = client or BitrixClient()

    # ==================== STORAGE ====================

    def get_storages(self) -> List[Dict[str, Any]]:
        """
        Получить список доступных хранилищ

        Returns:
            Список хранилищ (personal, group, common)
        """
        result = self.client.call('disk.storage.getlist')
        return result if isinstance(result, list) else []

    def get_storage(self, storage_id: int) -> Dict[str, Any]:
        """Получить хранилище по ID"""
        return self.client.call('disk.storage.get', {'id': storage_id})

    def get_storage_children(
        self,
        storage_id: int,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить содержимое корня хранилища

        Args:
            storage_id: ID хранилища
            filter_params: Фильтры (NAME, TYPE и др.)
        """
        params = {'id': storage_id}
        if filter_params:
            params['filter'] = filter_params

        result = self.client.call('disk.storage.getchildren', params)
        return result if isinstance(result, list) else []

    # ==================== FOLDERS ====================

    def get_folder(self, folder_id: int) -> Dict[str, Any]:
        """Получить папку по ID"""
        return self.client.call('disk.folder.get', {'id': folder_id})

    def get_folder_children(
        self,
        folder_id: int,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить содержимое папки

        Args:
            folder_id: ID папки
            filter_params: Фильтры (NAME, TYPE и др.)
        """
        params = {'id': folder_id}
        if filter_params:
            params['filter'] = filter_params

        result = self.client.call('disk.folder.getchildren', params)
        return result if isinstance(result, list) else []

    def create_folder(
        self,
        storage_id: int,
        name: str,
        parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Создать папку

        Args:
            storage_id: ID хранилища (если в корне)
            name: Название папки
            parent_id: ID родительской папки (если не в корне)

        Returns:
            Созданная папка
        """
        if parent_id:
            # Создаём внутри папки
            return self.client.call('disk.folder.addsubfolder', {
                'id': parent_id,
                'data': {'NAME': name}
            })
        else:
            # Создаём в корне хранилища
            return self.client.call('disk.storage.addfolder', {
                'id': storage_id,
                'data': {'NAME': name}
            })

    def rename_folder(self, folder_id: int, name: str) -> Dict[str, Any]:
        """Переименовать папку"""
        return self.client.call('disk.folder.rename', {
            'id': folder_id,
            'newName': name
        })

    def delete_folder(self, folder_id: int) -> bool:
        """Удалить папку"""
        return self.client.call('disk.folder.deletetree', {'id': folder_id})

    def move_folder(self, folder_id: int, target_folder_id: int) -> Dict[str, Any]:
        """Переместить папку"""
        return self.client.call('disk.folder.moveto', {
            'id': folder_id,
            'targetFolderId': target_folder_id
        })

    def copy_folder(self, folder_id: int, target_folder_id: int) -> Dict[str, Any]:
        """Копировать папку"""
        return self.client.call('disk.folder.copyto', {
            'id': folder_id,
            'targetFolderId': target_folder_id
        })

    # ==================== FILES ====================

    def get_file(self, file_id: int) -> Dict[str, Any]:
        """Получить файл по ID"""
        return self.client.call('disk.file.get', {'id': file_id})

    def rename_file(self, file_id: int, name: str) -> Dict[str, Any]:
        """Переименовать файл"""
        return self.client.call('disk.file.rename', {
            'id': file_id,
            'newName': name
        })

    def delete_file(self, file_id: int) -> bool:
        """Удалить файл"""
        return self.client.call('disk.file.delete', {'id': file_id})

    def move_file(self, file_id: int, target_folder_id: int) -> Dict[str, Any]:
        """Переместить файл в другую папку"""
        return self.client.call('disk.file.moveto', {
            'id': file_id,
            'targetFolderId': target_folder_id
        })

    def copy_file(self, file_id: int, target_folder_id: int) -> Dict[str, Any]:
        """Копировать файл в другую папку"""
        return self.client.call('disk.file.copyto', {
            'id': file_id,
            'targetFolderId': target_folder_id
        })

    def get_download_url(self, file_id: int) -> str:
        """
        Получить URL для скачивания файла

        Returns:
            URL для скачивания
        """
        result = self.client.call('disk.file.get', {'id': file_id})
        return result.get('DOWNLOAD_URL', '') if isinstance(result, dict) else ''

    def restore_file(self, file_id: int) -> Dict[str, Any]:
        """Восстановить файл из корзины"""
        return self.client.call('disk.file.restore', {'id': file_id})

    # ==================== UPLOAD ====================

    def upload_file(
        self,
        folder_id: int,
        file_content: bytes,
        filename: str
    ) -> Dict[str, Any]:
        """
        Загрузить файл в папку

        Args:
            folder_id: ID папки назначения
            file_content: Содержимое файла (bytes)
            filename: Имя файла

        Returns:
            Загруженный файл

        Note:
            Для загрузки файлов требуется multipart/form-data,
            что не поддерживается стандартным webhook.
            Используйте disk.folder.uploadfile через OAuth приложение.
        """
        import base64

        # Для webhook доступен только метод с base64
        content_base64 = base64.b64encode(file_content).decode('utf-8')

        return self.client.call('disk.folder.uploadfile', {
            'id': folder_id,
            'data': {'NAME': filename},
            'fileContent': content_base64
        })

    # ==================== SEARCH ====================

    def search(
        self,
        query: str,
        storage_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Поиск файлов по имени

        Args:
            query: Поисковый запрос
            storage_id: ID хранилища (опционально)
        """
        params = {'filter': {'NAME': f'%{query}%'}}
        if storage_id:
            params['id'] = storage_id
            result = self.client.call('disk.storage.getchildren', params)
        else:
            # Поиск по всем хранилищам
            all_results = []
            storages = self.get_storages()
            for storage in storages:
                params['id'] = storage.get('ID')
                result = self.client.call('disk.storage.getchildren', params)
                if isinstance(result, list):
                    all_results.extend(result)
            return all_results

        return result if isinstance(result, list) else []

    # ==================== SHARING ====================

    def get_external_link(self, file_id: int) -> Dict[str, Any]:
        """
        Получить внешнюю ссылку на файл

        Returns:
            Информация о публичной ссылке
        """
        return self.client.call('disk.file.getExternalLink', {'id': file_id})

    def get_file_versions(self, file_id: int) -> List[Dict[str, Any]]:
        """Получить версии файла"""
        result = self.client.call('disk.file.getVersions', {'id': file_id})
        return result if isinstance(result, list) else []
