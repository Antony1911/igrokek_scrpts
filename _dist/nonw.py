from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageQt, ImageEnhance
# from PyQt5.QtGui import Qt
from pyqtgraph.examples.text import text

#from covid19gui_V3 import Ui_MainWindow
import os
import sys

input_img = Image.open("d:/.tools/scrn_Some/natan_17.png")
text_edit = QPlainTextEdit()

class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    textWritten = QtCore.pyqtSignal(str)
    def __init__(self, parent=None, **kwargs):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ShowIButton.clicked.connect(self.do_test)
        self.chooseStudy.clicked.connect(self.do_choosestudy)
        self.RunButton_3.clicked.connect(self.do_runstudy)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        w, h = input_img.size
        self.pixmap_item = self.scene.addPixmap(QtGui.QPixmap())
        # self.graphicsView.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        self.graphicsView.update()
        self.plainTextEdit.update()
        self.level = 1
        self.enhancer = None
        self.timer = QtCore.QTimer(interval=500, timeout=self.on_timeout)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def write(self, text):
        self.textWritten.emit(str(text))

    @QtCore.pyqtSlot()
    def do_test(self):
        # input_img = Image.open("/home/ironmantis7x/Documents/Maverick_AI/Python/keras-covid-19/maverickAI30k.png")
        self.enhancer = ImageEnhance.Brightness(input_img)
        self.timer.start()
        self.ShowIButton.setDisabled(True)

    @QtCore.pyqtSlot()
    def on_timeout(self):
        if self.enhancer is not None:
            result_img = self.enhancer.enhance(self.level)
            qimage = ImageQt.ImageQt(result_img)
            self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(qimage))
        if self.level > 7:
            self.timer.stop()
            self.enhancer = None
            self.level = 0
            self.ShowIButton.setDisabled(False)
        self.level = 1
        self.ShowIButton.setDisabled(False)

    @QtCore.pyqtSlot()
    def do_choosestudy(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

    @QtCore.pyqtSlot()
    def do_runstudy(self):
        os.system("df -h")
        # filetext = open('screenout.txt').read()
        # filetext.close()
        # textViewValue = self.plainTextEdit.toPlainText()
        # QPlainTextEdit.appendPlainText(self, str(textViewValue))
        # sys.stdout = self(textWritten=self.textWritten)
        self.normalOutputWritten(text_edit)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text_edit):
        #cursor = self.plainTextEdit.textCursor()
        #cursor.movePosition(QtGui.QTextCursor.End)
        #cursor.insertText(text_edit)
        self.plainTextEdit.appendPlainText(text_edit)
        #self.plainTextEdit.ensureCursorVisible()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())