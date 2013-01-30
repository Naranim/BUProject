__author__ = 'ciemny'
from slave_server.SlaveConfig import *
import socket
import os
import time
import shutil

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
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        fallowers = []
        for i in range(4, len(massage)) :
            try :
                tmpSocket = socket.socket()
                socket.connect((massage[i].split(":")[1], massage[i].split(":")[2]))
                tmpSocket.send(ticket)
                fallowers.append(tmpSocket)
            except ConnectionRefusedError :
                pass
            except ConnectionError :
                pass

        answer = "READY\nPORT:" + str(port)
        s.send(answer.encode())
        s.close()
        sock.settimeout(TICKET_TIMEOUT)
        (clientSocket, clientAddress) = sock.accept()
        request = clientSocket.recv(1024)
        if request == ticket :
            clientSocket.send("READY\n".encode())
            try:
                os.mkdir(FILES_PATH + user)
            except FileExistsError :
                pass

            file = open(FILES_PATH + user + "/" + fileName)
            while True:
                data = clientSocket.recv(1024)
                if not data :
                    break
                file.write(data)
                for s in fallowers :
                    s.send(data)

        else :
            clientSocket.send("WRONG TICKET".encode())

    except socket.timeout :
        print("File from %s, ticket: %stimed out." % (user, ticket))
    except socket.error :
        print("Error getting file: " + fileName + " from " + user)
    finally:
        sock.close()
        file.close()


def giveFile(s, massage):
    try:
        fileName = massage[1].split(":")[1]
        user = massage[2].split(":")[1]
        ticket = massage[3].split(":")[1]
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        if not os.path.isfile(FILES_PATH + user + "/" + fileName) :
            answer = "NOFILE"
            s.send(answer.encode())
            s.close()
            return


        s.close()
        answer = "READY\nPORT:" + str(port)
        s.send(answer.encode())
        s.close()
        sock.settimeout(TICKET_TIMEOUT)
        (clientSocket, clientAddress) = sock.accept()
        request = clientSocket.recv(1024)
        if request == ticket :

            file = open(FILES_PATH + user + "/" + fileName)
            while True:
                data = file.read(1024)
                if not data :
                    break
                clientSocket.send(data)

        else :
            clientSocket.send("WRONG TICKET".encode())

    except socket.timeout :
        print("File to %s, ticket: %stimed out." % (user, ticket))
    except socket.error :
        print("Error sending file: " + fileName + " to " + user)
    finally:
        sock.close()
        file.close()

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