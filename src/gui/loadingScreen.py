from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie
from .scrollableLabel import ScrollableLabel
import os


class LoadingScreen(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet("background-color: rgb(0, 8, 20);")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.label_status = QtWidgets.QLabel(self.central_widget)
        self.label_status.setGeometry(QtCore.QRect(415, 60, 451, 40))
        self.label_status.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 24pt \"MS Shell Dlg 2\";")
        self.label_status.setObjectName("lStatus")
        self.label_animation = QtWidgets.QLabel(self.central_widget)
        self.label_animation.setGeometry(QtCore.QRect(440, 160, 400, 400))
        self.label_animation.setText("")
        self.label_animation.setObjectName("lAnim")
        self.button_cancel = QtWidgets.QPushButton(self.central_widget)
        self.button_cancel.setGeometry(QtCore.QRect(0, 0, 90, 40))
        self.button_cancel.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                     "border: 1px solid rgb(255, 195, 0);\n"
                                     "color: rgb(255, 195, 0);\n"
                                     "font: 20pt \"MS Shell Dlg 2\";")
        self.button_cancel.setObjectName("btnCancel")
        self.scrollable_label = ScrollableLabel(parent=self.central_widget)
        self.scrollable_label.setGeometry(QtCore.QRect(970, 400, 300, 300))
        self.scrollable_label.setWidgetResizable(True)
        self.scrollable_label.setObjectName("scrollableLabel")
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../resource/loading.gif'))
        self.movie = QMovie(path)
        self.movie.setScaledSize(QtCore.QSize(400, 400))
        self.label_animation.setMovie(self.movie)
        self.start_animation()
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Video Stabilization Project"))
        self.label_status.setText(_translate("MainWindow", "Your video is being processed..."))
        self.button_cancel.setText(_translate("MainWindow", "Cancel"))

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()

    def append_text(self, text):
        self.scrollable_label.append_text(text)

