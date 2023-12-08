from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys




class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 1000, 1000)  # xpos, ypos, width, height
        self.setWindowTitle("This window")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("My Label")
        self.label.move(50, 50)

        self.button01 = QtWidgets.QPushButton(self)
        self.button01.setText("Tap this button")
        self.button01.clicked.connect(self.taped)

    def taped(self):
        self.label.setText("You pressed this button")
        self.update()
    
    def update(self):
        self.label.adjustSize()



def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec_())

window()