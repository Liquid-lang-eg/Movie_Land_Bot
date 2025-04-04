from aiohttp.client import ClientSession

async def fetch_from_backend(
    endpoint: str,
    params: dict = None,
    method: str = "GET",
    data: dict = None,
):
    """
    Делает запрос к локальному (или любому другому) бэкенду.
    Поддерживает методы GET, POST и DELETE.
    """
    url = f"{settings.BACKEND_URL}{endpoint}"
    if params is None:
        params = {}

    async with ClientSession() as session:
        method = method.upper()

        if method == "GET":
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    error_body = await response.text()
                    error_body = error_body[:settings.MAX_ERROR_LENGTH]
                    raise Exception(
                        f"Ошибка при запросе к бэкенду: {response.status}. "
                        f"Тело ответа: {error_body}"
                    )
        elif method == "POST":
            async with session.post(url, json=data, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    error_body = await response.text()
                    error_body = error_body[:settings.MAX_ERROR_LENGTH]
                    raise Exception(
                        f"Ошибка при запросе к бэкенду: {response.status}. "
                        f"Тело ответа: {error_body}"
                    )
        elif method == "DELETE":
            async with session.delete(url, json=data, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    error_body = await response.text()
                    error_body = error_body[:settings.MAX_ERROR_LENGTH]
                    raise Exception(
                        f"Ошибка при запросе к бэкенду: {response.status}. "
                        f"Тело ответа: {error_body}"
                    )
        else:
            raise Exception(f"Unsupported HTTP method: {method}")