from typing import Callable
from abc import ABC
from src.event.event import Event
from src.eventbus_client.subscriber.subscriber import Subscriber


class ClosureSubscriber(Subscriber, ABC):
    """
    Abstract subscriber which use a pre-defined callback as `on_event`

    Author: Nicola Ricciardi
    """

    def __init__(self, on_event_callback: Callable[[Event], None]):
        self.__on_event_callback = on_event_callback

    async def on_event(self, topic_name: str, event: Event):
        self.__on_event_callback(event)
