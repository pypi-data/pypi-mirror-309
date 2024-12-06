import uuid
from src.event.event_content import EventContent
from src.event.event_metadata import EventMetadata


class Event:

    def __init__(self, content: EventContent = None, metadata: EventMetadata = EventMetadata()):

        self._identifier = str(uuid.uuid4())
        self._content = content
        self._metadata = metadata


    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def content(self) -> EventContent:
        return self._content

    @property
    def metadata(self) -> EventMetadata:
        return self._metadata
