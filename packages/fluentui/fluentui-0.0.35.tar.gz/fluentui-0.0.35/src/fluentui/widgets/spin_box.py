from PySide6.QtWidgets import QSpinBox

from .widget import WidgetMix, QssSheet


class AbsSpinBoxMix(WidgetMix):
    ...


class SpinBox(AbsSpinBoxMix, QSpinBox):
    def __init__(self, value=0, *,
                 minimum=0,
                 maximum=99,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setRange(minimum, maximum)
        self.setValue(value)
        QssSheet.apply_theme(self)
