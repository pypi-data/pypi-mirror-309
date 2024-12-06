from typing import Callable, Iterable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from .widget import WidgetMix


class Menu(WidgetMix, QMenu):
    def __init__(self, title='',
                 actions: QAction | Iterable[QAction] = None,
                 on_triggered=Callable[[QAction], None],
                 **kwargs
                 ):
        super().__init__(title, **kwargs)
        if on_triggered:
            self.triggered.connect(on_triggered)

        self.addActions(actions or [])
