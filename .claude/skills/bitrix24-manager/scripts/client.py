"""
HTTP клиент для работы с Bitrix24 REST API
"""
import json
import requests
from typing import Dict, Any, Optional
from .config import BITRIX24_WEBHOOK_URL


class BitrixAPIError(Exception):
    """Ошибка при работе с Bitrix24 API"""
    pass


class BitrixClient:
    """Клиент для работы с Bitrix24 REST API"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or BITRIX24_WEBHOOK_URL
        if not self.webhook_url.endswith('/'):
            self.webhook_url += '/'

    def _get_url(self, method: str, use_v3: bool = False) -> str:
        """
        Получить URL для вызова метода

        REST v3 API требует /rest/api/ вместо /rest/
        """
        if use_v3:
            url = self.webhook_url.replace('/rest/', '/rest/api/')
            return f"{url}{method}.json"
        return f"{self.webhook_url}{method}.json"

    def call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполнить REST API метод

        Args:
            method: Название метода (например, 'tasks.task.add')
            params: Параметры метода

        Returns:
            Ответ API (поле 'result')
        """
        url = self._get_url(method)

        try:
            response = requests.post(url, json=params or {}, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                error_msg = data.get('error_description', data.get('error', 'Unknown error'))
                raise BitrixAPIError(f"Bitrix24 API Error: {error_msg}")

            return data.get('result', {})

        except requests.RequestException as e:
            raise BitrixAPIError(f"HTTP Error: {str(e)}")
        except json.JSONDecodeError as e:
            raise BitrixAPIError(f"JSON Decode Error: {str(e)}")

    def call_v3(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполнить REST v3 API метод (использует /rest/api/)

        Note: REST v3 может быть недоступен на некоторых порталах
        """
        url = self._get_url(method, use_v3=True)

        try:
            response = requests.post(url, json=params or {}, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                error = data['error']
                if isinstance(error, dict):
                    error_msg = error.get('message', str(error))
                else:
                    error_msg = str(error)
                raise BitrixAPIError(f"Bitrix24 API Error: {error_msg}")

            result = data.get('result', {})
            if isinstance(result, dict) and 'result' in result:
                return result['result']
            return result

        except requests.RequestException as e:
            raise BitrixAPIError(f"HTTP Error: {str(e)}")
        except json.JSONDecodeError as e:
            raise BitrixAPIError(f"JSON Decode Error: {str(e)}")

    def batch(self, commands: list) -> Dict[str, Any]:
        """
        Выполнить пакетный запрос (до 50 команд за раз)

        Args:
            commands: Список кортежей (method, params) или строк 'method?params'

        Returns:
            {'cmd1': result1, 'cmd2': result2, ...}

        Example:
            results = client.batch([
                ('tasks.task.get', {'taskId': 100}),
                ('tasks.task.get', {'taskId': 101}),
                ('user.current', {}),
            ])
        """
        cmd = {}
        for i, item in enumerate(commands):
            cmd_id = f'cmd{i}'
            if isinstance(item, str):
                cmd[cmd_id] = item
            elif isinstance(item, tuple):
                method, params = item[0], item[1] if len(item) > 1 else {}
                cmd[cmd_id] = f"{method}?{self._encode_params(params)}"

        result = self.call('batch', {'halt': 0, 'cmd': cmd})

        # Преобразуем результат в удобный формат
        if isinstance(result, dict) and 'result' in result:
            return result['result']
        return result

    def batch_complete_tasks(self, task_ids: list) -> Dict[str, Any]:
        """Завершить несколько задач за один запрос"""
        commands = [('tasks.task.complete', {'taskId': tid}) for tid in task_ids]
        return self.batch(commands)

    def batch_get_tasks(self, task_ids: list) -> list:
        """Получить несколько задач за один запрос"""
        commands = [('tasks.task.get', {'taskId': tid}) for tid in task_ids]
        results = self.batch(commands)
        return [r.get('task', r) for r in results.values() if r]

    def batch_notify(self, notifications: list) -> Dict[str, Any]:
        """
        Отправить несколько уведомлений за один запрос

        Args:
            notifications: Список кортежей (user_id, message)
        """
        commands = [
            ('im.notify.personal.add', {'USER_ID': uid, 'MESSAGE': msg})
            for uid, msg in notifications
        ]
        return self.batch(commands)

    @staticmethod
    def _encode_params(params: Dict[str, Any]) -> str:
        """Кодирование параметров для batch URL"""
        from urllib.parse import quote
        parts = []
        for key, value in params.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    parts.append(f"{key}[{sub_key}]={quote(str(sub_value))}")
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    parts.append(f"{key}[{i}]={quote(str(item))}")
            else:
                parts.append(f"{key}={quote(str(value))}")
        return '&'.join(parts)
