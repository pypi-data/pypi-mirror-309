import aiohttp
from typing import Any, Dict, Optional


class AsyncRestClient:
    """Универсальный клиент для работы с REST API."""

    def __init__(self, address: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        """
        :param address: Базовый URL API.
        :param headers: Заголовки для всех запросов.
        :param timeout: Тайм-аут запросов в секундах.
        """
        self.address = address.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout

    async def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Выполняет запрос к REST API.
        :param method: HTTP-метод (GET, POST, PUT, DELETE).
        :param endpoint: URL эндпоинта.
        :param kwargs: Дополнительные параметры запроса.
        :return: Ответ API в виде JSON.
        """
        url = f"{self.address}/{endpoint.lstrip('/')}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(method, url, timeout=self.timeout, **kwargs) as response:
                response.raise_for_status()
                return await response.json()

    async def __call__(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Позволяет использовать клиент как функцию.
        :param method: HTTP-метод.
        :param endpoint: URL эндпоинта.
        :param kwargs: Дополнительные параметры.
        :return: Ответ API в виде JSON.
        """
        return await self.request(method, endpoint, **kwargs)
