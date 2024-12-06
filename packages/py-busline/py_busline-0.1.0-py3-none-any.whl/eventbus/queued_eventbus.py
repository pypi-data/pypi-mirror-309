import asyncio
import logging
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

from src.event.event import Event
from src.eventbus.eventbus import EventBus
from src.eventbus.topic import Topic

MAX_WORKERS = 3
MAX_QUEUE_SIZE = 0


class QueuedEventBus(EventBus):

    def __init__(self, max_queue_size=MAX_QUEUE_SIZE, n_workers=MAX_WORKERS):

        super().__init__()

        self.__queue = Queue(maxsize=max_queue_size)
        self.__n_workers = n_workers

        self.__tpool = ThreadPoolExecutor(max_workers=self.__n_workers)

        for i in range(self.__n_workers):
            self.__tpool.submit(self.__elaborate_queue)

    async def put_event(self, topic_name: str, event: Event):
        self.__queue.put((topic_name, event))

    def __elaborate_queue(self):

        while True:

            topic_name, event = self.__queue.get()

            topic_subscription = self._topics_subscriptions.get(topic_name)

            logging.debug(
                f"new event {event} on topic {topic_subscription.topic.name}, notify subscribers: {topic_subscription.subscribers}")

            if len(topic_subscription.subscribers) == 0:
                return

            for subscriber in topic_subscription.subscribers:
                asyncio.run(subscriber.on_event(event))
