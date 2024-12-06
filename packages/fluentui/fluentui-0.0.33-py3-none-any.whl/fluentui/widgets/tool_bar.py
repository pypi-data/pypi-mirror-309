from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QToolBar

from .widget import WidgetMix
from ..gui import Action


class ToolBar(WidgetMix, QToolBar):
    def __init__(self, title='', *,
                 icon_size: int | tuple[int, int] = None,
                 triggered: Callable[[Action], None] = None,
                 **kwargs
                 ):
        if isinstance(icon_size, int):
            icon_size = (icon_size, icon_size)
        super().__init__(title, **kwargs)

        if triggered: self.actionTriggered.connect(triggered)
        if icon_size is not None:
            self.setIconSize(QSize(*icon_size))
