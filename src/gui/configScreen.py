# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\screen1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QStyle
from utils import durationFromMs


class ConfigScreen(object):
    videoPath = None
    playbackPausedBySliderEvent=False
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet("background-color: rgb(0, 8, 20);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gbOptions = QtWidgets.QGroupBox(self.centralwidget)
        self.gbOptions.setGeometry(QtCore.QRect(1080, 0, 191, 341))
        self.gbOptions.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "border: 0px;"
                                     "background-color: rgb(0, 8, 20);")
        self.gbOptions.setTitle("")
        self.gbOptions.setAlignment(QtCore.Qt.AlignCenter)
        self.gbOptions.setObjectName("gbOptions")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.gbOptions)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 0, 191, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.cbShowTracking = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbShowTracking.setObjectName("cbShowTracking")
        self.cbShowTracking.setStyleSheet("margin-left:50px")
        self.cbShowTracking.setChecked(False)
        self.verticalLayout.addWidget(self.cbShowTracking)

        self.cbAudio = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbAudio.setObjectName("cbAudio")
        self.cbAudio.setStyleSheet("margin-left:50px")
        self.cbAudio.setChecked(False)
        self.verticalLayout.addWidget(self.cbAudio)
        self.cbGreyscale = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbGreyscale.setObjectName("cbGreyscale")
        self.cbGreyscale.setStyleSheet("margin-left:50px")

        self.cbGreyscale.setChecked(False)
        self.verticalLayout.addWidget(self.cbGreyscale)
        self.cbCompress = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbCompress.setObjectName("cbCompress")
        self.cbCompress.setText("Compress output")
        self.cbCompress.setStyleSheet("margin-left:50px")
        self.cbCompress.setChecked(False)
        self.verticalLayout.addWidget(self.cbCompress)
        self.cbPlots = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbPlots.setObjectName("cbPlots")
        self.cbPlots.setText("Generate trajectory plots")
        self.cbPlots.setStyleSheet("margin-left:50px")
        self.cbPlots.setChecked(False)
        self.verticalLayout.addWidget(self.cbPlots)
        self.radiusFrame=QtWidgets.QFrame(self.verticalLayoutWidget)
        self.radiusFrame.setFixedHeight(200)
        self.radiusSlider = QtWidgets.QSlider(self.radiusFrame)
        self.radiusSlider.setOrientation(QtCore.Qt.Horizontal)
        self.radiusSlider.setObjectName("radiusSlider")
        self.radiusSlider.setGeometry(20,40,160,30)
        self.radiusSlider.setRange(5,50)
        self.radiusSlider.setValue(30)
        self.lRadius=QtWidgets.QLabel(self.radiusFrame)
        self.lRadius.setAlignment(QtCore.Qt.AlignCenter)
        self.lRadius.setGeometry(0,0,200,30)
        self.lRadius.setText("Smoothing radius: "+str(self.radiusSlider.value()))
        self.lRadius.setStyleSheet("color: rgb(255, 255, 255);""font: 12pt \"MS Shell Dlg 2\";")
        self.lRadius.setMargin(0)
        self.radiusSlider.valueChanged.connect(self._updateRadius)
        self.verticalLayout.addWidget(self.radiusFrame)    


        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(320, -1, 641, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget(self.centralwidget)
        self.videoWidget.setGeometry(QtCore.QRect(320, 0, 640, 360))
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.positionSlider = QtWidgets.QSlider(self.frame)
        self.positionSlider.setGeometry(QtCore.QRect(70, 360, 491, 22))
        self.positionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.positionSlider.setObjectName("horizontalSlider")
        self.btnPlay = QtWidgets.QPushButton(self.frame)
        self.btnPlay.setGeometry(QtCore.QRect(0, 360, 24, 24))
        self.btnPlay.setStyleSheet("background-color: rgb(255, 214, 10);")
        self.btnPlay.setText("")
        self.btnPlay.setObjectName("btnPlay")

        self.btnPlay.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPlay))
        self.lTime = QtWidgets.QLabel(self.frame)
        self.lTime.setGeometry(QtCore.QRect(570, 360, 72, 20))
        self.lTime.setStyleSheet("color: rgb(255, 255, 255);")
        self.lTime.setAlignment(QtCore.Qt.AlignCenter)
        self.lTime.setObjectName("lTime")
        self.btnStop = QtWidgets.QPushButton(self.frame)
        self.btnStop.setGeometry(QtCore.QRect(30, 360, 24, 24))
        self.btnStop.setStyleSheet("background-color: rgb(255, 214, 10);")
        self.btnStop.setText("")
        self.btnStop.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaStop))

        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setGeometry(QtCore.QRect(0, 0, 85, 41))
        self.btnCancel.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                     "font: 20pt \"MS Shell Dlg 2\";\n"
                                     "color: rgb(255, 195, 0);\n"
                                     "border: 1px solid rgb(255, 214, 10);")
        self.btnCancel.setObjectName("btnCancel")
        self.btnSelect = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelect.setGeometry(QtCore.QRect(550, 650, 220, 50))
        self.btnSelect.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                        "font: 26pt \"MS Shell Dlg 2\";\n"
                                        "color: rgb(255, 195, 0);\n"
                                        "border: 1px solid rgb(255, 214, 10);")
        self.btnSelect.setObjectName("btnSelect")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(340, 385, 600, 251))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lMode = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lMode.setStyleSheet("color: rgb(255, 195, 0);\n"
                                 "font: 26pt \"MS Shell Dlg 2\";")
        self.lMode.setAlignment(QtCore.Qt.AlignCenter)
        self.lMode.setObjectName("lMode")
        self.gridLayout.addWidget(self.lMode, 0, 0, 1, 1)
        self.lTracker = QtWidgets.QLabel(self.gridLayoutWidget)
        self.lTracker.setStyleSheet("font: 24pt \"MS Shell Dlg 2\";\n"
                                    "color: rgb(255, 195, 0);")
        self.lTracker.setAlignment(QtCore.Qt.AlignCenter)
        self.lTracker.setObjectName("labeTracker")
        self.gridLayout.addWidget(self.lTracker, 3, 0, 1, 1)
        self.gbTracker = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.gbTracker.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gbTracker.sizePolicy().hasHeightForWidth())
        self.gbTracker.setSizePolicy(sizePolicy)
        self.gbTracker.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "font: 20pt \"MS Shell Dlg 2\";")
        self.gbTracker.setTitle("")
        self.gbTracker.setAlignment(QtCore.Qt.AlignCenter)
        self.gbTracker.setObjectName("gbTracker")
        self.widget = QtWidgets.QWidget(self.gbTracker)
        self.widget.setGeometry(QtCore.QRect(110, 4, 387, 61))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioCSRT = QtWidgets.QRadioButton(self.widget)
        self.radioCSRT.setStyleSheet("padding-right: 10px;")
        self.radioCSRT.setObjectName("radioCSRT")
        self.radioCSRT.setChecked(True)
        self.horizontalLayout_2.addWidget(self.radioCSRT)
        self.radioKCF = QtWidgets.QRadioButton(self.widget)
        self.radioKCF.setStyleSheet(
            "padding-right: 10px;""padding-left: 10px;")
        self.radioKCF.setObjectName("radioKCF")
        self.horizontalLayout_2.addWidget(self.radioKCF)
        self.radioMOSSE = QtWidgets.QRadioButton(self.widget)
        self.radioMOSSE.setStyleSheet(
            "padding-right: 10px;""padding-left: 10px;")
        self.radioMOSSE.setObjectName("radioMOSSE")
        self.horizontalLayout_2.addWidget(self.radioMOSSE)
        self.gridLayout.addWidget(self.gbTracker, 4, 0, 1, 1)
        self.gbMode = QtWidgets.QGroupBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gbMode.sizePolicy().hasHeightForWidth())
        self.gbMode.setSizePolicy(sizePolicy)
        self.gbMode.setStyleSheet("color: rgb(255, 255, 255);\n"
                                  "font: 16pt \"MS Shell Dlg 2\";\n")
        self.gbMode.setTitle("")
        self.gbMode.setAlignment(QtCore.Qt.AlignCenter)
        self.gbMode.setObjectName("gbMode")
        self.widget1 = QtWidgets.QWidget(self.gbMode)
        self.widget1.setGeometry(QtCore.QRect(90, 10, 420, 47))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioManualObjectSelection = QtWidgets.QRadioButton(self.widget1)
        self.radioManualObjectSelection.setChecked(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.radioManualObjectSelection.sizePolicy().hasHeightForWidth())
        self.radioManualObjectSelection.setSizePolicy(sizePolicy)
        self.radioManualObjectSelection.setStyleSheet("padding-right: 10px;")
        self.radioManualObjectSelection.setObjectName("radioManualObjectSelection")
        self.horizontalLayout.addWidget(self.radioManualObjectSelection)
        self.radioAIObjectDetection = QtWidgets.QRadioButton(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.radioAIObjectDetection.sizePolicy().hasHeightForWidth())
        self.radioAIObjectDetection.setSizePolicy(sizePolicy)
        self.radioAIObjectDetection.setStyleSheet("padding-left: 10px;")
        self.radioAIObjectDetection.setObjectName("radioAIObjectDetection")
        self.horizontalLayout.addWidget(self.radioAIObjectDetection)
        self.gridLayout.addWidget(self.gbMode, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        if self.videoPath != None:
            self._setMedia()
            self.btnPlay.clicked.connect(self._play)
            self.btnStop.clicked.connect(self._stop)
            self.positionSlider.setTickInterval(100)
            self.mediaPlayer.setNotifyInterval(100)
            self.positionSlider.sliderPressed.connect(
                self._pausePlaybackSliderEvent)
            self.positionSlider.valueChanged.connect(self._updatePosition)
            self.positionSlider.sliderReleased.connect(
                self._resumePlaybackAfterSliderEvent)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Video Stabilization Project"))
        self.cbShowTracking.setText(_translate("MainWindow", "Show tracking"))
        self.cbAudio.setText(_translate("MainWindow", "Enable Audio"))
        self.cbGreyscale.setText(_translate("MainWindow", "Greyscale"))
        self.btnCancel.setText(_translate("MainWindow", "Cancel"))
        self.btnSelect.setText(_translate("MainWindow", "Select Object"))
        self.lMode.setText(_translate("MainWindow", "Object Selection Mode"))
        self.lTracker.setText(_translate("MainWindow", "Tracker"))
        self.radioCSRT.setText(_translate("MainWindow", "CSRT"))
        self.radioKCF.setText(_translate("MainWindow", "KCF"))
        self.radioMOSSE.setText(_translate("MainWindow", "MOSSE"))
        self.radioManualObjectSelection.setText(
            _translate("MainWindow", "Manual Selection"))
        self.radioAIObjectDetection.setText(
            _translate("MainWindow", "AI Object Detection"))

    def _updateRadius(self,radius):
        self.lRadius.setText("Smoothing radius: "+str(radius))

    def _setMedia(self):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile(self.videoPath)))
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self._mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self._positionChanged)
        self.mediaPlayer.durationChanged.connect(self._durationChanged)
        self.mediaPlayer.pause()

    def _play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def _stop(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.stop()
    def _forceStop(self):
        self.mediaPlayer.stop()

    def _mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.btnPlay.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.btnPlay.setIcon(self.centralwidget.style().standardIcon(QStyle.SP_MediaPlay))


    def _positionChanged(self, position):
        self.positionSlider.blockSignals(True)
        self.positionSlider.setValue(position)
        self.positionSlider.blockSignals(False)
        self.lTime.setText(
            f"{durationFromMs(position)} / {durationFromMs(self.mediaPlayer.duration())}")

    def _durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.lTime.setText(f"00:00 / {durationFromMs(duration)}")

    def _updatePosition(self):
        position = self.positionSlider.value()
        self.mediaPlayer.setPosition(position)
        self.lTime.setText(
            f"{durationFromMs(position)} / {durationFromMs(self.mediaPlayer.duration())}")

    def _pausePlaybackSliderEvent(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playbackPausedBySliderEvent = True
            self.mediaPlayer.pause()

    def _resumePlaybackAfterSliderEvent(self):
        if self.playbackPausedBySliderEvent:
            self.mediaPlayer.play()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ConfigScreen()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
