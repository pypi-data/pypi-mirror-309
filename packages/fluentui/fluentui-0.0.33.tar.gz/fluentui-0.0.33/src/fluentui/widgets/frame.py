from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea

from .widget import WidgetMix


class FrameMix(WidgetMix):
    def __init__(self: QFrame, frame_shape: QFrame.Shape = None, **kwargs):
        super().__init__(**kwargs)
        if frame_shape is not None:
            self.setFrameShape(frame_shape)


class Frame(FrameMix, QFrame):
    ...


class AbsScrollAreaMix(FrameMix):
    def __init__(self,
                 hor_scroll_bar_policy: Qt.ScrollBarPolicy = None,
                 ver_scroll_bar_policy: Qt.ScrollBarPolicy = None,
                 **kwargs):
        super().__init__(**kwargs)
        if hor_scroll_bar_policy is not None:
            self.setHorizontalScrollBarPolicy(hor_scroll_bar_policy)
        if ver_scroll_bar_policy is not None:
            self.setVerticalScrollBarPolicy(ver_scroll_bar_policy)


class ScrollArea(AbsScrollAreaMix, QScrollArea):
    ...
