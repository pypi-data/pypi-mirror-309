from functools import partial
from operator import setitem
from typing import Callable

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QImage, QColor, QValidator, QIntValidator
from PySide6.QtNetwork import QNetworkReply, QNetworkRequest, QNetworkAccessManager
from PySide6.QtWidgets import QTextEdit, QLineEdit
from bs4 import BeautifulSoup

from .frame import AbsScrollAreaMix
from .widget import WidgetMix
from ..gui import TextDocument


class Input(WidgetMix, QLineEdit):
    def __init__(self, text: object = '', *,
                 placeholder='',
                 read_only=False,
                 text_changed: Callable[[str], None] = None,
                 validator: QValidator = None,
                 **kwargs
                 ):
        super().__init__(f'{text}', **kwargs)
        if text_changed: self.textChanged.connect(text_changed)
        if validator is not None: self.setValidator(validator)

        self.setReadOnly(read_only)
        self.setPlaceholderText(placeholder)

    def setText(self, text: object, block_signals=False):
        super().setText(f'{text}')
        if block_signals: self.blockSignals(True)
        self.setCursorPosition(0)
        if block_signals: self.blockSignals(False)


class IntInput(Input):
    def __init__(self, text='', **kwargs):
        super().__init__(text, **kwargs)
        self.setValidator(QIntValidator())


class Textarea(AbsScrollAreaMix, QTextEdit):
    downer = QNetworkAccessManager()

    def __init__(self,
                 text='', *,
                 placeholder='',
                 text_color='',
                 font_pixel=0,
                 read_only=False,
                 undo_redo_enabled=True,
                 accept_rich_text=True,
                 on_text_change: Callable[[], None] = None,
                 align: Qt.AlignmentFlag = None,
                 on_selection_changed: Callable = None,
                 on_cursor_moved: Callable = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.reply: list[QNetworkReply] = []

        if on_text_change: self.textChanged.connect(on_text_change)
        if on_cursor_moved: self.cursorPositionChanged.connect(on_cursor_moved)
        if on_selection_changed: self.selectionChanged.connect(on_selection_changed)

        self.setText(text)
        self.setReadOnly(read_only)
        self.setAcceptRichText(accept_rich_text)
        self.setUndoRedoEnabled(undo_redo_enabled)
        self.document().setDocumentMargin(0)
        self.setPlaceholderText(placeholder)

        if text_color: self.setTextColor(QColor(text_color))
        if font_pixel:
            font = self.font()
            font.setPixelSize(font_pixel)
            self.setFont(font)
        if align is not None: self.setAlignment(align)

        self.setViewportMargins(8, 4, 8, 4)

    def setText(self, text: str):
        super().setText(text)
        for x in BeautifulSoup(text, 'lxml').find_all('img'):
            if not (url := QUrl(x.get('src', ''))).isValid():
                continue
            if url.scheme() not in ("http", "https"):
                continue
            if self.document().resource(TextDocument.ResourceType.Image, url):
                continue
            reply = self.downer.get(QNetworkRequest(url))
            reply.finished.connect(partial(self.on_downloaded, reply))
            self.reply.append(reply)

    def content(self) -> str:
        if self.document().isEmpty():
            return ''

        contents = []
        for p in BeautifulSoup(self.toHtml(), 'lxml').find_all('p'):
            del p['style']
            for span in p.find_all('span'):
                style: str = span['style']
                if setitem(span, 'style', style) or style == "":
                    span.unwrap()
            text = f'{p}'.rstrip()
            contents.append(f'<p>{'\u200B'}</p>' if text == '<p><br/></p>' else text)
        return '\n'.join(x for x in contents)

    def on_downloaded(self, reply: QNetworkReply):
        image = QImage()
        if not image.loadFromData(reply.readAll()):
            return

        try:
            self.reply.remove(reply)
            doc = self.document()
            doc.addResource(TextDocument.ResourceType.Image, reply.url(), image)
            doc.setTextWidth(doc.idealWidth())
        except (RuntimeError, ValueError) as _:
            ...

    def adaptive_height(self: QTextEdit, width=0) -> None:
        if (d := self.document()) and width > 0:
            d.setTextWidth(width)
            d.setTextWidth(idea_width := int(d.idealWidth()))
            self.setFixedSize(idea_width, d.size().toSize().height())
        else:
            d.setTextWidth(d.idealWidth())
            self.setFixedHeight(d.size().toSize().height())

    def __del__(self):
        for x in self.reply:
            x.abort()
