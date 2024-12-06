from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox

from .widget import WidgetMix


class CheckBox(WidgetMix, QCheckBox):
    def __init__(self, text='', *,
                 tristate=False,
                 state=Qt.CheckState.Unchecked,
                 state_changed: Callable[[Qt.CheckState], ...] = None,
                 **kwargs
                 ):
        super().__init__(text, **kwargs)
        if state_changed: self.stateChanged.connect(state_changed)
        self.setTristate(tristate)
        self.setCheckState(state)
