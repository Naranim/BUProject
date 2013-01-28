from master_server.DataBase import *
from master_server import MasterServerLib
import time


@myDebug
def login(msg, ip):
    if not (msg[1][0:6] == "login:" and msg[2][0:7] == "passwd:") : return "WRONG REQUEST"
    usrLogin = msg[1][6:]
    loginSucc = False
    tmp = DataBase.getValues("users", ["id"], [("login", usrLogin)])
    if len(tmp()) == 0 : return "WRONG LOG"
    return "SUCCESS\n"

@myDebug
def upload(msg, ip):
    #TODO
    #wybierz listę najlepszych kandydatów
    #slavesList = DataBase.DBdriver.
    #jedź po kolei i znajdź działający
    #niech sobie gnój czeka na klienta i da port

    #wyślij klientowi port, niech się męczy sam
    if not checkRequest(msg, ip) : return "WRONG REQUEST"
    return "dupa"

@myDebug
def download(msg, ip):
    #TODO
    #wybierz listę serwerów z plikiem
    #wybierz najmniej obciążony
    #zagadaj do niego, zdobądź port
    #wyślij dane klientowi
    if not checkRequest(msg, ip) : return "WRONG REQUEST"
    return "dupa"

@myDebug
def getList(msg, ip):
    if not checkRequest(msg, ip) : return "WRONG REQUEST"
    usrLogin = msg[1][6:]
    response = DataBase.getValues("users", ["id"], [("login", usrLogin)])
    usrId = response()[0][0]
    files = DataBase.getValues("files", ["name", "size", "added"], [("owner", usrId)])
    fileList = "Files:\n"
    for row in files:
        for var in row:
            fileList += str(var) + "|"
        # I'm sorry for that :(
        fileList = fileList[0:-1] + ';'

    return list;

@myDebug
def checkRequest(msg, ip):
    if not (msg[1][0:6] == "login:") : return 0
    usrLogin = msg[1][6:]
    tmp = DataBase.getValues("users", ["id"], [("login", usrLogin)])
    if len(tmp()) == 0 : return 0
    return 1
