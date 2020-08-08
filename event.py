class Event:
    def __init__(self, id, event, date):
        self.__strId = id
        self.__strEvent = event
        self.__dtmDate = date

    def getId(self):
        return self.__strId

    def getEvent(self):
        return self.__strEvent

    def getDate(self):
        return self.__dtmDate
