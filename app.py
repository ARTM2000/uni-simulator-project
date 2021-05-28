from PyQt5.QtWidgets import QApplication
import sys

from src.MyWindow import MyWindow

def myApp():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    myApp()