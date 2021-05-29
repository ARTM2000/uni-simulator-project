from src.functions import myCustomSleep, nowTimeStamp
from src.simulate.Customer import Customer


class Service:
    def __init__(self, name: str) -> None:
        self.name = name
        self.notWorkingServiceTimeList: list[tuple] = []
        self.currentServiceNotWorkingTimestamp = nowTimeStamp()
        self.customer = {}
        self.allServicedCustomers = []
        self.available = True

    def assignACustomer(self, customerData: Customer, customerPauseTime: int) -> int:
        serviceNotWorkingUntilTime = nowTimeStamp()
        self.notWorkingServiceTimeList.append(
            (
                customerData.index, # until this customer, service not working 
                self.currentServiceNotWorkingTimestamp, 
                serviceNotWorkingUntilTime
            )
        )
        print(customerData)
        self.available = False
        self.customer = customerData.getInfo()
        startTime = nowTimeStamp()
        self.doCustomerWork(customerPauseTime, startTime)
        return customerData.index
    
    def isServiceAvailable(self) -> bool:
        return self.available

    def doCustomerWork(self, cPauseTime, serviceStartAt) -> None:
        customerServiceTime: int = self.customer["serviceTime"]
        myCustomSleep(customerServiceTime)
        self.customer["pauseTime"] = cPauseTime
        self.customer["serviceStartAt"] = serviceStartAt
        self.customer["serviceEndAt"] = nowTimeStamp()
        self.allServicedCustomers.append(self.customer)
        # reset not working timestamp for service
        self.currentServiceNotWorkingTimestamp = nowTimeStamp()
        self.available = True