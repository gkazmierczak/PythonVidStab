from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ScrollableLabel(QScrollArea):

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        layout = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 12pt \"MS Shell Dlg 2\";")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

    def append_text(self, text):
        self.label.setText(self.label.text() + "\n" + text)

    def clear_text(self):
        self.label.setText("")
