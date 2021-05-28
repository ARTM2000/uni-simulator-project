import random
from typing import Iterable

def isNumeric(input: str):
    try:
        number = int(input)
        if number == 0:
            raise ""
        return True
    except:
        return False

def generateCustomeEntranceTimeGapPrediction(maxTime: int):
    columns: Iterable[str] = ["مدت بین دو ورود", "احتمال", "احتمال تجمعی"]
    data: Iterable[set] = []

    totalPrediction = 0

    for i in range(1, maxTime + 1):
        prediction = round(1 / maxTime, 5)
        totalPrediction = totalPrediction + (1 / maxTime)
        row = (i, prediction, round(totalPrediction, 5))
        data.append(row)

    return {"column": columns, "data": data}

def generateCustomerServicePrediction(maxTime: int):
    columns: Iterable[str] = ["زمان خدمت دهی", "احتمال", "احتمال تجمعی"]
    data: Iterable[set] = []

    totalPrediction = 0

    for i in range(1, maxTime + 1):
        prediction = round(1 / maxTime, 5)
        totalPrediction = totalPrediction + (1 / maxTime)
        row = (i, prediction, round(totalPrediction, 5))
        data.append(row)

    return {"column": columns, "data": data}


def generateCustomerEntranceTimeGap(
        customersCount: int, 
        entranceData: Iterable[set[str]]
    ):
    columns: Iterable[str] = ["مشتری", "عدد تصادفی", "مدت بین دو ورود"]
    data: Iterable[set] = []

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
