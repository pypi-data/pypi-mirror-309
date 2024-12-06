from typing import Callable

from src.event.event import Event
from src.subscriber.subscriber import Subscriber


class ClosureSubscriber(Subscriber):

    def __init__(self, on_event_callback: Callable[[Event], None]):
        self.__on_event_callback = on_event_callback

    async def on_event(self, event: Event):
        self.__on_event_callback(event)
