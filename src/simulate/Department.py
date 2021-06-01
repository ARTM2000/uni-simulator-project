import threading
from queue import Queue

from src.functions import isNumeric, nowTimeStamp, myCustomSleep
from src.simulate.Service import Service
from src.simulate.Customer import Customer
from src.simulate.ServiceTheard import ServiceThread
from src.ResultTable import ResultTable

class Department:
    def __init__(self, servicesCount: int, customersData: list[Customer], parent):
        self.queue = Queue(maxsize=0)
        self.services: list[Service] = []
        self.customers: list[Customer] = customersData
        self.customersCount = len(customersData)
        self.departmentStartTimestamp = nowTimeStamp()
        self.threads: list[ServiceThread] = []
        # create all services
        for i in range(servicesCount):
            self.services.append(Service(f"service-n{ servicesCount - i }"))
        # do final customers work
        finalTable = self.addCustomersToDepartment()
        parent.simulationTable = finalTable

    def addCustomersToDepartment(self):
        for currentCustomer in self.customers:
            # if lastEntranceTime exist, we pause until
            # time arrive
            if isNumeric(currentCustomer.lastEntranceTime):
                myCustomSleep(currentCustomer.lastEntranceTime)
            
            # check if queue was empty
            queueWasEmpty = self.queue.empty()

            # add current customer to queue
            self.queue.put(currentCustomer)
            # if queue was empty, recall doCustomerWork
            if queueWasEmpty:
                self.doCustomersWork()

        # after all customer added to queue,
        # check if queue become empty
        # and doneWorkedCustomers's length become equal to
        # all department customers, start calculation
        allThreadsDead = False
        while (not allThreadsDead):
            for i in range(len(self.threads)):
                currentThread = self.threads[i]
                if currentThread.is_alive():
                    break
                if i + 1 == len(self.threads):
                    allThreadsDead = True

        return self.calculateResult()

    def doCustomersWork(self):
        while not self.queue.empty():
            currentCustomer: Customer = self.queue.get()

            availableService = None
            serviceFound = False
            customerPauseTime_start = nowTimeStamp()

            # search for available service and process
            # pause until a service become available
            while not serviceFound:
                for i in range(len(self.services)):
                    isAvailable = self.services[i].isServiceAvailable()
                    # print(f"{self.services[i].name} status is: ",isAvailable)
                    if isAvailable:
                        serviceFound = True
                        availableService = self.services[i]
                
                # for updating show service available or not
            
            customerPauseTime_stop = nowTimeStamp()

            customerIndex = currentCustomer.index

            # creating a thread for service
            currentThread = ServiceThread(
                service=availableService, 
                customer=currentCustomer, 
                customerPauseTime=customerPauseTime_stop - customerPauseTime_start
            )
            # running thread activity
            currentThread.start()
            for i in range(len(self.services)):
                if self.services[i].name != availableService.name:
                    self.services[i].watchForNewCustomerInDepartment(
                        customerIndex, 
                        currentThread.getThreadStartTimestamp()
                    )
            self.threads.append(currentThread)

    def calculateResult(self):

        allServiceCustomersReport: list[dict] = []
        allNotWorkingServiceTime: list[dict] = []

        for i in range(len(self.services)):
            currentService = self.services[i]
            # print("=========================")
            # print("service name: ", currentService.name)
            # print("serviced customers => ", currentService.allServicedCustomers)
            # print("not working time => ", currentService.notWorkingServiceTimeList)
            # concatenate this service customers report to saved one
            allServiceCustomersReport = allServiceCustomersReport + currentService.allServicedCustomers
            allNotWorkingServiceTime = allNotWorkingServiceTime + currentService.notWorkingServiceTimeList
        
        # sort allServiceCustomersReport by customers indexes
        allServiceCustomersReport.sort(key=lambda c: c["index"])

        # final formatting allServiceCustomersReport
        nowPassedTime = 0        
        for report in allServiceCustomersReport:
            if report["index"] == 1:
                report["entranceTime"] = 0
            else:
                report["entranceTime"] = nowPassedTime + report["lastEntranceTime"]
                nowPassedTime = nowPassedTime + report["lastEntranceTime"]
            report["serviceStartAt"] = report["serviceStartAt"] - self.departmentStartTimestamp
            report["serviceEndAt"] = report["serviceEndAt"] - self.departmentStartTimestamp
            report["spendTimeInDepartment"] = report["serviceEndAt"] - report["entranceTime"]
            if report["index"] == 1:
                report["servicesNotWorkingTime"] = '-'
            else :
                listOfNotWorkingTimesBeforeCustomerEntrance = list(
                        filter(
                        lambda nwt: nwt['cIndex'] == report['index'], 
                        allNotWorkingServiceTime
                    )
                )
                beforeThisCustomerTotalNotWorkingTime = 0
                if len(listOfNotWorkingTimesBeforeCustomerEntrance) > 0:
                    for nwt in listOfNotWorkingTimesBeforeCustomerEntrance:
                        notWorkingTime = nwt['to'] - nwt['from']
                        beforeThisCustomerTotalNotWorkingTime += notWorkingTime
                report["servicesNotWorkingTime"] = beforeThisCustomerTotalNotWorkingTime

        finalTableHeader = [
            'مشتری', 'مدت از آخرین ورود', 'زمان ورود', 'مدت خدمت دهی', 'زمان شروع خدمت', 'مدت ماندن مشتری در صف', 'زمان پایان خدمت', 'مدت ماندن مشتری در سیستم', 'مدت بیکاری خدمت دهنده(گان)']
        finalFormattedDataForTable: list[tuple] = []
        for report in allServiceCustomersReport:
            row = (
                report['index'], 
                report['lastEntranceTime'], 
                report['entranceTime'], 
                report['serviceTime'],
                report['serviceStartAt'],
                report['pauseTime'],
                report['serviceEndAt'],
                report['spendTimeInDepartment'],
                report['servicesNotWorkingTime']
            )
            finalFormattedDataForTable.append(row)

        finalSimulationTable = ResultTable(
            finalFormattedDataForTable, 
            finalTableHeader, 
            4, 
            1400, 
            500, 
            "نتیجه شبیه سازی - Alireza Tanoomandian"
        )
        return finalSimulationTable
