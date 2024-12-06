import json
from typing import Callable

from PySide6.QtCore import QEventLoop, QUrl
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply, QHttpMultiPart, QHttpPart
from PySide6.QtWidgets import QApplication

from ..core import Qt

access = QNetworkAccessManager()


class MIME:
    JSON = '"application/json"'
    MultipartForm = 'multipart/form-data'
    Form = 'application/x-www-form-urlencoded'


class Request(QNetworkRequest):
    def __init__(self, url: str,
                 method='get', *,
                 data: dict | QHttpMultiPart = None,
                 ):
        super().__init__()
        self.method = method.upper()
        self.data = data or {}

        if method == 'GET':
            if query := '&'.join(f'{k}={v}' for k, v in data.items()):
                url += f'?{query}'
        elif method == 'POST':
            if isinstance(data, QHttpMultiPart):
                self.setHeader('Content-Type', MIME.MultipartForm)
            elif not self.header('Content-Type'):
                self.setHeader('Content-Type', MIME.Form)
        self.setUrl(url)

    def send(self, *, sync=True,
             finished: Callable[[QNetworkReply], None] = None,
             download_progress: Callable[[int, int], None] = None,
             upload_progress: Callable[[int, int], None] = None,
             ) -> QNetworkReply:
        if self.method == 'POST':
            data = self.data
            match self.header('Content-Type'):
                case MIME.JSON:
                    data = json.dumps(data)
                case MIME.Form:
                    data = '&'.join(f'{k}={v}' for k, v in self.data.items())
            reply = access.post(self, data.encode())
        else:
            reply = access.get(self)

        if sync:
            QApplication.setOverrideCursor(Qt.CursorShape.Wait)
            loop = QEventLoop()

            reply.finished.connect(loop.quit)
            loop.exec(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)

            QApplication.restoreOverrideCursor()
            return reply

        if finished:
            reply.finished.connect(
                lambda: reply.error().value != 5 and finished(reply)
            )
        if upload_progress: reply.uploadProgress.connect(upload_progress)
        if download_progress: reply.downloadProgress.connect(download_progress)

        return reply

    def setHeader(self, header: QNetworkRequest.KnownHeaders | str, value: str) -> None:
        if isinstance(header, str):
            super().setRawHeader(header.encode(), value.encode())
            return
        super().setHeader(header, value.encode())

    def header(self, header: QNetworkRequest.KnownHeaders | str) -> str:
        if isinstance(header, str):
            return super().rawHeader(header).data().decode()
        return super().header(header)

    def urlString(self, options=QUrl.ComponentFormattingOption.PrettyDecoded) -> str:
        if not isinstance(options, QUrl.ComponentFormattingOption):
            options = QUrl.ComponentFormattingOption(options)
        return self.url().toString(options)


class HttpPart(QHttpPart):
    def __init__(self,
                 headers: dict[QNetworkRequest.KnownHeaders | str, str] = None,
                 body: str | bytes = None, *,
                 other: QHttpPart = None
                 ):
        if other:
            super().__init__(other)
        else:
            super().__init__()

        for key, value in headers.items():
            if isinstance(key, str):
                self.setRawHeader(key.encode(), value.encode())
                continue
            self.setHeader(key, value.encode())

        if body is not None:
            if not isinstance(body, bytes):
                body = f'{body}'.encode()
            self.setBody(body)


class HttpMultiPart(QHttpMultiPart):
    def __init__(self, *part: QHttpPart,
                 ct=QHttpMultiPart.ContentType.FormDataType,
                 parent=None
                 ):
        super().__init__(ct, parent)
        self.append(*part)

    def append(self, *part: QHttpPart) -> None:
        for x in part:
            super().append(x)
