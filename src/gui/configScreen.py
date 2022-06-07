from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QStyle
from .utils import duration_from_ms


class ConfigScreen(object):
    video_path = None
    playback_paused_by_slider_event = False

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet("background-color: rgb(0, 8, 20);")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.groupbox_options = QtWidgets.QGroupBox(self.central_widget)
        self.groupbox_options.setGeometry(QtCore.QRect(1080, 0, 191, 341))
        self.groupbox_options.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "border: 0px;"
                                     "background-color: rgb(0, 8, 20);")
        self.groupbox_options.setTitle("")
        self.groupbox_options.setAlignment(QtCore.Qt.AlignCenter)
        self.groupbox_options.setObjectName("gbOptions")
        self.vertical_layout_widget = QtWidgets.QWidget(self.groupbox_options)
        self.vertical_layout_widget.setGeometry(QtCore.QRect(-1, 0, 191, 341))
        self.vertical_layout_widget.setObjectName("verticalLayoutWidget")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName("verticalLayout")

        self.checkbox_show_tracking = QtWidgets.QCheckBox(self.vertical_layout_widget)
        self.checkbox_show_tracking.setObjectName("cbShowTracking")
        self.checkbox_show_tracking.setStyleSheet("margin-left:50px")
        self.checkbox_show_tracking.setChecked(False)
        self.vertical_layout.addWidget(self.checkbox_show_tracking)

        self.checkbox_audio = QtWidgets.QCheckBox(self.vertical_layout_widget)
        self.checkbox_audio.setObjectName("cbAudio")
        self.checkbox_audio.setStyleSheet("margin-left:50px")
        self.checkbox_audio.setChecked(False)
        self.vertical_layout.addWidget(self.checkbox_audio)
        self.checkbox_greyscale = QtWidgets.QCheckBox(self.vertical_layout_widget)
        self.checkbox_greyscale.setObjectName("cbGreyscale")
        self.checkbox_greyscale.setStyleSheet("margin-left:50px")

        self.checkbox_greyscale.setChecked(False)
        self.vertical_layout.addWidget(self.checkbox_greyscale)
        self.checkbox_compress = QtWidgets.QCheckBox(self.vertical_layout_widget)
        self.checkbox_compress.setObjectName("cbCompress")
        self.checkbox_compress.setText("Compress output")
        self.checkbox_compress.setStyleSheet("margin-left:50px")
        self.checkbox_compress.setChecked(False)
        self.vertical_layout.addWidget(self.checkbox_compress)
        self.checkbox_plots = QtWidgets.QCheckBox(self.vertical_layout_widget)
        self.checkbox_plots.setObjectName("cbPlots")
        self.checkbox_plots.setText("Generate trajectory plots")
        self.checkbox_plots.setStyleSheet("margin-left:50px")
        self.checkbox_plots.setChecked(False)
        self.vertical_layout.addWidget(self.checkbox_plots)
        self.radius_frame = QtWidgets.QFrame(self.vertical_layout_widget)
        self.radius_frame.setFixedHeight(200)
        self.radius_slider = QtWidgets.QSlider(self.radius_frame)
        self.radius_slider.setOrientation(QtCore.Qt.Horizontal)
        self.radius_slider.setObjectName("radiusSlider")
        self.radius_slider.setGeometry(20, 40, 160, 30)
        self.radius_slider.setRange(5, 50)
        self.radius_slider.setValue(30)
        self.label_radius = QtWidgets.QLabel(self.radius_frame)
        self.label_radius.setAlignment(QtCore.Qt.AlignCenter)
        self.label_radius.setGeometry(0, 0, 200, 30)
        self.label_radius.setText("Smoothing radius: " + str(self.radius_slider.value()))
        self.label_radius.setStyleSheet("color: rgb(255, 255, 255);""font: 12pt \"MS Shell Dlg 2\";")
        self.label_radius.setMargin(0)
        self.radius_slider.valueChanged.connect(self._update_radius)
        self.vertical_layout.addWidget(self.radius_frame)

        self.frame = QtWidgets.QFrame(self.central_widget)
        self.frame.setGeometry(QtCore.QRect(320, -1, 641, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget(self.central_widget)
        self.video_widget.setGeometry(QtCore.QRect(320, 0, 640, 360))
        self.media_player.setVideoOutput(self.video_widget)
        self.position_slider = QtWidgets.QSlider(self.frame)
        self.position_slider.setGeometry(QtCore.QRect(70, 360, 491, 22))
        self.position_slider.setOrientation(QtCore.Qt.Horizontal)
        self.position_slider.setObjectName("horizontalSlider")
        self.button_play = QtWidgets.QPushButton(self.frame)
        self.button_play.setGeometry(QtCore.QRect(0, 360, 24, 24))
        self.button_play.setStyleSheet("background-color: rgb(255, 214, 10);")
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
        self.button_stop.setStyleSheet("background-color: rgb(255, 214, 10);")
        self.button_stop.setText("")
        self.button_stop.setIcon(self.central_widget.style().standardIcon(QStyle.SP_MediaStop))

        self.button_cancel = QtWidgets.QPushButton(self.central_widget)
        self.button_cancel.setGeometry(QtCore.QRect(0, 0, 85, 41))
        self.button_cancel.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                     "font: 20pt \"MS Shell Dlg 2\";\n"
                                     "color: rgb(255, 195, 0);\n"
                                     "border: 1px solid rgb(255, 214, 10);")
        self.button_cancel.setObjectName("btnCancel")
        self.button_select = QtWidgets.QPushButton(self.central_widget)
        self.button_select.setGeometry(QtCore.QRect(550, 650, 220, 50))
        self.button_select.setStyleSheet("background-color: rgb(0, 29, 61);\n"
                                     "font: 26pt \"MS Shell Dlg 2\";\n"
                                     "color: rgb(255, 195, 0);\n"
                                     "border: 1px solid rgb(255, 214, 10);")
        self.button_select.setObjectName("btnSelect")
        self.grid_layout_widget = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(340, 385, 600, 251))
        self.grid_layout_widget.setObjectName("gridLayoutWidget")
        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("gridLayout")
        self.label_mode = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_mode.setStyleSheet("color: rgb(255, 195, 0);\n"
                                 "font: 26pt \"MS Shell Dlg 2\";")
        self.label_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mode.setObjectName("lMode")
        self.grid_layout.addWidget(self.label_mode, 0, 0, 1, 1)
        self.label_tracker = QtWidgets.QLabel(self.grid_layout_widget)
        self.label_tracker.setStyleSheet("font: 24pt \"MS Shell Dlg 2\";\n"
                                    "color: rgb(255, 195, 0);")
        self.label_tracker.setAlignment(QtCore.Qt.AlignCenter)
        self.label_tracker.setObjectName("labeTracker")
        self.grid_layout.addWidget(self.label_tracker, 3, 0, 1, 1)
        self.groupbox_tracker = QtWidgets.QGroupBox(self.grid_layout_widget)
        self.groupbox_tracker.setEnabled(True)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.groupbox_tracker.sizePolicy().hasHeightForWidth())
        self.groupbox_tracker.setSizePolicy(size_policy)
        self.groupbox_tracker.setStyleSheet("color: rgb(255, 255, 255);\n"
                                     "font: 20pt \"MS Shell Dlg 2\";")
        self.groupbox_tracker.setTitle("")
        self.groupbox_tracker.setAlignment(QtCore.Qt.AlignCenter)
        self.groupbox_tracker.setObjectName("gbTracker")
        self.widget = QtWidgets.QWidget(self.groupbox_tracker)
        self.widget.setGeometry(QtCore.QRect(110, 4, 387, 61))
        self.widget.setObjectName("widget")
        self.horizontal_layout2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontal_layout2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout2.setObjectName("horizontalLayout_2")
        self.radio_CSRT = QtWidgets.QRadioButton(self.widget)
        self.radio_CSRT.setStyleSheet("padding-right: 10px;")
        self.radio_CSRT.setObjectName("radioCSRT")
        self.radio_CSRT.setChecked(True)
        self.horizontal_layout2.addWidget(self.radio_CSRT)
        self.radio_KCF = QtWidgets.QRadioButton(self.widget)
        self.radio_KCF.setStyleSheet(
            "padding-right: 10px;""padding-left: 10px;")
        self.radio_KCF.setObjectName("radioKCF")
        self.horizontal_layout2.addWidget(self.radio_KCF)
        self.radio_MOSSE = QtWidgets.QRadioButton(self.widget)
        self.radio_MOSSE.setStyleSheet(
            "padding-right: 10px;""padding-left: 10px;")
        self.radio_MOSSE.setObjectName("radioMOSSE")
        self.horizontal_layout2.addWidget(self.radio_MOSSE)
        self.grid_layout.addWidget(self.groupbox_tracker, 4, 0, 1, 1)
        self.groupbox_mode = QtWidgets.QGroupBox(self.grid_layout_widget)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.groupbox_mode.sizePolicy().hasHeightForWidth())
        self.groupbox_mode.setSizePolicy(size_policy)
        self.groupbox_mode.setStyleSheet("color: rgb(255, 255, 255);\n"
                                  "font: 16pt \"MS Shell Dlg 2\";\n")
        self.groupbox_mode.setTitle("")
        self.groupbox_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.groupbox_mode.setObjectName("gbMode")
        self.widget = QtWidgets.QWidget(self.groupbox_mode)
        self.widget.setGeometry(QtCore.QRect(90, 10, 420, 47))
        self.widget.setObjectName("widget1")
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.radio_manual_object_selection = QtWidgets.QRadioButton(self.widget)
        self.radio_manual_object_selection.setChecked(True)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.radio_manual_object_selection.sizePolicy().hasHeightForWidth())
        self.radio_manual_object_selection.setSizePolicy(size_policy)
        self.radio_manual_object_selection.setStyleSheet("padding-right: 10px;")
        self.radio_manual_object_selection.setObjectName("radioManualObjectSelection")
        self.horizontal_layout.addWidget(self.radio_manual_object_selection)
        self.radio_ai_object_detection = QtWidgets.QRadioButton(self.widget)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.radio_ai_object_detection.sizePolicy().hasHeightForWidth())
        self.radio_ai_object_detection.setSizePolicy(size_policy)
        self.radio_ai_object_detection.setStyleSheet("padding-left: 10px;")
        self.radio_ai_object_detection.setObjectName("radioAIObjectDetection")
        self.horizontal_layout.addWidget(self.radio_ai_object_detection)
        self.grid_layout.addWidget(self.groupbox_mode, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        if self.video_path != None:
            self._set_media()
            self.button_play.clicked.connect(self._play)
            self.button_stop.clicked.connect(self._stop)
            self.position_slider.setTickInterval(100)
            self.media_player.setNotifyInterval(100)
            self.position_slider.sliderPressed.connect(
                self._pause_playback_slider_event)
            self.position_slider.valueChanged.connect(self._update_position)
            self.position_slider.sliderReleased.connect(
                self._resume_playback_after_slider_event)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Video Stabilization Project"))
        self.checkbox_show_tracking.setText(_translate("MainWindow", "Show tracking"))
        self.checkbox_audio.setText(_translate("MainWindow", "Enable Audio"))
        self.checkbox_greyscale.setText(_translate("MainWindow", "Greyscale"))
        self.button_cancel.setText(_translate("MainWindow", "Cancel"))
        self.button_select.setText(_translate("MainWindow", "Select Object"))
        self.label_mode.setText(_translate("MainWindow", "Object Selection Mode"))
        self.label_tracker.setText(_translate("MainWindow", "Tracker"))
        self.radio_CSRT.setText(_translate("MainWindow", "CSRT"))
        self.radio_KCF.setText(_translate("MainWindow", "KCF"))
        self.radio_MOSSE.setText(_translate("MainWindow", "MOSSE"))
        self.radio_manual_object_selection.setText(
            _translate("MainWindow", "Manual Selection"))
        self.radio_ai_object_detection.setText(
            _translate("MainWindow", "AI Object Detection"))

    def _update_radius(self, radius):
        self.label_radius.setText("Smoothing radius: " + str(radius))

    def _set_media(self):
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
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.stop()

    def _force_stop(self):
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

    def _update_position(self):
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

