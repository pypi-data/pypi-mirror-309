from typing import Any


class EventContent:

    def __init__(self, content: Any, content_type: str):

        self.__content = content
        self.__content_type = content_type


    @property
    def content(self) -> Any:
        return self.__content

    @property
    def content_type(self) -> str:
        return self.__content_type
