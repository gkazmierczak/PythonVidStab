from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QStyle
from .utils import duration_from_ms


class ResultScreen(object):
    video_path = None
    playback_paused_by_slider_event = False

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet("background-color: rgb(0, 8, 20);")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.label_status = QtWidgets.QLabel(self.central_widget)
        self.label_status.setGeometry(QtCore.QRect(415, 20, 451, 40))
        self.label_status.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 24pt \"MS Shell Dlg 2\";")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setObjectName("lStatus")
        self.frame = QtWidgets.QFrame(self.central_widget)
        self.frame.setGeometry(QtCore.QRect(320, 100, 641, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget(self.central_widget)
        self.video_widget.setGeometry(QtCore.QRect(320, 100, 640, 360))
        self.media_player.setVideoOutput(self.video_widget)
        self.position_slider = QtWidgets.QSlider(self.frame)
        self.position_slider.setGeometry(QtCore.QRect(70, 360, 491, 22))
        self.position_slider.setOrientation(QtCore.Qt.Horizontal)
        self.position_slider.setObjectName("horizontalSlider")
        self.button_play = QtWidgets.QPushButton(self.frame)
        self.button_play.setGeometry(QtCore.QRect(0, 360, 24, 24))
        self.button_play.setStyleSheet("background-color: rgb(255, 195, 0);")
        self.button_play.setText("")
        self.button_play.setObjectName("btnPlay")
        self.button_play.setIcon(self.central_widget.style().standardIcon(QStyle.SP_MediaPlay))
        self.label_time = QtWidgets.QLabel(self.frame)
        self.label_time.setGeometry(QtCore.QRect(570, 360, 72, 20))
        self.label_time.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("lTime")
        self.button_stop = QtWidgets.QPushButton(self.frame)
        self.button_stop.setGeometry(QtCore.QRect(30, 360, 24, 24))
        self.button_stop.setStyleSheet("background-color: rgb(255, 195, 0);")
        self.button_stop.setText("")
        self.button_stop.setIcon(self.central_widget.style().standardIcon(QStyle.SP_MediaStop))
        self.button_restart = QtWidgets.QPushButton(self.central_widget)
        self.button_restart.setGeometry(QtCore.QRect(460, 520, 130, 40))
        self.button_restart.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                      "border: 1px solid rgb(255, 195, 0);\n"
                                      "color: rgb(255, 195, 0);\n"
                                      "font: 20pt \"MS Shell Dlg 2\";")
        self.button_restart.setObjectName("btnRestart")
        self.button_close = QtWidgets.QPushButton(self.central_widget)
        self.button_close.setGeometry(QtCore.QRect(690, 520, 90, 40))
        self.button_close.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                    "border: 1px solid rgb(255, 195, 0);\n"
                                    "color: rgb(255, 195, 0);\n"
                                    "font: 20pt \"MS Shell Dlg 2\";")
        self.button_close.setObjectName("btnClose")
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        if self.video_path != None:
            self._setMedia()
            self.button_play.clicked.connect(self._play)
            self.button_stop.clicked.connect(self._stop)
            self.position_slider.setTickInterval(100)
            self.media_player.setNotifyInterval(100)
            self.position_slider.sliderPressed.connect(
                self._pause_playback_slider_event)
            self.position_slider.valueChanged.connect(self._update_positions)
            self.position_slider.sliderReleased.connect(
                self._resume_playback_after_slider_event)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_status.setText(_translate("MainWindow", "Your video is ready"))
        self.button_restart.setText(_translate("MainWindow", "Start over"))
        self.button_close.setText(_translate("MainWindow", "Close"))

    def _setMedia(self):
        self.media_player.setMedia(QMediaContent(
            QUrl.fromLocalFile(self.video_path)))
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self._media_state_changed)
        self.media_player.positionChanged.connect(self._position_changed)
        self.media_player.durationChanged.connect(self._duration_changed)
        self.media_player.pause()

    def _play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def _stop(self):
        self.media_player.stop()

    def _media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.button_play.setIcon(self.central_widget.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.button_play.setIcon(self.central_widget.style().standardIcon(QStyle.SP_MediaPlay))

    def _position_changed(self, position):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(position)
        self.position_slider.blockSignals(False)
        self.label_time.setText(
            f"{duration_from_ms(position)} / {duration_from_ms(self.media_player.duration())}")

    def _duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
        self.label_time.setText(f"00:00 / {duration_from_ms(duration)}")

    def _update_positions(self):
        position = self.position_slider.value()
        self.media_player.setPosition(position)
        self.label_time.setText(
            f"{duration_from_ms(position)} / {duration_from_ms(self.media_player.duration())}")

    def _pause_playback_slider_event(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.playback_paused_by_slider_event = True
            self.media_player.pause()

    def _resume_playback_after_slider_event(self):
        if self.playback_paused_by_slider_event:
            self.media_player.play()

