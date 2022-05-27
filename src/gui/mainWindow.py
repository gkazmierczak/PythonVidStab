import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFileDialog
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from configScreen import ConfigScreen
from resultScreen import ResultScreen
from titleScreen import TitleScreen
from loadingScreen import LoadingScreen
from src.tracker import Tracker
from src.stabilizer import Stabilizer
import src.converter as videoUtils
import tempfile
import shutil


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(1280, 720)
        self.titleScreen = TitleScreen()
        self.configScreen = ConfigScreen()
        self.loadingScreen = LoadingScreen()
        self.resultScreen = ResultScreen()
        self.startTitleScreen()

    def startConfigScreen(self):
        self.configScreen.videoPath = self.inputFilePath
        self.configScreen.setupUi(self)
        self.configScreen.btnCancel.clicked.connect(self.returnToTitleScreen)
        self.configScreen.btnSelect.clicked.connect(self._roiSelection)
        self.show()

    def startResultScreen(self):
        self.resultScreen.videoPath = self.outputFilePath
        self.resultScreen.setupUi(self)
        self.resultScreen.btnRestart.clicked.connect(self.closeResultScreen)
        self.resultScreen.btnClose.clicked.connect(self.close)

    def closeResultScreen(self):
        self.resultScreen._stop()
        self.startTitleScreen()

    def returnToTitleScreen(self):
        self.configScreen._stop()
        self.startTitleScreen()

    def startTitleScreen(self):
        self.titleScreen.setupUi(self)
        self.titleScreen.selectBtn.clicked.connect(self._selectFile)
        self.show()

    def _selectFile(self):
        self.inputFilePath, _ = QFileDialog.getOpenFileName(self, "Select file", "",
                                                            "Movie files (*.mp4 *.avi *.wmv *.mov *.mkv)")
        if self.inputFilePath != "":
            self.startConfigScreen()

    def _roiSelection(self):
        self.configScreen._forceStop()
        isManualEnabled = self.configScreen.radioManualObjectSelection.isChecked()
        self.videoCapture = videoUtils.createVideoCapture(self.inputFilePath)
        videoFrames = videoUtils.videoToFrameList(self.videoCapture)
        if isManualEnabled:
            self.tracker = Tracker(videoFrames)
        else:
            self.tracker = Tracker(videoFrames, yolo=True)

        if self.tracker.bbox != (0, 0, 0, 0):
            self.stabilizeFile(self.configScreen.radiusSlider.value())

    def _getTrackingMode(self):
        modes = ["CSRT", "KCF", "MOSSE"]
        radios = [self.configScreen.radioCSRT, self.configScreen.radioKCF, self.configScreen.radioMOSSE]
        for i, radio in enumerate(radios):
            if radio.isChecked():
                return modes[i]

    def stabilizeFile(self, radius):
        self.startLoadingScreen()
        self.outputOptions = {
            'audio': self.configScreen.cbAudio.isChecked(),
            'greyscale': self.configScreen.cbGreyscale.isChecked(),
            'compress': self.configScreen.cbCompress.isChecked(),
            'plots': self.configScreen.cbPlots.isChecked()
        }
        self.worker = Worker(self.tracker, self._getTrackingMode(), radius, self.outputOptions['plots'],
                             self.configScreen.cbShowTracking.isChecked())
        self.worker.start()
        self.worker.started_tracking.connect(self._startedTracking)
        self.worker.started_stabilizing.connect(self._startedStabilizing)
        self.worker.finished_tracking.connect(self._finishedTracking)
        self.worker.finished_stabilizing.connect(self._finishedStabilizing)
        self.worker.err_sig.connect(self.stabilizationError)

    def _startedTracking(self):
        self.loadingScreen.appendText("Tracking...")

    def _startedStabilizing(self):
        self.loadingScreen.appendText("Stabilizing...")

    def _finishedTracking(self):
        self.loadingScreen.appendText("Tracking completed.")

    def _finishedStabilizing(self):
        self.loadingScreen.appendText("Stabilizing completed.")
        self.outputFilePath = ""
        while self.outputFilePath == "":
            self.outputFilePath, _ = QFileDialog.getSaveFileName(self, "Save file", "", "All Files (*)")

        print(self.outputOptions)
        if self.outputOptions['greyscale']:
            videoUtils.convertFramesToGreyscale(self.tracker.frames)

        if self.outputOptions['audio']:
            tempdirPath = tempfile.mkdtemp()
            tempfileName = tempdirPath + "\\tempfile.mp4"
            videoUtils.writeVideoToFile(tempfileName, self.tracker.frames, self.videoCapture.get(cv2.CAP_PROP_FPS),
                                        iscolor=not self.outputOptions['greyscale'])
            videoUtils.muxVideoAudio(tempfileName, self.inputFilePath, self.outputFilePath)
            shutil.rmtree(tempdirPath)
        else:
            if self.outputOptions['compress']:
                videoUtils.writeVideoToFile(self.outputFilePath, self.tracker.frames,
                                            self.videoCapture.get(cv2.CAP_PROP_FPS),
                                            not self.outputOptions['greyscale'])
                videoUtils.repackVideo(self.outputFilePath)
            else:
                videoUtils.writeVideoToFile(self.outputFilePath, self.tracker.frames,
                                            self.videoCapture.get(cv2.CAP_PROP_FPS),
                                            not self.outputOptions['greyscale'])

        self.loadingScreen.appendText(f"Saved output as {self.outputFilePath}")
        self.startResultScreen()

    def stabilizationError(self, e):
        self.loadingScreen.appendText("ERROR: " + str(e))

    def startLoadingScreen(self):
        self.loadingScreen.setupUi(self)
        self.loadingScreen.btnCancel.clicked.connect(self.returnToTitleScreen)
        self.show()


class Worker(QThread):
    started_tracking = pyqtSignal()
    finished_tracking = pyqtSignal()
    started_stabilizing = pyqtSignal()
    finished_stabilizing = pyqtSignal()
    err_sig = pyqtSignal(str)

    def __init__(self, tracker, trackingMode, smoothingRadius, generatePlots, showTracking):
        super(QThread, self).__init__()
        self.tracker = tracker
        self.trackingMode = trackingMode
        self.smoothingRadius = smoothingRadius
        self.generatePlots = generatePlots
        self.showTracking = showTracking

    def run(self):
        try:
            self.started_tracking.emit()
            self.tracker.trackingData = self.tracker.track(self.trackingMode, self.showTracking)
            self.finished_tracking.emit()
            self.started_stabilizing.emit()
            self.stabilizer = Stabilizer(self.tracker.frames, self.tracker.trackingData)
            self.stabilizer.stabilize(self.smoothingRadius, self.generatePlots)
            self.finished_stabilizing.emit()
        except Exception as e:
            self.err_sig.emit(str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
