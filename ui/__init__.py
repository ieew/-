from PySide6.QtWidgets import QMainWindow, QTextEdit
from PySide6.QtGui import QKeyEvent, QResizeEvent, QInputMethodEvent, QKeyEvent, QShortcut, QKeySequence, QGuiApplication, QCloseEvent
from PySide6.QtCore import QRect, QThread, Signal

from .Thread import TaskWorker
from .window import UiMainWindow
import time


class MainWindow(QMainWindow):
    thread_range = Signal()

    __start_time = 0
    __hit_count = 0

    def __init__(self) -> None:
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)
        self.c = 0
        self.setup_thread()
        self.ui.input_box.input_method_hook = self.input_hook
        self.ui.input_box.key_press_hook = self.key_press_hook
        self.ShortAlt_E = QShortcut(QKeySequence("Alt+E"), self)
        self.ShortAlt_E.activated.connect(self.Alt_E)
        self.ui.input_box.textChanged.connect(self.text_overloading)
        self.ui.input_box.cursorPositionChanged.connect(self.cursor_overloading)

    def setup_thread(self):
        self.thread1 = QThread(self)
        self.range_thread = TaskWorker()
        self.range_thread.moveToThread(self.thread1)
        self.range_thread.range_requested.connect(self.update_info)
        self.thread_range.connect(self.range_thread.range_proc)

    def resizeEvent(self, event: QResizeEvent) -> None:
        h = 320 / 600 * event.size().height()
        self.ui.horizontalLayoutWidget.setGeometry(50, 0, event.size().width() - 60, 20)
        self.ui.progress_bar.setGeometry(QRect(10, 20, event.size().width() - 20, 20))

        self.ui.display_box.setGeometry(QRect(10, 40, event.size().width() - 20, h))
        self.ui.input_box.setGeometry(QRect(10, h + 50, event.size().width() - 20, event.size().height() - 80 - h))
        return super().resizeEvent(event)

    def key_press_hook(self, e: QKeyEvent):
        if self.ui.display_box.toPlainText() != self.ui.input_box.toPlainText() and e.text() != u"\u0016":
            QTextEdit.keyPressEvent(self.ui.input_box, e)

    def input_hook(self, arg__1: QInputMethodEvent):
        if self.ui.input_box.isReadOnly():
            arg__1.setCommitString("")

        if self.ui.display_box.toPlainText() != self.ui.input_box.toPlainText():
            QTextEdit.inputMethodEvent(self.ui.input_box, arg__1)

    def text_overloading(self):
        if not self.thread1.isRunning():
            self.thread1.start()
            self.thread_range.emit()
            self.__start_time = time.time()
            self.__hit_count = 0
        else:
            self.__hit_count += 1

        value = len(self.ui.input_box.toPlainText()) / len(self.ui.display_box.toPlainText()) * self.ui.progress_bar.maximum() - 1
        self.ui.progress_bar.setValue(value if value > 0 else 0)
        if self.ui.display_box.toPlainText() == self.ui.input_box.toPlainText():
            self.ui.input_box.setReadOnly(True)
            self.input_ReadOnlyChange_event()
        # cursor = self.ui.display_box.textCursor()
        # cursor.movePosition(self.ui.input_box.textCursor().MoveOperation.Right, self.ui.input_box.textCursor().MoveMode.MoveAnchor, 1)
        # cursor.insertText(f"{self.c}")
        # self.c += 1

    def cursor_overloading(self):
        cursor = self.ui.display_box.textCursor()
        cursor.movePosition(self.ui.input_box.textCursor().MoveOperation.Right, self.ui.input_box.textCursor().MoveMode.MoveAnchor, 1)

    def input_ReadOnlyChange_event(self):
        if self.thread1.isRunning():
            self.range_thread.signal = False
            self.thread1.quit()

    def Alt_E(self):
        clipboard = QGuiApplication.clipboard()
        self.ui.display_box.setHtml(f"{self.ui.display_box.textstart}{clipboard.text()}{self.ui.display_box.textend}")
        self.ui.input_box.setReadOnly(False)
        self.ui.input_box.setText("")

    def update_info(self):
        if self.ui.display_box.toPlainText() == self.ui.input_box.toPlainText():
            self.range_thread.signal = False
        else:
            t = time.time() - self.__start_time
            input_num = len(self.ui.input_box.toPlainText())
            self.ui.label["速度"].setText(f"速度: {round(float(input_num) / t * 60, ndigits=2)}")
            self.ui.label["击键"].setText(f"击键: {round(self.__hit_count / t, ndigits=2)}")
            if input_num > 0:
                self.ui.label["码长"].setText(f"码长: {round(self.__hit_count / input_num, ndigits=2)}")
