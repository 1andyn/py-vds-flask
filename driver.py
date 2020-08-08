import pymongo
import datetime
import authfile
import dns


class Database:
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://" + authfile.c_sr + ":" + authfile.c_pa + "@" + authfile.c_co +
                                     "/vue_days_since?authSource=admin&retryWrites=true&w=majority")
        self.__mgdbClient = client
        self.__db = client.vue_days_since

    # returns database object for arg react sch
    def get_database(self):
        return self.__db

    # inserts event into database
    def insert_event(self, event, user):
        collection = self.__db["vds_events"]
        doc = {"strUsrId": user,
                "strId": event.getId(),
                "strEvent": event.getEvent(),
                "dtmDate": event.getDate()}

        return collection.insert_one(doc)

    # retrieves events for user
    def get_events(self, user):
        collection = self.__db["vds_events"]
        events = []
        for event in collection.find({"strUsrId": user},
                                     {"_id": 0,
                                      "strUsrId": 1,
                                      "strId": 1,
                                      "strEvent": 1,
                                      "dtmDate": 1}):
            events.append(event)

        return events

    # deletes ALL events for user
    def del_events(self, user):
        collection = self.__db["vds_events"]
        collection.delete_many({"strUsrId": user})

    # deletes ALL events for user
    def del_one_event(self, user, eid):
        collection = self.__db["vds_events"]
        collection.delete_one({"strUsrId": user, "strId": eid})