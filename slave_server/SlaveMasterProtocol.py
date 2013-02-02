__author__ = 'ciemny'
from slave_server.SlaveConfig import *
import socket
import os
import time
import shutil
import slave_server.SlaveClientProtocol
from _thread import *

def generateFileList() :
    """
    Zwraca string zawierajacy pelna informacje o przechowywanych plikach
    """
    filesPath = FILES_PATH
    ret = []
    for login in os.listdir(filesPath) :
        ret += [login + ":"] + [s + '|' for s in os.listdir(filesPath + '/' + login)] + ['\n']
    return ''.join(ret)


def connectToMaster() :
    """
    Metoda do nawiazania pierwszego polaczanie z master serwerem w razie awarii.
    Pozwala na wygenerowanie raportu o zawartych plikach i przeslaniu go na serwer glowny
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    connected = False
    while not connected:
        print("Attempting to connect to master: " + MasterAddress + ":" + str(MasterPort))
        try :
            s.connect((MasterAddress, MasterPort))
        except socket.timeout :
            print("Connection timed out.")
            continue
        except socket.error :
            print("Refused.")
            time.sleep(5)
            continue
        connected = True
        s.send(str("REPORT\nName:" + SlaveName + "\n" + generateFileList() + ">>>").encode())
        answer = s.recv(100000)
        answer = answer.decode().split("\n")
        print(answer)


def reportDownloadComplete(file, user, modified, slave_id):
    """
    raport dla master serwera o zakonczeniu pobierania
    pliku file
    od uzytkownika user
    zmodyfikowanego modified
    """
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MasterAddress, MasterPort))
        massage = "COMPLETE_DOWNLOAD\nfile:" + file + "\nuser" + user + "\nmodified" + modified + "\nslave:" + slave_id
        s.send(massage.encode())
    finally:
        s.close()

#def reportUploadComplete(file, user, modified):
#    """
#    raport dla master serwera o zakonczeniu wysylania
#    pliku file
#    od uzytkownika user
#    zmodyfikowanego modified
#    """

#    try :
#        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        s.connect((MasterAddress, MasterPort))
#        s.send("UPLOAD_COMPLETE\n" + file + "\n" + md5)
#    finally:
#        s.close()

def getFile(s, massage):
    """
    Metoda do przygotowania pobierania pliku na slava
    Slave przechodzi w stan oczekiwania na klienta (TICKET_TIMEOUT sekund) oraz daje masterowi
    dane potrzebne klientowi do nawiazania polaczenia

    Argument to socket i zapytanie od master serwera
    """
    try:
        fileName = massage[1].split(":")[1]
        user = massage[2].split(":")[1]
        ticket = massage[3].split(":")[1]
        slave_id = massage[4].split(":")[1]
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        fallowersAddresses = []
        for i in range(5, len(massage)) :
            fallowersAddresses.append((massage[i].split(":")[1], massage[i].split(":")[2]))


    except socket.error :
        print("Error getting file: " + fileName + " from " + user)

    res = slave_server.SlaveClientProtocol.getFile(s, fileName, user, ticket, fallowersAddresses, slave_id)

    reportDownloadComplete(res, fileName, user)


def giveFile(s, massage):
    """
    Metoda do przygotowania pobierania pliku przez klienta
    Slave przechodzi w stan oczekiwania na klienta (TICKET_TIMEOUT sekund) oraz daje masterowi
    dane potrzebne klientowi do nawiazania polaczenia

    Argument to socket i zapytanie od master serwera
    """

    try:
        fileName = massage[1].split(":")[1]
        user = massage[2].split(":")[1]
        ticket = massage[3].split(":")[1]
        slave_id = massage[4].split(":")[1]
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        if not os.path.isfile(FILES_PATH + user + "/" + fileName) :
            answer = "NOFILE"
            s.send(answer.encode())
            s.close()
            return

    except socket.error :
        print("Error sending file: " + fileName + " to " + user)

    res = slave_server.SlaveClientProtocol.giveFile(s, fileName, user, ticket)

    reportDownloadComplete(res, fileName, user)


def deleteFile(massage):
    """
    metoda do usuwania konkretnego pliku z serwera

    Argument to zapytanie od master serwera
    """
    fileName = massage[1].split(":")[1]
    user = massage[2].split(":")[1]
    try:
        os.remove(FILES_PATH + user + "/" + fileName)
    except IOError:
        print("Error deleting " + fileName)


def reportState(massage):
    """
    Metoda do raportowania swojego stanu masterowi.Generuje liste przechowywanych plikow

    Argument to zapytanie od master serwera
    """
    connectToMaster()


if __name__ == '__main__' :
    connectToMaster()