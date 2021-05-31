from threading import Thread

from src.simulate.Service import Service
from src.simulate.Customer import Customer
from src.functions import nowTimeStamp

class ServiceThread(Thread):
    def __init__(self, service: Service, customer: Customer, customerPauseTime: int):
        super(ServiceThread, self).__init__()
        self.threadID = customer.index
        self.service = service
        self.customer = customer
        self.customerPauseTimeInQueue = customerPauseTime
        self.startTime: int = 0

    def run(self):
        customerIndex = self.customer.index
        self.startTime = nowTimeStamp()
        print(f"customer by index {customerIndex} assigned to {self.service.name}")
        self.service.assignACustomer(
            customerData=self.customer, 
            customerPauseTime=self.customerPauseTimeInQueue
        )
    def getThreadStartTimestamp(self) -> int:
        return self.startTime
