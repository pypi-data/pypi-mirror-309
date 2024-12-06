from typing import Callable

from PySide6.QtWidgets import QTabWidget

from .widget import WidgetMix


class TabWidget(WidgetMix, QTabWidget):
    def __init__(self, *,
                 # tabs: [{'label': str, 'icon': QPixmap | QIcon, 'widget': QWidget}, ...]
                 tabs: list[dict] = None,
                 position=QTabWidget.TabPosition.North,
                 current_changed: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        if current_changed: self.currentChanged.connect(current_changed)

        self.setTabPosition(position)
        for x in tabs or {}:
            if icon := x.get('icon', None):
                self.addTab(x['widget'], icon, x['label'])
                continue
            self.addTab(x['widget'], x['label'])
