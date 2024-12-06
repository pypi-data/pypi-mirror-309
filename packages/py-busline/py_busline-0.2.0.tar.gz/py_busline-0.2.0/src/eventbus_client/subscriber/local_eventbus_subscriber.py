from abc import ABC
from src.eventbus.eventbus import EventBus
from src.eventbus_client.subscriber.subscriber import Subscriber


class LocalEventBusSubscriber(Subscriber, ABC):
    """
    Abstract subscriber which works with local eventbus without implementing `on_event` method

    Author: Nicola Ricciardi
    """

    def __init__(self, eventbus_instance: EventBus):
        self._eventbus = eventbus_instance

    async def _internal_subscribe(self, topic_name: str):
        self._eventbus.add_subscriber(topic_name, self)

    async def _internal_unsubscribe(self, topic_name: str | None = None):
        self._eventbus.remove_subscriber(self, topic_name)