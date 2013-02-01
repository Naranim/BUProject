from multiprocessing.connection import answer_challenge
import threading
from socket import *
import master_server.ClientMasterProtocol
from master_server.main import *



class ClientThread(threading.Thread):
    def __init__(self, client, clientAddress):
        threading.Thread.__init__(self)
        print("Making thread ")
        self.client = client
        self.clientAddress = clientAddress



    def handleClient(self, client, address):
        print("handleClient thread")

        msg = client.recv(1024)
        msg = msg.decode().split("\n")

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

        print("Sending response: " + answer)
        client.send(answer.encode('UTF-8'))
        client.close()

        print(msg)
        print("After msg")


    def run(self):
        self.handleClient(self.client, self.clientAddress)