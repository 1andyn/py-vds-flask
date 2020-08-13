import datetime
import pymongo
import authfile
import dns
import event


class Database:
    def __init__(self):

        if authfile.dev:
            db = "dev_vue_days_since"
            user = authfile.c_dsr
            pw = authfile.c_dpa
        else:
            db = "vue_days_since"
            user = authfile.c_sr
            pw = authfile.c_pa

        client = pymongo.MongoClient("mongodb+srv://" + user + ":" + pw + "@" + authfile.c_co +
                                     "/" + db + "?authSource=admin&retryWrites=true&w=majority")
        self.__mgdbClient = client
        self.__db = client[db]

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

        return collection.update_one({"strUsrId": user,
                                      "strId": event.getId()},
                                     {"$set": doc}, upsert=True)

    # inserts archive event into database, removes from non-archive
    def arch_event(self, event, user):
        collection = self.__db["vds_archive"]
        doc = {"strUsrId": user,
               "strId": event.getId(),
               "strEvent": event.getEvent(),
               "dtmDate": event.getDate()}

        collection.update_one({"strUsrId": user,
                               "strId": event.getId()},
                              {"$set": doc}, upsert=True)

        collection = self.__db["vds_events"]
        collection.delete_one({"strUsrId": user, "strId": event.getId()})

    # retrieves events for user
    def get_events(self, user):
        collection = self.__db["vds_events"]
        events = []
        for e in collection.find({"strUsrId": user},
                                 {"_id": 0,
                                  "strId": 1,
                                  "strEvent": 1,
                                  "dtmDate": 1}):
            events.append(e)
        return events

    # retrieves events for user
    def get_archive(self, user):
        collection = self.__db["vds_archive"]
        events = []
        for e in collection.find({"strUsrId": user},
                                 {"_id": 0,
                                  "strId": 1,
                                  "strEvent": 1,
                                  "dtmDate": 1}):
            events.append(e)
        return events

    def clr_archive(self, user):
        collection = self.__db["vds_archive"]
        collection.delete_many({"strUsrId": user})

    # deletes ALL events for user
    def del_one_arch(self, user, eid):
        collection = self.__db["vds_archive"]
        collection.delete_one({"strUsrId": user, "strId": eid})

    # deletes ALL events for user
    def del_events(self, user):
        collection = self.__db["vds_events"]
        collection.delete_many({"strUsrId": user})

    # deletes ALL events for user
    def del_one_event(self, user, eid):
        collection = self.__db["vds_events"]
        collection.delete_one({"strUsrId": user, "strId": eid})
