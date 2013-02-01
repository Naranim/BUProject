from socket import *
import queue
import threading
from master_server.ClientThread import *
from master_server.BUConfig import *


global MSDataBase


connectionsQueue = queue.Queue()
condition = threading.Condition()


if __name__ == "__main__" :
    "main of mains"

    # Socket
    MSSocket = socket(AF_INET, SOCK_STREAM)
    #MSSocket.bind(("", MS_PORT))
    MSSocket.bind(("", 0))
    MSSocket.listen(10)
    print("main started on port " + str(MSSocket.getsockname()[1]))

    # main while
    while 1 :
        print("Waiting for a connection...")
        (MSClient, clientAddress) = MSSocket.accept()
        print("New connection from: " + str(clientAddress))
        th = ClientThread(MSClient, clientAddress)
        th.start()



    MSSocket.close()
