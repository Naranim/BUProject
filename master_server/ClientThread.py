from multiprocessing.connection import answer_challenge
import threading
from socket import *
import master_server.ClientMasterProtocol
from master_server.main import *



class ClientThread(threading.Thread):
    def __init__(self, threadId, condition, connectionsQueue):
        print("Making thread " + str(threadId))
        self.threadId = threadId
        self.condition = condition
        self.connectionsQueue = connectionsQueue
        threading.Thread.__init__(self)


    def handleClient(self, client, address):
        print("handleClient thread : " + str(self.threadId))

        msg = client.recv(1024)
        msg = msg.decode('utf-8').split("\n")

        answer = ""
        header = msg[0]

        if header == "LOGIN" :
            answer = master_server.ClientMasterProtocol.login(msg)
        elif header == "DOWNLOAD" :
            answer = master_server.ClientMasterProtocol.download(msg)
        elif header == "UPLOAD" :
            answer = master_server.ClientMasterProtocol.upload(msg)
        elif header == "GETLIST" :
            answer = master_server.ClientMasterProtocol.getList(msg)
        else :
            answer = "WRONG HEADER"

        print("I wanna send !")
        client.send(answer.encode('UTF-8'))

        print(msg)
        print("After msg")


    def run(self):
        while True :
            gotConnection = False
            client = socket(AF_INET, SOCK_STREAM)
            address = ()

            condition.acquire()
            try:
                while 1:
                    if not self.connectionsQueue.empty() :
                        (client, address) = self.connectionsQueue.get()
                        gotConnection = True
                        print("thread " + str(self.threadId) + " has new connection")
                        break
                    else :
                        print("thread " + str(self.threadId) + " sleeps")
                        self.condition.wait()
                        print("thread " + str(self.threadId) + " wakes up")
            finally :
                self.condition.release()

            if gotConnection :
                self.handleClient(client, address)
                client.close()
