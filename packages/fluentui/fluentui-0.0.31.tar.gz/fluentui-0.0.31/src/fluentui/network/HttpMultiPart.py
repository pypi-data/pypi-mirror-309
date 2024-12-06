from PySide6.QtCore import QObject
from PySide6.QtNetwork import QHttpMultiPart

from .HttpPart import HttpPart


class HttpMultiPart(QHttpMultiPart):
    def __init__(self, content_type=QHttpMultiPart.ContentType.FormDataType, *,
                 items: list[HttpPart] = None,
                 parent: QObject = None):
        super().__init__(content_type, parent)
        self.append(items or [])

    def append(self, item: HttpPart | list[HttpPart]) -> None:
        for x in item if isinstance(item, list) else [item]:
            super().append(x)
