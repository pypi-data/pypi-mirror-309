import httpx
from .exceptions import RestQueryError

class AsyncRestClient:
    def __init__(self, address: str, headers: dict[str, str], timeout: int):
        self.address = address.rstrip("/")
        self.headers = headers
        self.timeout = timeout

    async def __call__(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.address}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            response = await client.request(method, url, **kwargs)
            if response.status_code not in {200, 201}:
                raise RestQueryError(
                    f"HTTP {response.status_code}: {response.text}",
                    status_code=response.status_code,
                )
            return response.json()
