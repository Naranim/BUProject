from multiprocessing.connection import answer_challenge
import threading
from socket import *
import master_server.ClientMasterProtocol
from master_server.main import *



class ClientThread(threading.Thread):
    """
    Klasa watku do obslugi klienta polaczonego z glownym serwerem.
    """
    def __init__(self, client, clientAddress):
        """
        konstruktor ClientThrerad
        Jako argumenty przyjmuje socket klienta i jego adres
        """
        threading.Thread.__init__(self)
        print("Making thread ")
        self.client = client
        self.clientAddress = clientAddress



    def handleClient(self, client, address):
        """
        Obsluga zapytania od klienta
        dostaje socket i adres, odczytuje zapytanie i je rozpatruje
        """
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
        elif header == "COMPLETE_DOWNLOAD" :
            answer = master_server.ClientMasterProtocol.complete_download(msg)
        else :
            answer = "WRONG HEADER"

        print("Sending response: " + answer)
        client.send(answer.encode('UTF-8'))
        client.close()

        print(msg)
        print("After msg")


    def run(self):
        """
        Nadpisana metoda run. Uruchamiana jest podczas uruchomienia watku.
        """
        self.handleClient(self.client, self.clientAddress)