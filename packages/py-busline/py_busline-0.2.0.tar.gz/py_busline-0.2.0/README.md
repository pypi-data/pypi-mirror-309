from src.eventbus_client.eventbus_client import EventBusClient

# Busline for Python

Agnostic eventbus for Python.

## Local EventBus

```python
from src.eventbus.async_local_eventbus import AsyncLocalEventBus
from src.eventbus_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from src.event.event import Event
from src.eventbus_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber


local_eventbus_instance = AsyncLocalEventBus()       # singleton

def callback(e: Event):
    print(e)

subscriber = LocalEventBusClosureSubscriber(local_eventbus_instance, callback)
publisher = LocalEventBusPublisher(local_eventbus_instance)

await subscriber.subscribe("test-topic")

await publisher.publish("test-topic", Event())      # publish empty event
```

## Agnostic EventBus

Implement business logic of your `Publisher` and `Subscriber` and... done. Nothing more.

```python
from src.event.event import Event
from src.eventbus_client.publisher.publisher import Publisher

class YourEventBusPublisher(Publisher):

    async def _internal_publish(self, topic_name: str, event: Event):
        pass        # send events to your eventbus (maybe in cloud?)
```

```python
from src.eventbus_client.subscriber.subscriber import Subscriber
from src.event.event import Event

class YourEventBusSubscriber(Subscriber):
    
    async def on_event(self, topic_name: str, event: Event):
        pass        # receive your events
```

You could create a client to allow components to use it instead of become a publisher or subscriber.

```python

class YourEventBusClient(YourEventBusPublisher, YourEventBusSubscriber):
    pass
```





