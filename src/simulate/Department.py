from queue import Queue

from src.functions import isNumeric, nowTimeStamp, myCustomSleep
from src.simulate.Service import Service

class Department:
    def __init__(self, servicesCount: int, customersData: list[dict]):
        self.queue = Queue(maxsize=0)
        self.services: list[Service] = []
        self.customersCount = len(customersData)
        # create all services
        for i in range(servicesCount):
            self.services.append(Service(f"service-n{ i + 1 }"))
        # add customers to queue
        for i in range(len(customersData)):
            self.queue.put(customersData[i])
        # do final customers work
        self.doCustomersWork()
        self.departmentStartTimestamp = nowTimeStamp()

    def doCustomersWork(self):
        for i in range(self.customersCount):
            # if queue is empty, we break loop
            if self.queue.empty():
                break
            currentCustomer = self.queue.get()
            # if lastEntranceTime exist, we pause until
            # time arrive
            if isNumeric(currentCustomer.lastEntranceTime):
                myCustomSleep(currentCustomer.lastEntranceTime)

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

            availableService.assignACustomer(
                currentCustomer, 
                customerPauseTime_stop - customerPauseTime_start
            )

            