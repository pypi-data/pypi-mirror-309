from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from .widget import WidgetMix


class Label(WidgetMix, QLabel):
    def __init__(self,
                 text='',
                 align: Qt.AlignmentFlag = None,
                 word_wrap=False,
                 interaction_flag: Qt.TextInteractionFlag = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setText(text)
        if interaction_flag is not None: self.setTextInteractionFlags(interaction_flag)
        if align is not None: self.setAlignment(align)
        self.setWordWrap(word_wrap)


class Line(WidgetMix, QLabel):
    def __init__(self, orient='hor', thick=1, **kwargs):
        kwargs['height' if orient == 'hor' else 'width'] = thick
        super().__init__(**kwargs)


class Horline(Line):
    def __init__(self, thick=1, **kwargs):
        super().__init__(orient='hor', thick=thick, **kwargs)


class Verline(Line):
    def __init__(self, thick=1, **kwargs):
        super().__init__(orient='ver', thick=thick, **kwargs)
