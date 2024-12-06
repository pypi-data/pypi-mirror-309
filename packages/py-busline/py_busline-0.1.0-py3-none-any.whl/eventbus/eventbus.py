from abc import ABC, abstractmethod
from typing import Dict
from src.eventbus.exceptions import TopicNotFound
from src.subscriber.subscriber import Subscriber
from src.eventbus.topic import Topic, TopicSubscriptions
from src.event.event import Event



class EventBus(ABC):

    def __init__(self):
        self._topics_subscriptions: Dict[str, TopicSubscriptions] = {}

    def add_topic(self, topic: Topic):
        self._topics_subscriptions[topic.name] = TopicSubscriptions(topic)

    def add_subscriber(self, topic_name: str, subscriber: Subscriber, raise_if_topic_missed: bool = False):
        """
        Add subscriber to topic

        :param raise_if_topic_missed:
        :param topic_name:
        :param subscriber:
        :return:
        """

        if topic_name not in self._topics_subscriptions.keys():
            if raise_if_topic_missed:
                raise TopicNotFound(f"topic '{topic_name}' not found")

            else:
                self._topics_subscriptions[topic_name] = TopicSubscriptions(Topic(topic_name))

        self._topics_subscriptions[topic_name].subscribers.append(subscriber)
        subscriber.on_subscription(topic_name)

    def remove_subscriber(self, subscriber: Subscriber, topic_name: str = None):
        """
        Remove subscriber from topic selected or from all if topic is None

        :param subscriber:
        :param topic_name:
        :return:
        """

        for name in self._topics_subscriptions.keys():

            if topic_name is None or topic_name == name:
                self._topics_subscriptions[name].subscribers.remove(subscriber)
                subscriber.on_unsubscription(name)

    @abstractmethod
    async def put_event(self, topic_name: str, event: Event):
        """
        Put a new event in the bus and notify subscribers of corresponding
        event's topic

        :param topic_name:
        :param event:
        :return:
        """

        raise NotImplemented()

