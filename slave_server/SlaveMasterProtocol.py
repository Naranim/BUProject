__author__ = 'ciemny'
from slave_server.SlaveConfig import *
import socket
import os
import time
import shutil
import slave_server.SlaveClientProtocol
from _thread import *

def generateFileList() :
    filesPath = FILES_PATH
    ret = []
    for login in os.listdir(filesPath) :
        ret += [login + ":"] + [s + '|' for s in os.listdir(filesPath + '/' + login)] + ['\n']
    return ''.join(ret)


def connectToMaster() :
    """

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
        #TODO
        # DELETE FILES, UNKNOWN
        answer = answer.decode().split("\n")
        print(answer)


def reportDownloadComplete(file, md5):
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MasterAddress, MasterPort))
        s.send("DOWNLOAD_COMPLETE\n" + file + "\n" + md5)
    finally:
        s.close()

def reportUploadComplete(file, md5):
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MasterAddress, MasterPort))
        s.send("UPLOAD_COMPLETE\n" + file + "\n" + md5)
    finally:
        s.close()

def getFile(s, massage):
    try:
        fileName = massage[1].split(":")[1]
        user = massage[2].split(":")[1]
        ticket = massage[3].split(":")[1]
        md5 = massage[4].split(":")[1]
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        fallowersAddresses = []
        for i in range(5, len(massage)) :
            fallowersAddresses.append((massage[i].split(":")[1], massage[i].split(":")[2]))


    except socket.error :
        print("Error getting file: " + fileName + " from " + user)

    res = slave_server.SlaveClientProtocol.getFile(s, fileName, user, ticket, fallowersAddresses)

    reportDownloadComplete(res, fileName, md5, user)


def giveFile(s, massage):
    try:
        fileName = massage[1].split(":")[1]
        user = massage[2].split(":")[1]
        ticket = massage[3].split(":")[1]
        md5 = massage[4].split(":")[1]
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

    reportDownloadComplete(res, fileName, md5, user)



def moveFileFromTmp(massage) :
    fileName = massage[1].split(":")[1]
    user = massage[2].split(":")[1]
    try :
        shutil.move(TMP_PATH + user + "/" + fileName, FILES_PATH + user)
    except FileNotFoundError:
        print("Error moving " + fileName)

def moveFileToTmp(massage) :
    fileName = massage[1].split(":")[1]
    user = massage[2].split(":")[1]
    try :
        shutil.move(FILES_PATH + user + "/" + fileName, TMP_PATH + user)
    except FileNotFoundError:
        print("Error moving " + fileName)

def deleteFile(s, massage):
    fileName = massage[1].split(":")[1]
    user = massage[2].split(":")[1]
    try:
        os.remove(FILES_PATH + user + "/" + fileName)
    except FileNotFoundError:
        print("Error deleting " + fileName)

def deleteFileInTmp(massage):
    fileName = massage[1].split(":")[1]
    user = massage[2].split(":")[1]
    try:
        os.remove(TMP_PATH + user + "/" + fileName)
    except FileNotFoundError:
        print("Error deleting " + fileName)

def reportState(s, massage):
    s.close()
    connectToMaster()


if __name__ == '__main__' :
    connectToMaster()