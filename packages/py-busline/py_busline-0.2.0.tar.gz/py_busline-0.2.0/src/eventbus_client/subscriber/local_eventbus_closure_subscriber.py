from typing import Callable
from src.event.event import Event
from src.eventbus.eventbus import EventBus
from src.eventbus_client.subscriber.closure_subscriber import ClosureSubscriber
from src.eventbus_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalEventBusClosureSubscriber(LocalEventBusSubscriber, ClosureSubscriber):
    """
    Subscriber which works with local eventbus, this class can be initialized and used stand-alone

    Author: Nicola Ricciardi
    """

    def __init__(self, eventbus_instance: EventBus, on_event_callback: Callable[[Event], None]):
        ClosureSubscriber.__init__(self, on_event_callback)
        self._eventbus = eventbus_instance