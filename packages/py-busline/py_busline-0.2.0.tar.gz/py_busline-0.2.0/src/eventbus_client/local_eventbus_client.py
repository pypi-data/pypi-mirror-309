from abc import ABC
from src.eventbus.eventbus import EventBus
from src.eventbus_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from src.eventbus_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalEventBusClient(LocalEventBusPublisher, LocalEventBusSubscriber, ABC):
    """
    Abstract eventbus client class for local eventbus which should be implemented to create a generic local eventbus client

    Author: Nicola Ricciardi
    """

    def __init__(self, eventbus_instance: EventBus):
        LocalEventBusPublisher.__init__(self, eventbus_instance)
        LocalEventBusSubscriber.__init__(self, eventbus_instance)
