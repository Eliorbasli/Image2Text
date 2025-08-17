import aio_pika
from aio_pika.abc import AbstractRobustConnection
from common.config import settings


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.amqp_url)
