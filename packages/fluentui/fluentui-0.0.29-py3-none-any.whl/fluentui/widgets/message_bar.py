from enum import Enum
from functools import partial

from PySide6.QtCore import QPoint
from PySide6.QtGui import QMouseEvent

from .button import PrimaryButton, Button, QAbstractButton
from .dialog import Dialog
from .label import Label
from .layout import Row, Column, Stretch
from .widget import Widget, ShadowEffect
from ..core import Qt
from ..gui import Color


class ButtonRole(Enum):
    OK = '确定'
    Cancel = '取消'


class MessageBar(Dialog):
    def __init__(self,
                 title='',
                 message='',
                 intent='info',
                 buttons: ButtonRole | QAbstractButton | list = ButtonRole.OK,
                 parent=None
                 ):
        self.__drag_pos: QPoint = None
        self.clicked_button = None

        super().__init__(
            Row(self.__create_frame(title, message, intent, buttons)),
            attrs=[Qt.WidgetAttribute.Translucent, {Qt.WidgetAttribute.DeleteOnClose}],
            parent=parent,
            width=600,
            size=',24',
            margin='0 8 8 0',
            win_flags=Qt.WindowType.Dialog | Qt.WindowType.Frameless
        )

        self.destroyed.connect(lambda: print('MessageBar Destroyed'))

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)
        if e.button() == Qt.MouseButton.Left:
            self.__drag_pos = e.globalPosition().toPoint() - self.geometry().topLeft()

    def mouseMoveEvent(self, e: QMouseEvent):
        super().mouseMoveEvent(e)
        if e.buttons() & Qt.MouseButton.Left and self.__drag_pos:
            self.move(e.globalPosition().toPoint() - self.__drag_pos)

    def mouseReleaseEvent(self, e: QMouseEvent):
        super().mouseReleaseEvent(e)
        if e.button() == Qt.MouseButton.Left:
            self.__drag_pos = None

    @classmethod
    def info(cls, title: str, message: str, parent=None) -> bool:
        return cls(title, message, 'info', parent=parent).exec()

    @classmethod
    def warning(cls, title: str, message: str, parent=None) -> bool:
        return cls(title, message, 'warning', parent=parent).exec()

    @classmethod
    def error(cls, title: str, message: str, parent=None) -> bool:
        return cls(title, message, 'error', parent=parent).exec()

    @classmethod
    def success(cls, title: str, message: str, parent=None) -> bool:
        return cls(title, message, 'success', parent=parent).exec()

    @classmethod
    def question(cls, title: str, message: str, parent=None) -> bool:
        buttons = [ButtonRole.OK, ButtonRole.Cancel]
        return cls(title, message, 'info', buttons, parent).exec() == ButtonRole.OK

    def exec(self) -> Button | ButtonRole:
        super().exec()
        self.deleteLater()
        return self.clicked_button

    def __create_frame(self,
                       title='',
                       message='',
                       intent='info',
                       buttons: ButtonRole | QAbstractButton | list = None,
                       ):
        if not isinstance(buttons, list): buttons = [buttons]
        buttons.reverse()

        for i, x in enumerate(buttons):
            if isinstance(x, ButtonRole):
                match x.name:
                    case 'OK':
                        buttons[i] = PrimaryButton(x.value)
                    case 'Cancel':
                        buttons[i] = Button(x.value)
            buttons[i].clicked.connect(partial(self.__on_clicked, x))

        match intent:
            case 'info':
                qss = {'background': '#f5f5f5', 'border': f'2 solid #d1d1d1'}
            case 'warning':
                qss = {'background': '#fff9f5', 'border': '2 solid #fdcfb4'}
            case 'error':
                qss = {'background': '#fdf3f4', 'border': '2 solid #eeacb2'}
            case _:  # success
                qss = {'background': '#f1faf1', 'border': '2 solid #9fd89f'}

        return Widget(
            Column(
                Row(
                    Label(
                        f'<b>{title}</b>',
                        align=Qt.Alignment.Top,
                        interaction_flag=Qt.TextInteraction.SelectableByMouse,
                    ),
                    Label(
                        message,
                        word_wrap=True,
                        hor_stretch=1,
                        align=Qt.Alignment.Top,
                        interaction_flag=Qt.TextInteraction.Browser
                    ),
                    spacing=6
                ),
                Row(Stretch(), *buttons, margin='16 0 0', spacing=6),
            ),
            qss=qss | {'border-radius': 5},
            margin='28 14',
            shadow_effect=ShadowEffect(8, (2, 2), Color(alpha=0.12))
        )

    def __on_clicked(self, sender: QAbstractButton | ButtonRole):
        self.clicked_button = sender
        self.close()
