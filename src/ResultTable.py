from typing import Iterable, Set
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

class ResultTable(QTableWidget): 
    def __init__(
        self, 
        data: Iterable[set], 
        columns: Iterable[str], 
        showIndex: int, 
        width: int, 
        height: int,
        title: str
        ):
        super(ResultTable, self).__init__()
        self.data = data
        self.columns = columns
        self.index = showIndex
        self.setGeometry(50 * showIndex, 50, width, height)
        self.setWindowTitle(title)
        self.initialTableUI()


    def initialTableUI(self):
        # initial table base view
        print("initial table UI")
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)

        # add data in table
        if self.index <= 3:
            # for i, (refId, randomNumber, value) in enumerate(self.data):
            for i, (refId, randomNumber, value) in enumerate(self.data):
                referenceId = QTableWidgetItem(str(refId))
                randomNumber = QTableWidgetItem(str(randomNumber))
                value = QTableWidgetItem(str(value))
                self.setItem(i, 0, referenceId)
                self.setItem(i, 1, randomNumber)
                self.setItem(i, 2, value)

        header = self.horizontalHeader()
        for i in range(len(self.columns)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    # def get_rgb_from_hex(self, code):
    #     code_hex = code.replace("#", "")
    #     rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    #     return QColor.fromRgb(rgb[0], rgb[1], rgb[2])