from typing import Callable

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QColorDialog, QDialog, QLayout

from .widget import WidgetMix, QssSheet


class DialogMix(WidgetMix):
    def __init__(self,
                 layout: QLayout = None, *,
                 accepted: Callable = None,
                 rejected: Callable = None,
                 finished: Callable[[int], None] = None,
                 **kwargs
                 ):
        super().__init__(layout, **kwargs)
        if accepted: self.accepted.connect(accepted)
        if rejected: self.rejected.connect(rejected)
        if finished: self.finished.connect(finished)
        QssSheet.Widget.apply(self)


class Dialog(DialogMix, QDialog):
    ...


class ColorDialog(DialogMix, QColorDialog):
    def __init__(self, color: QColor | str = '#fff',
                 color_selected: Callable[[QColor], None] = None,
                 **kwargs
                 ):
        if isinstance(color, str): color = QColor(color)
        QColorDialog.__init__(self, color)
        super().__init__(**kwargs)
        if color_selected: self.colorSelected.connect(color_selected)

    @staticmethod
    def getColor(initial='#fff',
                 parent: QWidget = None,
                 title='',
                 options=QColorDialog.ColorDialogOption.ShowAlphaChannel
                 ) -> QColor:
        return super().getColor(QColor(initial), parent, title, options)
