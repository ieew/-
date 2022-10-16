from typing import Dict, Optional
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout, QLabel, QProgressBar, QStatusBar
from PySide6.QtCore import QRect, QCoreApplication, Qt, QMetaObject

from .controls import TextBrowser, TextEdit


class UiMainWindow:
    
    def setup_ui(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "竹竹跟打器", None))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 0, 740, 20))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.push_button = QPushButton(self.centralwidget)
        self.push_button.setObjectName("pushButton")
        self.push_button.setGeometry(QRect(10, 0, 40, 20))
        self.push_button.setText(QCoreApplication.translate("MainWindow", "设置", None))

        self.label: Dict[str, Optional[QLabel]] = {"速度": None, "击键": None, "码长": None}

        for i in self.label:
            self.label[i] = QLabel(self.horizontalLayoutWidget)
            self.label[i].setObjectName(i)
            self.label[i].setAlignment(Qt.AlignCenter)
            self.label[i].setText(f"{i}: 0.00")
            self.horizontalLayout.addWidget(self.label[i])
        else:
            self.label["速度"].setStyleSheet("QLabel { background-color: #dadada }")
            self.label["击键"].setStyleSheet("QLabel { background-color: #c5c5c5 }")
            self.label["码长"].setStyleSheet("QLabel { background-color: #dfdfdf }")

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setGeometry(QRect(10, 20, 780, 20))
        self.progress_bar.setStyleSheet("QProgressBar { border: 0px solid grey; border-radius: 0px; background-color: #f2f2f2} QProgressBar::chunk { background-color: #a0a0a0; width: 20px;}")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(99)
        self.progress_bar.setValue(0)

        self.display_box = TextBrowser(self.centralwidget)
        self.display_box.set_ui()

        self.input_box = TextEdit(self.centralwidget)
        self.input_box.set_ui()

        QWidget.setTabOrder(self.input_box, self.display_box)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet("QStatusBar { background-color: #e7e7e7 }")
        MainWindow.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(MainWindow)
