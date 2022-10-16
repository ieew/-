from typing import Callable, Dict, List
from PySide6.QtWidgets import QTextBrowser, QTextEdit
from PySide6.QtCore import QRect, Qt, QEvent
from PySide6.QtGui import QFont, QKeyEvent, QInputMethodEvent, QEnterEvent, QMouseEvent, QFocusEvent, QMoveEvent, QResizeEvent


class TextBrowser(QTextBrowser):
    def set_ui(self):
        self.setObjectName("display_box")
        self.setGeometry(QRect(10, 40, 780, 320))
        self.textstart = u"""<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n
<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n
p, li { white-space: pre-wrap; }\n
hr { height: 1px; border-width: 0; }\n
</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:20pt; font-weight:400; font-style:normal;\">\n
<p style=\" margin-top:13px; margin-bottom:13px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"""
        self.textend = u"</p></body></html>"

        self.setHtml(f"{self.textstart}欢迎使用竹竹跟打器，当前载入的是测试文章。快捷键：载文(Alt+E){self.textend}")
        self.setTextInteractionFlags(Qt.NoTextInteraction)

class TextEdit(QTextEdit):
    input_method_hook: List[Callable]
    events: Dict[QEvent, List[Callable]] = {}

    def set_ui(self):
        self.setObjectName(u"Input_box")
        self.setGeometry(QRect(10, 370, 780, 200))
        font1 = QFont()
        font1.setPointSize(15)
        self.setFont(font1)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.input_method_hook = None
        self.key_press_hook = None
        self.key_release_hook = None

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if self.key_press_hook:
            self.key_press_hook(e)

    def inputMethodEvent(self, arg__1: QInputMethodEvent) -> None:
        if self.input_method_hook:
            self.input_method_hook(arg__1)

    def event(self, e: QEvent) -> bool:
        if e.type() in self.events:
            for i in self.events[e.type()]:
                i(e)
        return super().event(e)

    def decorate(self, *type: QEvent.Type):
        def _(fun: Callable):
            for i in type:
                if i not in self.events:
                    self.events[i] = []
                self.events[i].append(fun)
        return _