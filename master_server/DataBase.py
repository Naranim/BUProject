from master_server.BUConfig import *
import postgresql.driver as pg_driver
from master_server.BULib import *

class DataBase(object):
    """Static class to manage data base"""

    DBdriver = pg_driver.connect(
        user = DB_LOGIN,
        password = DB_PASS,
        host = DB_HOST,
     #   database = DB_NAME,
        port = DB_PORT
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
        DataBase.DBdriver.execute(query)



def oblicz(st_zap, il_pol):
    return ((1-st_zap)**3)*800/(il_pol*il_pol)

if __name__ == "__main__" :

    print("Data base")
