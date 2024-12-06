from typing import Callable

from PySide6.QtWidgets import QTabBar

from .widget import WidgetMix


class TabBar(WidgetMix, QTabBar):
    def __init__(self,
                 tabs: list[dict] = None,
                 current_changed: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if current_changed: self.currentChanged.connect(current_changed)
        for x in tabs or {}:
            if icon := x.get('icon', None):
                self.addTab(icon, x['label'])
                continue
            self.addTab(x['label'])
