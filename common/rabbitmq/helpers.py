import json
import aio_pika

from typing import Any, Optional
from aio_pika.exceptions import QueueEmpty
from common.config import settings
from common.rabbitmq.connection import get_connection


async def publish_job(payload: dict) -> None:
    """Publish a message to the RabbitMQ queue."""
    conn = await get_connection()
    async with conn:
        ch = await conn.channel(publisher_confirms=True, on_return_raises=True)
        q = await ch.declare_queue(settings.queue_name, durable=True) 
        await ch.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            ),
            routing_key=q.name,
            mandatory=True,
        )
        
async def read_one_json(
    queue_name: str = settings.queue_name,
    timeout: float = 5.0,
    ack: bool = True,
) -> Optional[dict[str, Any]]:
    """
    Read a single message from the queue and return it as a dict.
    """
    conn = await get_connection()
    
    async with conn:
        channel = await conn.channel()
        queue = await channel.declare_queue(queue_name, durable=True)

        try:
            msg = await queue.get(timeout=timeout, no_ack=False)
        except QueueEmpty:
            return None

        try:
            data = json.loads(msg.body)
        except Exception:
            data = {"_raw": msg.body.decode("utf-8", "ignore")}

        if ack:
            await msg.ack()

        return data