from PyQt5 import QtCore, QtGui, QtWidgets


class TitleScreen(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(0, 8, 20);")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.label_start = QtWidgets.QLabel(self.central_widget)
        self.label_start.setGeometry(QtCore.QRect(285, 10, 709, 58))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_start.setFont(font)
        self.label_start.setStyleSheet("color: rgb(255, 195, 0);")
        self.label_start.setObjectName("labelStart")
        self.label_status = QtWidgets.QLabel(self.central_widget)
        self.label_status.setGeometry(QtCore.QRect(480, 240, 320, 33))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_status.setFont(font)
        self.label_status.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_status.setObjectName("labelStatus")
        self.button_select = QtWidgets.QPushButton(self.central_widget)
        self.button_select.setGeometry(QtCore.QRect(565, 335, 151, 47))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_select.setFont(font)
        self.button_select.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                     "alternate-background-color: rgb(0, 53, 102);\n"
                                     "color: rgb(255, 195, 0);\n"
                                     "border-color: rgb(255, 195, 0);")
        self.button_select.setObjectName("selectBtn")
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Video Stabilization Project"))
        self.label_start.setText(_translate("MainWindow", "Python Video Stabilization Project"))
        self.label_status.setText(_translate("MainWindow", "Please select a file to begin"))
        self.button_select.setText(_translate("MainWindow", "Select File"))

