import logging
import asyncio

from src.event.event import Event
from src.eventbus.eventbus import EventBus


class AsyncEventBus(EventBus):

    async def put_event(self, topic_name: str, event: Event):

        topic_subscription = self._topics_subscriptions.get(topic_name)

        logging.debug(f"new event {event} on topic {topic_subscription.topic.name}, notify subscribers: {topic_subscription.subscribers}")

        if len(topic_subscription.subscribers) == 0:
            return

        tasks = []

        for subscriber in topic_subscription.subscribers:
            task = asyncio.create_task(subscriber.on_event(event))
            tasks.append(task)

        await asyncio.gather(*tasks)

            
