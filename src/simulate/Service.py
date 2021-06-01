from src.functions import myCustomSleep, nowTimeStamp
from src.simulate.Customer import Customer


class Service:
    def __init__(self, name: str) -> None:
        self.name = name
        self.notWorkingServiceTimeList: list[dict] = []
        self.lastNotWorkingRecord: dict = {}
        self.currentServiceNotWorkingTimestamp = nowTimeStamp()
        self.departmentLastCustomerIndex = 0
        self.customer = {}
        self.allServicedCustomers = []
        self.available = True

    # this method should call after a new department's customer 
    # assigned to a available service
    def watchForNewCustomerInDepartment(
        self,
        newCustomerIndex: int, 
        newCustomerEnterTimestamp: int
    ) -> None:
        self.departmentLastCustomerIndex = newCustomerIndex

        if self.customer != {} and newCustomerIndex == self.customer["index"]:
            return

        # if this is not first record of not working time,
        # we complete this last record
        if self.lastNotWorkingRecord != {} and self.available:
            self.lastNotWorkingRecord["cIndex"] = newCustomerIndex
            self.lastNotWorkingRecord["to"] = newCustomerEnterTimestamp
            self.notWorkingServiceTimeList.append(self.lastNotWorkingRecord)

        if self.available:
            newNotWorkingRecord = {}
            newNotWorkingRecord["name"] = self.name
            newNotWorkingRecord["cIndex"] = '-'
            newNotWorkingRecord["from"] = newCustomerEnterTimestamp
            newNotWorkingRecord["to"] = '-'
            self.lastNotWorkingRecord = newNotWorkingRecord
        else:
            print("service was not available: ", self.name)


    def assignACustomer(self, customerData: Customer, customerPauseTime: int) -> int:
        # serviceNotWorkingUntilTime = nowTimeStamp()
        # self.notWorkingServiceTimeList.append(
        #     (
        #         customerData.index, # until this customer, service not working 
        #         self.currentServiceNotWorkingTimestamp, 
        #         serviceNotWorkingUntilTime
        #     )
        # )
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
        customerEndTime = nowTimeStamp()
        self.customer["serviceEndAt"] = customerEndTime
        self.customer["serviceName"] = self.name
        self.allServicedCustomers.append(self.customer)

        # after customer service finished, we add
        # a new notWorkingRecore for service until completed
        newNotWorkingRecord = {}
        newNotWorkingRecord["name"] = self.name
        newNotWorkingRecord["cIndex"] = '-'
        newNotWorkingRecord["from"] = customerEndTime
        newNotWorkingRecord["to"] = '-'
        self.lastNotWorkingRecord = newNotWorkingRecord

        ## reset not working timestamp for service
        ## self.currentServiceNotWorkingTimestamp = nowTimeStamp()
        self.available = True
