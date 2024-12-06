import logging
from abc import ABC, abstractmethod
from src.event.event import Event
from src.eventbus.eventbus import EventBus


class Publisher(ABC):
    """
    Abstract class which can be implemented by your components which must be able to publish on eventbus

    Author: Nicola Ricciardi
    """

    @abstractmethod
    async def _internal_publish(self, topic_name: str, event: Event):
        """
        Actual publish on topic the event

        :param topic_name:
        :param event:
        :return:
        """

    async def publish(self, topic_name: str, event: Event):
        """
        Publish on topic the event

        :param topic_name:
        :param event:
        :return:
        """

        self.on_publishing(topic_name, event)
        await self._internal_publish(topic_name, event)
        self.on_published(topic_name, event)

    def on_publishing(self, topic_name: str, event: Event):
        """
        Callback called on publishing start

        :param topic_name:
        :param event:
        :return:
        """

    def on_published(self, topic_name: str, event: Event):
        """
        Callback called on publishing end

        :param topic_name:
        :param event:
        :return:
        """