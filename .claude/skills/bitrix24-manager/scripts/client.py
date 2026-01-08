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

    def batch(self, calls: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Выполнить пакетный запрос (batch)"""
        cmd = {}
        for cmd_id, call_data in calls.items():
            method = call_data['method']
            params = call_data.get('params', {})
            cmd[cmd_id] = f"{method}?{self._encode_params(params)}"

        return self.call('batch', {'cmd': cmd})

    @staticmethod
    def _encode_params(params: Dict[str, Any]) -> str:
        parts = []
        for key, value in params.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    parts.append(f"{key}[{sub_key}]={sub_value}")
            else:
                parts.append(f"{key}={value}")
        return '&'.join(parts)
