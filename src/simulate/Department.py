from queue import Queue
from time import sleep

from src.functions import isNumeric, nowTimeStamp, myCustomSleep
from src.simulate.Service import Service
from src.simulate.Customer import Customer

class Department:
    def __init__(self, servicesCount: int, customersData: list[Customer]):
        self.queue = Queue(maxsize=0)
        self.services: list[Service] = []
        self.customers: list[dict] = customersData
        self.customersCount = len(customersData)
        self.departmentStartTimestamp = nowTimeStamp()
        # create all services
        for i in range(servicesCount):
            self.services.append(Service(f"service-n{ servicesCount - i }"))
        # do final customers work
        self.addCustomersToDepartment()

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

        # after all customer added to queue,
        # check if queue become empty
        # and doneWorkedCustomers's length become equal to
        # all department customers, start calculation
        while (not self.queue.empty()) and (remainedCustomers != 0):
            print("Wait until simulation for this department done!!!")
            sleep(2)
        print(self.queue.empty())
        print(remainedCustomers)

        self.calculateResult()

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
                    if isAvailable:
                        serviceFound = True
                        availableService = self.services[i]
            
            customerPauseTime_stop = nowTimeStamp()

            customerIndex = currentCustomer.index
            print(f"customer {customerIndex} assigned to {availableService.name}")

            availableService.assignACustomer(
                currentCustomer, 
                customerPauseTime_stop - customerPauseTime_start
            )

    def calculateResult(self):
        print("calculation")
        for i in range(len(self.services)):
            currentService = self.services[i]
            print("=========================")
            print("service name: ", currentService.name)
            print("serviced customers => ", currentService.allServicedCustomers)
            print("not working time => ", currentService.notWorkingServiceTimeList)
