from typing import Callable

from PySide6.QtCore import Signal, QEvent
from PySide6.QtGui import QMouseEvent, QCloseEvent, QKeyEvent, QColor, QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QSizePolicy, QLayout, QGraphicsDropShadowEffect, QSystemTrayIcon, QMenu

from ..assets import QssSheet, Qss
from ..core import Margins, Qt, ObjectMix

WidgetSizeMax = 16777215


class WidgetMix(ObjectMix):
    on_close = Signal()
    on_key_enter_pressed = Signal(QWidget)
    on_clicked = Signal(QWidget)

    def __init__(
            # a、b、c、d、e、f、g、h、i、j、k、l、m、n、o、p、q、r、s、t、u、v、w、x、y、z
            self, *args,
            attrs: Qt.WidgetAttribute | list[Qt.WidgetAttribute | list[Qt.WidgetAttribute]] = None,
            color_scheme='auto',  # light, dark, auto
            shadow_effect: QGraphicsDropShadowEffect = None,
            enabled=True,
            hidden=False,
            menu_policy=Qt.ContextMenuPolicy.Default,
            layout_dir: Qt.LayoutDirection = None,
            margin='0',
            mouse_tracking=False,
            parent: QWidget = None,
            propes: dict = None,
            qss: dict = None,
            tooltip='',
            win_title='',
            win_flags: Qt.WindowType = None,

            # 大小参数
            width: int = None, height: int = None, size: str | int | tuple = None,
            min_w: int = None, min_h: int = None,
            max_w: int = None, max_h: int = None,
            hor_stretch=0, ver_stretch=0,

            # 布局参数
            row_span=1,
            column_span=1,
            align_self=Qt.AlignmentFlag(0),

            closed: Callable = None,
            destroyed: Callable[[], None] = None,
            clicked: Callable[[QWidget], None] = None,
            key_enter_pressed: Callable[[QWidget], None] = None,
            **kwargs
    ):
        if not (layout := None) and args:
            first = args[0]
            if first is None or first == () or isinstance(first, QLayout):
                args, layout = args[1:], first
        super().__init__(*args, parent=parent, **kwargs)

        self.row_span = row_span
        self.column_span = column_span
        self.align_self = align_self
        self.qss = Qss()

        # # 设置属性
        self.__init_properties(attrs, propes, qss, color_scheme)
        self.__init_size(width, height, size, min_w, min_h, max_w, max_h, hor_stretch, ver_stretch)

        # 订阅信号
        if closed: self.on_close.connect(closed)
        if clicked: self.on_clicked.connect(clicked)
        if destroyed: self.destroyed.connect(destroyed)
        if key_enter_pressed: self.on_key_enter_pressed.connect(key_enter_pressed)

        # 对象属性
        if hidden: self.setHidden(hidden)
        if win_flags is not None: self.setWindowFlags(win_flags)
        if shadow_effect:
            if not shadow_effect.parent(): shadow_effect.setParent(self)
            self.setGraphicsEffect(shadow_effect)
        self.setContentsMargins(Margins(margin))
        self.setEnabled(enabled)
        self.setToolTip(tooltip)
        self.setWindowTitle(win_title)
        self.setMouseTracking(mouse_tracking)
        self.setContextMenuPolicy(menu_policy)

        if layout:
            if layout_dir is not None:
                self.setLayoutDirection(layout_dir)
            self.setLayout(layout)

    def setStyleSheet(self, qss: dict | Qss) -> None:
        self.qss = Qss(qss) if isinstance(qss, dict) else qss
        super().setStyleSheet(f'{self.__class__.__name__} {self.qss.build()}')

    def mergeStyleSheet(self, qss: dict | Qss) -> None:
        self.qss |= qss
        super().setStyleSheet(f'{self.__class__.__name__} {self.qss.build()}')

    def event(self, e: QEvent) -> bool:
        accepted = super().event(e)
        if e.type() == QEvent.Type.Polish:
            QssSheet.apply_theme(self)
        return accepted

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)
        if self.isSignalConnected(self.on_close):
            self.on_close.emit()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        if e.key() in (Qt.Key.Enter, Qt.Key.Return):
            if self.isSignalConnected(self.on_key_enter_pressed):
                self.on_key_enter_pressed.emit(self)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setProperty('mousePressed', True)

    def mouseReleaseEvent(self, e: QMouseEvent):
        super().mouseReleaseEvent(e)
        if self.property('mousePressed'):
            self.setProperty('mousePressed', False)
            if self.isSignalConnected(self.on_clicked):
                self.on_clicked.emit(self)

    def __init_properties(self,
                          attrs: Qt.WidgetAttribute | set[Qt.WidgetAttribute | set[Qt.WidgetAttribute]] = None,
                          propes: dict = None,
                          qss: dict = None,
                          color_scheme='auto',
                          ):
        propes = propes or {}
        setattr(self, '_init_color_scheme', color_scheme)

        self.setAttribute(Qt.WidgetAttribute.DeleteOnClose)
        if attrs is not None:
            for x in attrs if isinstance(attrs, list) else [attrs]:
                if isinstance(x, set):
                    for a in x: self.setAttribute(a, False)
                    continue
                self.setAttribute(x)

        propes |= {'custom-qss': qss, 'mousePressed': False}
        for k, v in propes.items():
            self.setProperty(k, v)

    def __init_size(self, w: int | str = None, h: int | str = None,
                    size: str | int | tuple = None,
                    min_w: int = None, min_h: int = None,
                    max_w: int = None, max_h: int = None,
                    hor_stretch=0, ver_stretch=0
                    ):

        if min_w is not None or min_h is not None:
            self.setMinimumSize(min_w or WidgetSizeMax, min_h or WidgetSizeMax)
        if max_w is not None or max_h is not None:
            self.setMaximumSize(max_w or WidgetSizeMax, max_h or WidgetSizeMax)

        if isinstance(w, str) or isinstance(h, str) or hor_stretch > 0 or ver_stretch > 0:
            policy = self.sizePolicy()
            if isinstance(w, str): policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            if isinstance(h, str): policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
            if hor_stretch > 0: policy.setHorizontalStretch(hor_stretch)
            if ver_stretch > 0: policy.setVerticalStretch(ver_stretch)
            self.setSizePolicy(policy)

        if size is not None:
            if isinstance(size, str):
                if size[-1] == ',':  # 仅指定宽。如: '800,'
                    self.resize(int(size[1:]), self.height())
                elif size[0] == ',':  # 仅指定高。如: ',800'
                    self.resize(self.width(), int(size[1:]))
                else:
                    size = [int(x) for x in size.split(',')]
                    size = size * 2 if len(size) == 1 else size
                    self.resize(*size)
            else:
                if isinstance(size, int): size = (size, size)
                self.setFixedSize(*size)
        if isinstance(w, int) and isinstance(h, int):
            self.setFixedSize(w, h)
        elif isinstance(w, int):
            self.setFixedWidth(w)
        elif isinstance(h, int):
            self.setFixedHeight(h)


class Widget(WidgetMix, QWidget):
    def __init__(self, layout: QLayout = None, **kwargs):
        super().__init__(layout, **kwargs)
        self.setAttribute(Qt.WidgetAttribute.StyledBackground)


class InvisWidget(Widget):
    ...


class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self, blur_radius=1.0,
                 offset=(8.0, 8.0),
                 color=QColor.fromRgbF(0.247059, 0.247059, 0.247059, 0.705882),
                 parent=None
                 ):
        super().__init__(parent)
        self.setBlurRadius(blur_radius)
        self.setOffset(*offset)
        self.setColor(color)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self,
                 menu: QMenu = None,
                 icon: str | QIcon | QPixmap = None,
                 tooltip='',
                 activated: Callable[[QSystemTrayIcon.ActivationReason], None] = None,
                 show=False,
                 **kwargs
                 ):
        if isinstance(icon, str): icon = QIcon(icon)
        super().__init__(**kwargs)
        if activated: self.activated.connect(activated)

        self.setToolTip(tooltip)
        if icon: self.setIcon(icon)
        if menu: self.setContextMenu(menu)
        if show: self.show()
