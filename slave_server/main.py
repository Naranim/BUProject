__author__ = 'ciemny'

import socket, threading, _thread, os
from slave_server.SlaveConfig import *
from slave_server.SlaveMasterProtocol import *

if __name__ == '__main__' :
    try :
        os.mkdir("file_sys")
    except FileExistsError :
        pass


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", SlavePort))

    while True :
        (targetSocket, targetAddress) = s.accept()
        massage = targetSocket.recv(1024)
        massage = massage.decode("UTF-8").split("\n")
        if massage[0] == 'GETFILE' :
            thr = _thread.start_new_thread(getFile(), (targetSocket, massage))
        elif massage[0] == 'GIVEFILE' :
            thr = _thread.start_new_thread(giveFile(), (targetSocket, massage))
        elif massage[0] == 'DELETE' :
            thr = _thread.start_new_thread(deleteFile(), (targetSocket, massage))
        elif massage[0] == 'REPORT' :
            thr = _thread.start_new_thread(reportState(), (targetSocket, massage))