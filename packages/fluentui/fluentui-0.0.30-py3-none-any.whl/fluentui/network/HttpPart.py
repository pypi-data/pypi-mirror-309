from PySide6.QtNetwork import QHttpPart, QNetworkRequest


class HttpPart(QHttpPart):
    def __init__(self, other: QHttpPart = None,
                 headers: dict[QNetworkRequest.KnownHeaders | str, str] = None,
                 body: str | bytes = None,
                 ):
        super().__init__(other) if other else super().__init__()

        for key, value in headers.items():
            if isinstance(key, str):
                self.setRawHeader(key.encode(), value.encode())
                continue
            self.setHeader(key, value.encode())

        if body is not None:
            if not isinstance(body, bytes):
                body = f'{body}'.encode()
            self.setBody(body)
