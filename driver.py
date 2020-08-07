import pymongo
import datetime
import authfile
import dns


class Database:
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://" + authfile.c_sr + ":" + authfile.c_pa + "@" + authfile.c_co +
                                     "/vue_days_since?authSource=admin&retryWrites=true&w=majority")
        self.__mgdbClient = client
        self.__db = client.arg_react_sch
        print("MongoDB: Connection established")

    # returns database object for arg react sch
    def get_database(self):
        return self.__db