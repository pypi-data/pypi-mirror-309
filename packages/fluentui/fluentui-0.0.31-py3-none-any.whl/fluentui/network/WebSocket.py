from PySide6.QtCore import QByteArray
from PySide6.QtWebSockets import QWebSocket

from .AbsSocket import AbsSocket


class WebSocket(QWebSocket):
    def __init__(self):
        super().__init__()
        self.stateChanged.connect(self.on_state_changed)
        self.textMessageReceived.connect(self.on_text_received)
        self.binaryMessageReceived.connect(self.on_binary_received)

    def on_state_changed(self, state: AbsSocket.State):
        ...

    def on_text_received(self, text: str) -> None:
        ...

    def on_binary_received(self, data: QByteArray) -> None:
        ...

    def is_connect(self) -> bool:
        return self.state() == AbsSocket.State.Connected
