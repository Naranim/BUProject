from master_server.BUConfig import *
import postgresql.driver as pg_driver
import random
from bin.BULib import *

class DataBase(object):
    """Statyczna klasa obslugujaca polaczenie z baza danych w postgresie
        Dane potrzebne do polaczenia pobiera z BUConfig.py
        Za jej posrednictwem odbywaja sie wszystkie zapytania do bazy
    """

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
        """
        pomocnicza metoda do zamiany zmiennych na odpowiednie argumenty w pgsqlu
        """
        if isinstance(val, str) : return "'" + val + "'"
        else : return str(val)

    @staticmethod
    @myDebug
    def getValues(table, valuesNames, conditions):
        """Metoda do pobrania danych z tabeli table
        Pobiera wartosci z listy values
        Pod warunkami rownosci z listy par conditions
        """
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
        """Wstawia wartosci values do tabeli table"""
        query = "INSERT INTO " + table + " VALUES ("
        for i in values : query += DataBase.toDBString(i) + ", "
        query = query[0:-2] + ");"
        DataBase.DBdriver.execute(query)

    @staticmethod
    @myDebug
    def removeValues(table, conditions) :
        """
        Usuwa krotki spelniajace rownosci z listy par conditions z tabeli table
        """
        query = "DELETE FROM " + table + " WHERE "
        for i in conditions :
            query += DataBase.toDBString(i[0]) + " = " + DataBase.toDBString(i[1]) + "AND "
        query = query[0:-4] + ";"
        DataBase.DBdriver.prepare(query)

    def select(s) -> list:
        """
        Zwraca rezultat zapytania s
        """
        tmp = DataBase.DBdriver.prepare(s)
        return tmp()

if __name__ == "__main__" :
    print("Data base")
    res = DataBase.select("SELECT id, ip, port FROM slaves WHERE free > " + str(2*10000) + ";")
    L = res()
    print(L)
    random.shuffle(L)
    print(L)
