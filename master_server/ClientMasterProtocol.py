from master_server.DataBase import *
from master_server import MasterServerLib
import time
import random
import bin.BULib
import socket


@myDebug
def login(msg):
    """zaloguj uzytkownika
    msg - wiadomosc od uzytkownika
    zwraca SUCCESS gdy logowanie sie udalo
    WRONG LOG w przeciwnym przypadku"""
    if not (msg[1][0:6] == "login:") : return "WRONG REQUEST"
    usrLogin = msg[1][6:]
    tmp = DataBase.getValues("users", ["id"], [("login", usrLogin)])
    if len(tmp()) == 0 : return "WRONG LOG"
    return "SUCCESS\n"

@myDebug
def upload(msg):

    print("In upload")
    if not (msg[1][0:6] == "login:") : return "WRONG REQUEST"
    login = msg[1].split(":")[1]
    fileName = msg[2].split(":")[1]
    modified = msg[3].split(":")[1]
    fileSize = msg[4].split(":")[1]

    slaves = DataBase.select("SELECT id, ip, port FROM slaves WHERE free > " + str(2*int(fileSize)) + ";")

    random.shuffle(slaves)

    print(slaves)

    dest = slaves[0]

    ticket = bin.BULib.genRandString(20)
    s = socket.socket()
    s.connect((dest[1], dest[2]))
    request = "GETFILE\nname:"+fileName+"\nuser:"+login+"\nticket:"+ticket+"\nmodified:"+modified
    s.send(request.encode())
    answer = s.recv(1024)

    s.close()

    return answer.decode()



@myDebug
def download(msg):
    login = msg[1].split(":")[1]
    fileName = msg[2].split(":")[1]
    modified = msg[3].split(":")[1]
    slaves = DataBase.select("SELECT slave_id FROM files WHERE user_id="+login+" AND modified="+modified+ " AND name="+fileName+";")

    slaves = slaves()
    random.shuffle(slaves)

    dest = slaves[0]

    ticket = bin.BULib.genRandString(20)
    s = socket.socket()
    s.connect((dest[1], dest[2]))
    s.write("GIVEFILE\nname:"+fileName+"\nuser:"+login+"\nticket:"+ticket+"\nmodified:"+modified)

    answer = s.recv()

    s.close()

    return answer.decode()

@myDebug
def getList(msg):
    if not checkRequest(msg) : return "WRONG REQUEST"
    usrLogin = msg[1][6:]
    files = DataBase.select("SELECT name, modified FROM files WHERE user_id='" + usrLogin + "' group by name, modified;")
    fileList = "Files:\n"
    print("\n\n---> " + str(files) + "\n\n")
    for row in files:
        for var in row:
            fileList += str(var) + "|"
        # I'm sorry for that :(
        fileList = fileList[0:-1]

    return fileList;


@myDebug
def deleteFile(msg):
    login = msg[1].split(":")[1]
    fileName = msg[2].split(":")[1]
    modified = msg[3].split(":")[1]
    slaves = DataBase.select("SELECT ")

@myDebug
def checkRequest(msg):
    if not (msg[1][0:6] == "login:") : return 0
    usrLogin = msg[1][6:]
    tmp = DataBase.getValues("users", ["id"], [("login", usrLogin)])
    if len(tmp()) == 0 : return 0
    return 1

def complete_download(msg) :
    file = msg[1].split(":")[1]
    user = msg[2].split(":")[1]
    modified = msg[3].split(":")[1]
    slave_id = msg[4].split(":")[1]
    size = msg[4].split(":")[1]

    DataBase.insertValues("files", [file, size, login, slave_id, modified])

