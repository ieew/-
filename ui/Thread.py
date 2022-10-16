from typing import Optional
from PySide6.QtCore import QObject, Signal, QMutex
from time import sleep

from .controls import TextBrowser, TextEdit


lock = QMutex()


class TaskWorker(QObject):
    range_requested = Signal(int)

    def __init__(self):
        super().__init__()

    def range_proc(self):
        self.signal = True
        while self.signal:
            self.range_requested.emit(())
            sleep(0.1)
