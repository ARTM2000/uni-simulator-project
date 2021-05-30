import threading
from queue import Queue

from src.functions import isNumeric, nowTimeStamp, myCustomSleep
from src.simulate.Service import Service
from src.simulate.Customer import Customer
from src.simulate.ServiceTheard import ServiceThread

class Department:
    def __init__(self, servicesCount: int, customersData: list[Customer]):
        self.queue = Queue(maxsize=0)
        self.services: list[Service] = []
        self.customers: list[dict] = customersData
        self.customersCount = len(customersData)
        self.departmentStartTimestamp = nowTimeStamp()
        self.threads: list[ServiceThread] = []
        # create all services
        for i in range(servicesCount):
            self.services.append(Service(f"service-n{ servicesCount - i }"))
        # do final customers work
        return self.addCustomersToDepartment()

    def addCustomersToDepartment(self):
        remainedCustomers = len(self.customers)
        print(remainedCustomers)
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
            remainedCustomers = remainedCustomers - 1

        print("Wait until simulation for this department done!!!")
        # after all customer added to queue,
        # check if queue become empty
        # and doneWorkedCustomers's length become equal to
        # all department customers, start calculation
        allThreadsDead = False
        while (not self.queue.empty()) and (not allThreadsDead):
            # if len(threading.enumerate()) == 0:
            #     allThreadsDead = True
            for i in range(len(self.threads)):
                currentThread = self.threads[i]
                currentThreadServiceIsAvailable = currentThread.service.isServiceAvailable()
                if not currentThreadServiceIsAvailable:
                    break
                if i + 1 == len(self.threads):
                    allThreadsDead = True

        print(self.queue.empty())
        return self.calculateResult()

    def doCustomersWork(self):
        while not self.queue.empty():
            currentCustomer = self.queue.get()

            availableService = None
            serviceFound = False
            customerPauseTime_start = nowTimeStamp()

            # search for available service and process
            # pause until a service become available
            while not serviceFound:
                for i in range(len(self.services)):
                    isAvailable = self.services[i].isServiceAvailable()
                    print(f"{self.services[i].name} status is: ",isAvailable)
                    if isAvailable:
                        serviceFound = True
                        availableService = self.services[i]
            
            customerPauseTime_stop = nowTimeStamp()

            customerIndex = currentCustomer.index
            print(f"customer {customerIndex} assigned to {availableService.name}")

            # creating a thread for service
            currentThread = ServiceThread(
                service=availableService, 
                customer=currentCustomer, 
                customerPauseTime=customerPauseTime_stop - customerPauseTime_start
            )
            # running thread activity
            currentThread.start()
            self.threads.append(currentThread)

    def calculateResult(self):
        print("calculation")

        allServiceCustomersReport: list[dict] = []

        for i in range(len(self.services)):
            currentService = self.services[i]
            # finish service time of a service
            currentService.endService()
            print("=========================")
            print("service name: ", currentService.name)
            print("serviced customers => ", currentService.allServicedCustomers)
            print("not working time => ", currentService.notWorkingServiceTimeList)
            # concatenate this service customers report to saved one
            allServiceCustomersReport = allServiceCustomersReport + currentService.allServicedCustomers
        
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

        # print(allServiceCustomersReport)
