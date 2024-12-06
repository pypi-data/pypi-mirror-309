from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider

from .widget import WidgetMix, QssSheet


class Slider(WidgetMix, QSlider):
    def __init__(self,
                 value=0,
                 minimum=0,
                 maximum=100,
                 orient=Qt.Orientation.Horizontal,
                 value_changed: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(orient, **kwargs)
        if value_changed: self.valueChanged.connect(value_changed)

        self.setRange(minimum, maximum)
        self.setValue(int(value))
        QssSheet.Slider.apply(self)
