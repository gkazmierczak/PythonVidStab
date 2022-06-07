import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from .configScreen import ConfigScreen
from .resultScreen import ResultScreen
from .titleScreen import TitleScreen
from .loadingScreen import LoadingScreen
from src.tracker import Tracker
from src.stabilizer import Stabilizer
import src.converter as video_utils
import tempfile
import shutil


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(1280, 720)
        self.title_screen = TitleScreen()
        self.config_screen = ConfigScreen()
        self.loading_screen = LoadingScreen()
        self.result_screen = ResultScreen()
        self.start_title_screen()

    def start_config_screen(self):
        self.config_screen.video_path = self.input_file_path
        self.config_screen.setup_ui(self)
        self.config_screen.button_cancel.clicked.connect(self.return_to_title_screen)
        self.config_screen.button_select.clicked.connect(self._roi_selection)
        self.show()

    def start_result_screen(self):
        self.result_screen.video_path = self.output_file_path
        self.result_screen.setup_ui(self)
        self.result_screen.button_restart.clicked.connect(self.close_result_screen)
        self.result_screen.button_close.clicked.connect(self.close)

    def close_result_screen(self):
        self.result_screen._stop()
        self.start_title_screen()

    def return_to_title_screen(self):
        self.config_screen._stop()
        self.start_title_screen()

    def start_title_screen(self):
        self.title_screen.setup_ui(self)
        self.title_screen.button_select.clicked.connect(self._selectFile)
        self.show()

    def _selectFile(self):
        self.input_file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "",
                                                            "Movie files (*.mp4 *.avi *.wmv *.mov *.mkv)")
        if self.input_file_path != "":
            self.start_config_screen()

    def _roi_selection(self):
        self.config_screen.button_select.clicked.disconnect(self._roi_selection)
        self.config_screen._force_stop()
        is_manual_enabled = self.config_screen.radio_manual_object_selection.isChecked()
        self.video_capture = video_utils.create_video_capture(self.input_file_path)
        video_frames = video_utils.video_to_frame_list(self.video_capture)
        if is_manual_enabled:
            self.tracker = Tracker(video_frames)
        else:
            self.tracker = Tracker(video_frames, yolo=True)

        if self.tracker.bbox != (0, 0, 0, 0):
            self.stabilize_file(self.config_screen.radius_slider.value())
        else:
            self.config_screen.button_select.clicked.connect(self._roi_selection)

    def _getTrackingMode(self):
        modes = ["CSRT", "KCF", "MOSSE"]
        radios = [self.config_screen.radio_CSRT, self.config_screen.radio_KCF, self.config_screen.radio_MOSSE]
        for i, radio in enumerate(radios):
            if radio.isChecked():
                return modes[i]

    def stabilize_file(self, radius):
        self.start_loading_screen()
        self.output_options = {
            'audio': self.config_screen.checkbox_audio.isChecked(),
            'greyscale': self.config_screen.checkbox_greyscale.isChecked(),
            'compress': self.config_screen.checkbox_compress.isChecked(),
            'plots': self.config_screen.checkbox_plots.isChecked()
        }
        self.worker = Worker(self.tracker, self._getTrackingMode(), radius, self.output_options['plots'],
                             self.config_screen.checkbox_show_tracking.isChecked())
        self.worker.start()
        self.worker.started_tracking.connect(self._started_tracking)
        self.worker.started_stabilizing.connect(self._started_stabilizing)
        self.worker.finished_tracking.connect(self._finished_tracking)
        self.worker.finished_stabilizing.connect(self._finished_stabilizing)
        self.worker.err_sig.connect(self.stabilization_error)

    def _started_tracking(self):
        self.loading_screen.append_text("Tracking...")

    def _started_stabilizing(self):
        self.loading_screen.append_text("Stabilizing...")

    def _finished_tracking(self):
        self.loading_screen.append_text("Tracking completed.")

    def _finished_stabilizing(self):
        self.loading_screen.append_text("Stabilizing completed.")
        self.output_file_path = ""
        while self.output_file_path == "":
            self.output_file_path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "All Files (*)")
        if self.output_options['greyscale']:
            video_utils.convert_frames_to_greyscale(self.tracker.frames)

        if self.output_options['audio'] and video_utils.contains_audio(self.input_file_path):
            tempdir_path = tempfile.mkdtemp()
            tempfile_name = tempdir_path + "\\tempfile.mp4"
            video_utils.write_video_to_file(tempfile_name, self.tracker.frames, self.video_capture.get(cv2.CAP_PROP_FPS),
                                            iscolor=not self.output_options['greyscale'])
            video_utils.mux_video_audio(tempfile_name, self.input_file_path, self.output_file_path)
            shutil.rmtree(tempdir_path)
        else:
            if self.output_options['compress']:
                video_utils.write_video_to_file(self.output_file_path, self.tracker.frames,
                                                self.video_capture.get(cv2.CAP_PROP_FPS),
                                                not self.output_options['greyscale'])
                video_utils.repack_video(self.output_file_path)
            else:
                video_utils.write_video_to_file(self.output_file_path, self.tracker.frames,
                                                self.video_capture.get(cv2.CAP_PROP_FPS),
                                                not self.output_options['greyscale'])

        self.loading_screen.append_text(f"Saved output as {self.output_file_path}")
        self.start_result_screen()

    def stabilization_error(self, e):
        self.loading_screen.append_text("ERROR: " + str(e))

    def start_loading_screen(self):
        self.loading_screen.setup_ui(self)
        self.loading_screen.button_cancel.clicked.connect(self.return_to_title_screen)
        self.show()


class Worker(QThread):
    started_tracking = pyqtSignal()
    finished_tracking = pyqtSignal()
    started_stabilizing = pyqtSignal()
    finished_stabilizing = pyqtSignal()
    err_sig = pyqtSignal(str)

    def __init__(self, tracker, tracking_mode, smoothing_radius, generate_plots, show_tracking):
        super(QThread, self).__init__()
        self.tracker = tracker
        self.tracking_mode = tracking_mode
        self.smoothing_radius = smoothing_radius
        self.generate_plots = generate_plots
        self.show_tracking = show_tracking

    def run(self):
        try:
            self.started_tracking.emit()
            self.tracker.tracking_data = self.tracker.track(self.tracking_mode, self.show_tracking)
            self.finished_tracking.emit()
            self.started_stabilizing.emit()
            self.stabilizer = Stabilizer(self.tracker.frames, self.tracker.tracking_data)
            self.stabilizer.stabilize(self.smoothing_radius, self.generate_plots)
            self.finished_stabilizing.emit()
        except Exception as e:
            self.err_sig.emit(str(e))

