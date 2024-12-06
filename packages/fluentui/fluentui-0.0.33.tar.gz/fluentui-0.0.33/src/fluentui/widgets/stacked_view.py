from PySide6.QtWidgets import QStackedWidget, QWidget

from .frame import FrameMix


class StackedView(FrameMix, QStackedWidget):
    def __init__(self, *stack: QWidget, **kwargs):
        super().__init__(**kwargs)
        for x in stack or ():
            self.addWidget(x)
