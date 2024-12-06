from PySide6.QtWidgets import QWidget, QSplitter

from .frame import FrameMix
from ..core import Qt


class Splitter(FrameMix, QSplitter):
    def __init__(self, *split: QWidget,
                 sizes: list[int] = None,
                 handle_width=5,
                 children_collapsible=True,
                 orient=Qt.Orientation.Hor,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setOrientation(orient)
        self.setHandleWidth(handle_width)
        self.setChildrenCollapsible(children_collapsible)

        if sizes: self.setSizes(sizes or [])
        for x in split or []: self.addWidget(x)
