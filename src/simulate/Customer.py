class Customer:
    def __init__(self, index: int, serviceTime: int, lastEntranceTime: int) -> None:
        self.index = index
        self.serviceTime = serviceTime
        self.lastEntranceTime = lastEntranceTime

    def getInfo(self) -> dict:
        return {
            "index": self.index,
            "serviceTime": self.serviceTime,
            "lastEntranceTime": self.lastEntranceTime
        }