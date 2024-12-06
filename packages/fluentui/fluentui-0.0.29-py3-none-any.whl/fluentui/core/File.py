from PySide6.QtCore import QFile, QIODevice


class File(QFile):
    def __init__(self, name: str, *, mode: QIODevice.OpenModeFlag = None, parent=None):
        super().__init__(name, parent)
        if mode: self.open(mode)
