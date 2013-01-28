__author__ = 'ciemny'
from slave_server.SlaveConfig import *
import socket
import os
import time

def generateFileList() :
    filesPath = os.getcwd() + "/file_sys"
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


def reportDownloadComplete():
    pass

def reportUploadComplete():
    pass

def getFile():
    pass

def giveFile():
    pass

if __name__ == '__main__' :
    connectToMaster()