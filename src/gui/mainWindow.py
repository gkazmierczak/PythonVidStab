import sys
from PyQt5.QtWidgets import QApplication , QMainWindow , QPushButton , QWidget,QFileDialog
from PyQt5.QtMultimedia import QMediaContent
from configScreen import ConfigScreen
from titleScreen import TitleScreen
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.titleScreen = TitleScreen()
        self.configScreen = ConfigScreen()
        self.startTitleScreen()

    def startConfigScreen(self,filepath=None):
        if filepath!=None:
            self.configScreen.videoPath=filepath
        self.configScreen.setupUi(self)
        self.configScreen.btnCancel.clicked.connect(self.returnToTitleScreen)
        self.configScreen.btnSelect.clicked.connect(self._roiSelection)
        self.show()

    def returnToTitleScreen(self):
        self.configScreen.mediaPlayer.stop()
        self.startTitleScreen()

    def startTitleScreen(self):
        self.titleScreen.setupUi(self)
        self.titleScreen.selectBtn.clicked.connect(self._selectFile)
        self.show()

    def _selectFile(self):
        inputFilePath ,_= QFileDialog.getOpenFileName(self,"Select file","","All Files (*)")
        self.startConfigScreen(inputFilePath)
    
    def _roiSelection(self):
        isManualEnabled=self.configScreen.radioManualObjectSelection.isChecked()
        if isManualEnabled:
            #TODO: manual roi selection
            None
        else:
            #TODO: ai object detection then roi selection
            None 

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())