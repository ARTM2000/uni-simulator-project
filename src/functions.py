import random
from time import time, sleep
from typing import Iterable

from src.simulate.Customer import Customer

def isNumeric(input: str):
    try:
        number = int(input)
        if number == 0:
            raise ""
        return True 
    except:
        return False

def nowTimeStamp():
    now_second = time()
    # return round(now_second * 1000)
    return round(now_second * 100)

def myCustomSleep(ms: int):
    # return sleep(ms / 1000)
    return sleep(ms/100)

def generateCustomeEntranceTimeGapPrediction(maxTime: int):
    columns: Iterable[str] = ["مدت بین دو ورود", "احتمال", "احتمال تجمعی"]
    data: Iterable[tuple] = []

    totalPrediction = 0

    for i in range(1, maxTime + 1):
        prediction = round(1 / maxTime, 5)
        totalPrediction = totalPrediction + (1 / maxTime)
        row = (i, prediction, round(totalPrediction, 5))
        data.append(row)

    return {"column": columns, "data": data}

def generateCustomerServicePrediction(maxTime: int):
    columns: Iterable[str] = ["زمان خدمت دهی", "احتمال", "احتمال تجمعی"]
    data: Iterable[tuple] = []

    totalPrediction = 0

    for i in range(1, maxTime + 1):
        prediction = round(1 / maxTime, 5)
        totalPrediction = totalPrediction + (1 / maxTime)
        row = (i, prediction, round(totalPrediction, 5))
        data.append(row)

    return {"column": columns, "data": data}


def generateCustomerEntranceTimeGap(
        customersCount: int, 
        entranceData: Iterable[tuple[str]]
    ):
    columns: Iterable[str] = ["مشتری", "عدد تصادفی", "مدت بین دو ورود"]
    data: Iterable[tuple] = []

    for i in range(1, customersCount + 1):
        if i == 1:
            row = (i, "-", "-")   
            data.append(row)
            continue 
        customerRandomNO = round(random.uniform(0, 1), 5)
        entranceTimeGap = 0
        for j, (minutes, prediction, totalPrediction) in enumerate(entranceData):
            if customerRandomNO <= totalPrediction:
                entranceTimeGap = minutes
                break
        row = (i, customerRandomNO, entranceTimeGap)
        data.append(row)

    return {"column": columns, "data": data}


def generateCustomerServiceTimeGap(
        customersCount: int, 
        entranceData: Iterable[tuple[str]]
    ):
    columns: Iterable[str] = ["مشتری", "عدد تصادفی", "مدت خدمت گیری"]
    data: Iterable[set] = []

    for i in range(1, customersCount + 1):
        customerRandomNO = round(random.uniform(0, 1), 5)
        entranceTimeGap = 0
        for j, (minutes, prediction, totalPrediction) in enumerate(entranceData):
            if customerRandomNO <= totalPrediction:
                entranceTimeGap = minutes
                break
        row = (i, customerRandomNO, entranceTimeGap)
        data.append(row)

    return {"column": columns, "data": data}

def mergeCustomersData(
        customersServiceTime: list[tuple], 
        customersEntranceTime: list[tuple]
    ) -> list[dict]:
    customerData = []

    for i, (customerNumber, _, serviceTime) in enumerate(customersServiceTime):
        customerInfo = {
            "index": customerNumber,
            "serviceTime": serviceTime,
            "lastEntranceTime": 0
        }
        customerData.append(customerInfo)

    for i, (customerNumber2, _, lastEntranceTime) in enumerate(customersEntranceTime):
        customerData[i]["lastEntranceTime"] = lastEntranceTime
    # print(customerData)
    customers = []
    for customer in customerData:
        finalCustomer = Customer(
            index=customer["index"], 
            serviceTime=customer["serviceTime"], 
            lastEntranceTime=customer["lastEntranceTime"]
        )
        customers.append(finalCustomer)

    return customers