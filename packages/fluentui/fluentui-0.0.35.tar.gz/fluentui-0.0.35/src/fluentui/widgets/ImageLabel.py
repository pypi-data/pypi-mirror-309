from hashlib import md5
from pathlib import Path
from threading import Thread
from typing import Callable

from fluentui import Qt
from PySide6.QtCore import QUrl, QByteArray, QSize, QBuffer, QIODevice, Signal
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager

from .label import Label
from ..gui import Pixmap


class ImageLabel(Label):
    netManager = QNetworkAccessManager()
    done = Signal(QPixmap)
    CACHE_PATH = Path.home() / f'AppData/Local/images_cache'
    CACHE_PATH.mkdir(parents=True, exist_ok=True)

    def __init__(self,
                 src='',
                 on_done: Callable[[QPixmap], None] = None,
                 **kwargs
                 ):
        kwargs.setdefault('align', Qt.Alignment.Center)
        super().__init__(**kwargs)
        self.src = ''
        self.default = QPixmap(f':/images/default.png')
        self.data = b''  # 原图数据
        self.__reply: QNetworkReply = None

        self.destroyed.connect(lambda: self.__reply and self.__reply.abort())
        self.done.connect(lambda pix: self.__on_done(pix, on_done))

        self.setPixmap(self.default)
        self.request(src)

    def __on_done(self, pix: QPixmap, done: Callable):
        try:
            not self.setPixmap(pix) and done and done(pix)
        except RuntimeError as _:
            ...

    def request(self, src: str | Path | bytes) -> None:
        if isinstance(src, str):
            if not src or src == self.src: return
            self.src = src
        else:
            self.data = src.read_bytes() if isinstance(src, Path) else src
            self.setPixmap(pixmap := Pixmap.from_data(self.data))
            self.done.emit(pixmap)
            return

        ext = Path(src).suffix.split('?')[0]  # 图片扩展名
        if not (path := self.CACHE_PATH / (md5(src.encode()).hexdigest() + ext)).exists():
            if (p := Path(src)).exists():  # 如果缓存路径不存在，则判断系统路径
                path = p

        if path.exists():
            Thread(target=self.request, args=(path,)).start()
            return

        self.__reply = self.netManager.get(QNetworkRequest(QUrl(src)))
        self.__reply.finished.connect(lambda: {
            Thread(target=self.__on_finished, args=(path, self.__reply.readAll())).start()
        })
        return

    def __on_finished(self, path: Path, data: QByteArray) -> None:
        """ 下载完成 """
        try:
            if data.isEmpty() or data.isNull():  # 图片数据为空
                self.done.emit(QPixmap())
                return
            path.write_bytes(data.data())  # 保存图片
            self.data = data
            self.done.emit(Pixmap.from_data(data))
        except RuntimeError as _:
            ...

    def setPixmap(self, pixmap: QPixmap) -> None:
        if pixmap.isNull():
            self.data = QByteArray()
            pixmap = self.default

        super().setPixmap(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.Smooth
        ))

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.setPixmap(self.pixmap())

    def isNull(self) -> bool:
        return self.pixmap().isNull()

    def pixel_width(self) -> int:
        return self.pixmap().width()

    def pixel_height(self) -> int:
        return self.pixmap().height()

    def pixel_size(self) -> QSize:
        return self.pixmap().size()

    def thumbnail(self, format_='JPG', quality=-1) -> bytes:
        """ 缩略图数据。质量因子必须在 [0,100] 或 -1 的范围内 """
        if (isnull := self.pixmap().isNull()) or quality == 100:
            return b'' if isnull else self.data

        buffer = QBuffer(data := QByteArray())
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        self.pixmap().save(buffer, format_, 100)

        buffer.close()
        return data.data()

    def origin(self, format_='JPG') -> bytes:
        """ 原图数据 """
        return self.thumbnail(format_, 100)
