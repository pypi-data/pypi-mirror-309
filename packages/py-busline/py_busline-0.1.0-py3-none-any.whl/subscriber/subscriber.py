from abc import ABC, abstractmethod
from src.eventbus.topic import Topic
from src.event.event import Event


class Subscriber(ABC):

    @abstractmethod
    async def on_event(self, event: Event):
        raise NotImplemented()

    def on_subscription(self, topic_name: str):
        """
        Callback called on subscription

        :param topic_name:
        :return:
        """

    def on_unsubscription(self, topic_name: str):
        """
        Callback called on unsubscription

        :param topic_name:
        :return:
        """