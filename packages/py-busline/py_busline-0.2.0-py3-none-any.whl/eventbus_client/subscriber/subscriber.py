from abc import ABC, abstractmethod
from src.event.event import Event


class Subscriber(ABC):
    """
    Abstract class which can be implemented by your components which must be able to subscribe on eventbus

    Author: Nicola Ricciardi
    """

    @abstractmethod
    async def on_event(self, topic_name: str, event: Event):
        """
        Callback called when new event arrives

        :param topic_name:
        :param event:
        :return:
        """

    @abstractmethod
    async def _internal_subscribe(self, topic_name: str):
        """
        Actual subscribe to topic

        :param topic_name:
        :return:
        """

    @abstractmethod
    async def _internal_unsubscribe(self, topic_name: str | None = None):
        """
        Actual unsubscribe to topic

        :param topic_name:
        :return:
        """

    async def subscribe(self, topic_name: str):
        """
        Subscribe to topic

        :param topic_name:
        :return:
        """

        self.on_subscribing(topic_name)
        await self._internal_subscribe(topic_name)
        self.on_subscribed(topic_name)

    async def unsubscribe(self, topic_name: str | None = None):
        """
        Unsubscribe to topic

        :param topic_name:
        :return:
        """

        self.on_unsubscribing(topic_name)
        await self._internal_unsubscribe(topic_name)
        self.on_unsubscribed(topic_name)

    def on_subscribing(self, topic_name: str):
        """
        Callback called on subscribing

        :param topic_name:
        :return:
        """

    def on_subscribed(self, topic_name: str):
        """
        Callback called on subscribed

        :param topic_name:
        :return:
        """

    def on_unsubscribing(self, topic_name: str):
        """
        Callback called on unsubscribing

        :param topic_name:
        :return:
        """

    def on_unsubscribed(self, topic_name: str):
        """
        Callback called on unsubscribed

        :param topic_name:
        :return:
        """