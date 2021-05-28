from src.functions import myCustomSleep, nowTimeStamp

"""
    - customer spend time in department remained
    - unused time of service remained
"""

class Service:
    def __init__(self, name: str) -> None:
        self.name = name
        self.customer = {}
        self.allServicedCustomers = []
        self.available = True

    def assignACustomer(self, customerData: dict, customerPauseTime: int):
        print(customerData)
        self.available = False
        self.customer = customerData
        startTime = nowTimeStamp()
        self.doCustomerWork(customerPauseTime, startTime)
    
    def isServiceAvailable(self) -> bool:
        return self.available

    def doCustomerWork(self, cPauseTime, serviceStartAt):
        customerServiceTime: int = self.customer["serviceTime"]
        myCustomSleep(customerServiceTime)
        self.customer["pauseTime"] = cPauseTime
        self.customer["serviceStartAt"] = serviceStartAt
        self.customer["serviceEndAt"] = nowTimeStamp()
        self.allServicedCustomers.append(self.customer)
        self.available = True