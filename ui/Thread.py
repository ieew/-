from PySide6.QtCore import QObject, Signal, QMutex, QThread


lock = QMutex()

class TaskWorker(QObject):
    range_requested = Signal(int)

    def __init__(self):
        super().__init__()

    def range_proc(self):
        self.signal = True
        while self.signal:
            self.range_requested.emit(())
            QThread.msleep(80)
