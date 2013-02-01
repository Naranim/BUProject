from master_server.BUConfig import *
import postgresql.driver as pg_driver
import random
from bin.BULib import *

class DataBase(object):
    """Static class to manage data base"""

    DBdriver = pg_driver.connect(
        user = "root",
        password = "root",
        host = "localhost",
      #  database = DB_NAME,
        port = 5432
    )

    def __init__(self, arg):
        pass

    @staticmethod
    def toDBString(val) :
        if isinstance(val, str) : return "'" + val + "'"
        else : return str(val)

    @staticmethod
    @myDebug
    def getValues(table, valuesNames, conditions):
        """Method to get rows with selected values and given conditions"""
        query = "SELECT "
        for i in valuesNames:
            query += i + ", "
        query = query[0:-2] + " FROM " + table + " WHERE "
        for i in conditions :
            query += i[0] + " = " + DataBase.toDBString(i[1]) + "AND "
        query = query[0:-4] + ";"
        print(query)
        return DataBase.DBdriver.prepare(query)


    @staticmethod
    @myDebug
    def insertValues(table, values):
        """Insert array values to table"""
        query = "INSERT INTO " + table + " VALUES ("
        for i in values : query += DataBase.toDBString(i) + ", "
        query = query[0:-2] + ");"
        DataBase.DBdriver.execute(query)

    @staticmethod
    @myDebug
    def removeValues(table, conditions) :
        query = "DELETE FROM " + table + " WHERE "
        for i in conditions :
            query += DataBase.toDBString(i[0]) + " = " + DataBase.toDBString(i[1]) + "AND "
        query = query[0:-4] + ";"
        DataBase.DBdriver.prepare(query)

    @staticmethod
    @myDebug
    def select(s):
        tmp =  DataBase.DBdriver.prepare(s)
        return tmp()

if __name__ == "__main__" :
    print("Data base")
    res = DataBase.select("SELECT id, ip, port FROM slaves WHERE free > " + str(2*10000) + ";")
    L = res()
    print(L)
    random.shuffle(L)
    print(L)
