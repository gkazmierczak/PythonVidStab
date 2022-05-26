# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\titlescreen.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
class TitleScreen(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(0, 8, 20);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelStart = QtWidgets.QLabel(self.centralwidget)
        self.labelStart.setGeometry(QtCore.QRect(285, 10, 709, 58))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.labelStart.setFont(font)
        self.labelStart.setStyleSheet("color: rgb(255, 195, 0);")
        self.labelStart.setObjectName("labelStart")
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setGeometry(QtCore.QRect(480, 240, 320, 33))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelStatus.setFont(font)
        self.labelStatus.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelStatus.setObjectName("labelStatus")
        self.selectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.selectBtn.setGeometry(QtCore.QRect(565, 335, 151, 47))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.selectBtn.setFont(font)
        self.selectBtn.setStyleSheet("background-color: rgb(0, 29, 61);\n"
"alternate-background-color: rgb(0, 53, 102);\n"
"color: rgb(255, 195, 0);\n"
"border-color: rgb(255, 195, 0);")
        self.selectBtn.setObjectName("selectBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Video Stabilization Project"))
        self.labelStart.setText(_translate("MainWindow", "Python Video Stabilization Project"))
        self.labelStatus.setText(_translate("MainWindow", "Please select a file to begin"))
        self.selectBtn.setText(_translate("MainWindow", "Select File"))
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = TitleScreen()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

