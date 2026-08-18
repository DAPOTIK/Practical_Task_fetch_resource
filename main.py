from typing import Optional
import httpx
from loguru import logger
from pydantic import BaseModel

DEF_TIME = 3.0

class Resource(BaseModel):
    userId: int
    id: int
    title: str
    body: str


def fetch_resource(
        resource_id: int,
        timeout: Optional[float] = DEF_TIME
) -> Optional[Resource]:
        url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"

        try:
            response = httpx.get(url, timeout=timeout)

            if response.status_code == 200:
                logger.info("Успешно (resource_id = {})", resource_id)
                return Resource(**response.json())

            if response.status_code == 404:
                logger.error("Ошибка 404 (resource_id = {}): {}", resource_id, response.json())
                return None

            logger.warning("Неожиданный статус {} (resource_id = {})", response.status_code, resource_id)
            return None

        except (httpx.ConnectError, httpx.TimeoutException) as e:
            logger.warning("Ошибка соединения (resource_id = {}): {}", resource_id, e)
            return None

        except Exception as e:
            logger.exception("Непредвиденная ошибка (resource_id = {}): {}", resource_id, e)
            return None


logger.info("post1 = {}", fetch_resource(resource_id=1))
logger.info("post2 = {}", fetch_resource(resource_id=999))
logger.info("post3 = {}", fetch_resource(resource_id=1, timeout=0.001))
