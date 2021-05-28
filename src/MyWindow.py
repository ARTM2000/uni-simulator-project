from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from src.ResultTable import ResultTable
from src.functions import (
        isNumeric, 
        generateCustomeEntranceTimeGapPrediction, 
        generateCustomerServicePrediction,
        generateCustomerEntranceTimeGap,
        generateCustomerServiceTimeGap,
        mergeCustomersData
    )

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.winX = 20
        self.winY = 20
        self.winWidth = 500
        self.winHeight = 300

        self.setWindowTitle("Alireza Tanoomandian - University - simulator")
        self.setGeometry(self.winX, self.winY, self.winWidth, self.winHeight)
        self.setMinimumWidth(self.winWidth)
        self.setMaximumWidth(self.winWidth)
        self.initialUI()

    def initialUI(self):
        # customer max service time
        self.label = QtWidgets.QLabel(self)
        self.label.setText("<font color=black>بیشترین زمان خدمت دهی به مراجعه کننده</font>")
        self.label.adjustSize()
        self.label.move(193, 47)
        #-----------
        self.maxServiceTime = QtWidgets.QLineEdit(self)
        self.maxServiceTime.setMinimumWidth(80)
        self.maxServiceTime.move(50, 43)
        
        # customer entrance time gap
        self.firstLabel = QtWidgets.QLabel(self)
        self.firstLabel.setText("<font color=blue>بیشترین زمان بین دو ورود خدمت گیرنده</font>")
        self.firstLabel.adjustSize()
        self.firstLabel.move(205, 87)
        #-----------
        self.maxTimeGapBetweenCustomers = QtWidgets.QLineEdit(self)
        self.maxTimeGapBetweenCustomers.setMinimumWidth(80)
        self.maxTimeGapBetweenCustomers.move(50, 83)

        # simulation customers count
        self.secondLabel = QtWidgets.QLabel(self)
        self.secondLabel.setText("<font color=orange>تعداد مراجعه کننده در شبیه سازی</font>")
        self.secondLabel.adjustSize()
        self.secondLabel.move(245, 127)
        #-----------
        self.customersCount = QtWidgets.QLineEdit(self)
        self.customersCount.setMinimumWidth(80)
        self.customersCount.move(50, 123)

        # services count
        self.thirdLabel = QtWidgets.QLabel(self)
        self.thirdLabel.setText("<font color=green>تعداد سرویس دهندگان</font>")
        self.thirdLabel.adjustSize()
        self.thirdLabel.move(310, 167)
        #-----------
        self.serviceCount = QtWidgets.QLineEdit(self)
        self.serviceCount.setMinimumWidth(80)
        self.serviceCount.move(50, 163)

        self.actionBTN = QtWidgets.QPushButton(self)
        self.actionBTN.setText("انجام محاسبات")
        self.actionBTN.adjustSize()
        self.actionBTN.move(50, 210)
        self.actionBTN.setFixedWidth(400)
        self.actionBTN.setFixedHeight(40)
        self.actionBTN.clicked.connect(self.calculateNecessaryData)

    def calculateNecessaryData(self):
        maxTimeGap = self.maxTimeGapBetweenCustomers.text().strip()
        maxServiceTime = self.maxServiceTime.text().strip()
        customersCount = self.customersCount.text().strip()
        serviceCount = self.serviceCount.text().strip()

        # check inputs values
        if (
            (not isNumeric(maxServiceTime)) or
            (not isNumeric(maxTimeGap)) or
            (not isNumeric(customersCount)) or
            (not isNumeric(serviceCount))
        ):
            errorMessage = QtWidgets.QErrorMessage(self)
            errorMessage.showMessage("مقدار ورودی باید عدد طبیعی بزرگتر از 0 باشد")
            errorMessage.move(150, 100)
            return

        # if values are valid, do the process
        maxTimeGap = int(maxTimeGap)
        maxServiceTime = int(maxServiceTime)
        customersCount = int(customersCount)
        serviceCount = int(serviceCount)

        print("verified")

        self.entranceTimeGapData = generateCustomeEntranceTimeGapPrediction(maxTimeGap)
        # print(entranceTimeGapData)
        self.entranceTable = ResultTable(
            self.entranceTimeGapData["data"], 
            self.entranceTimeGapData["column"], 
            1, 
            350, 
            500, 
            "احتمال فاصله زمانی بین دو ورود")

        self.serviceTimeData = generateCustomerServicePrediction(maxServiceTime)
        self.serviceTime = ResultTable(
            self.serviceTimeData["data"], 
            self.serviceTimeData["column"], 
            2, 
            350, 
            500, 
            "احتمال زمان خدمت دهی")

        self.customerEntranceTimeGapData = generateCustomerEntranceTimeGap(
            customersCount, 
            self.entranceTimeGapData["data"]
        )
        # print(customerEntranceTimeGapData)
        self.customerEntrance = ResultTable(
            self.customerEntranceTimeGapData["data"], 
            self.customerEntranceTimeGapData["column"], 
            3, 
            350, 
            500,
            "فاصله زمانی ورود خدمت گیرندگان")

        self.customerServiceTime = generateCustomerServiceTimeGap(
            customersCount, 
            self.serviceTimeData["data"]
        )
        # print(customerEntranceTimeGapData)
        self.customerService = ResultTable(
            self.customerServiceTime["data"], 
            self.customerServiceTime["column"], 
            3, 
            370, 
            500,
            "مدت خدمت گیری خدمت گیرندگان")

        self.close()

        self.runFinalSimulatorResult()
        self.showTables()

    def runFinalSimulatorResult(self):
        customerFinalData = mergeCustomersData(
                self.customerServiceTime["data"], 
                self.customerEntranceTimeGapData["data"]
            )

    def showTables(self):
        self.entranceTable.show()
        self.serviceTime.show()
        self.customerEntrance.show()
        self.customerService.show()

