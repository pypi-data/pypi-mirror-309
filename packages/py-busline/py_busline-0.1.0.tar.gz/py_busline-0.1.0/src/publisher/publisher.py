import logging
from src.event.event import Event
from src.eventbus.eventbus import EventBus

class Publisher:

    def __init__(self, eventbus: EventBus):
        self.__eventbus = eventbus

        logging.info("publisher generated")

    async def publish(self, topic_name: str, event: Event):
        self.on_publish(event)
        await self.__eventbus.put_event(topic_name, event)
        self.on_published(event)

    def on_publish(self, event: Event):
        """
        Callback called on publishing start

        :param event:
        :return:
        """

    def on_published(self, event: Event):
        """
        Callback called on publishing end

        :param event:
        :return:
        """