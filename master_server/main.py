from socket import *
import queue
import threading
from master_server import ClientThread
from master_server.BUConfig import *

global connectionsQueue
global MSDataBase
global condition

connectionsQueue = queue.Queue()
condition = threading.Condition()


if __name__ == "__main__" :
    "main of mains"

    # Socket
    MSSocket = socket(AF_INET, SOCK_STREAM)
    MSSocket.bind(("", MS_PORT))
    MSSocket.listen(10)
    print("main started")

    # Threads production
    threadList = []
    for i in range(3) :
        CT = ClientThread.ClientThread(i, condition, connectionsQueue)
        CT.start()
        threadList.append(CT)

    # main while
    while 1 :
        print("Waiting for a connection...")
        (MSClient, clientAddress) = MSSocket.accept()
        print("New connection from: " + str(clientAddress))
        condition.acquire()
        try:
            connectionsQueue.put((MSClient, clientAddress))
        finally:
            condition.notifyAll()
            condition.release()


    MSSocket.close()
