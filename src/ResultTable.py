from typing import Iterable

from PyQt5 import QtWidgets, QtCore
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
        self.setGeometry(50, 50, width, height)
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

        # add data in table
        if self.index == 4:
            for i, row in enumerate(self.data):
                row1 = QTableWidgetItem(str(row[0]))
                row2 = QTableWidgetItem(str(row[1]))
                row3 = QTableWidgetItem(str(row[2]))
                row4 = QTableWidgetItem(str(row[3]))
                row5 = QTableWidgetItem(str(row[4]))
                row6 = QTableWidgetItem(str(row[5]))
                row7 = QTableWidgetItem(str(row[6]))
                row8 = QTableWidgetItem(str(row[7]))
                row9 = QTableWidgetItem(str(row[8]))
                self.setItem(i, 0, row1)
                self.setItem(i, 1, row2)
                self.setItem(i, 2, row3)
                self.setItem(i, 3, row4)
                self.setItem(i, 4, row5)
                self.setItem(i, 5, row6)
                self.setItem(i, 6, row7)
                self.setItem(i, 7, row8)
                self.setItem(i, 8, row9)

        header = self.horizontalHeader()
        for i in range(len(self.columns)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    # def get_rgb_from_hex(self, code):
    #     code_hex = code.replace("#", "")
    #     rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    #     return QColor.fromRgb(rgb[0], rgb[1], rgb[2])