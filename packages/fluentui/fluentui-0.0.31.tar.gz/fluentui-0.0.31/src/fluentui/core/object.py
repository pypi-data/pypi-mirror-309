from PySide6.QtCore import Signal, QMetaMethod, SIGNAL, SignalInstance


class ObjectMix:
    def __init__(self,
                 *args,
                 key='',
                 parent=None,
                 props: dict = None,
                 ):
        super().__init__(parent=parent, *args)
        self.setObjectName(key)
        for name, value in (props or {}).items():
            self.setProperty(name, value)

    def isSignalConnected(self, signal: SignalInstance) -> bool:
        return super().isSignalConnected(QMetaMethod.fromSignal(signal))

    def receivers(self, signal: Signal | str) -> int:
        if isinstance(signal, SignalInstance):
            signal = QMetaMethod.fromSignal(signal).methodSignature()
            signal = signal.toStdString()
        elif isinstance(signal, Signal):
            signal = f'{signal}'
        else:
            signal = f'{getattr(self.__class__, signal)}'
        return super().receivers(SIGNAL(signal))
