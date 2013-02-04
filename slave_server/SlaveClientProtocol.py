__author__ = 'ciemny'

import socket, time
from  slave_server.SlaveConfig import *

def getFile(s, fileName, user, ticket, fallowersAddresses, modified, slave_id):
    """
    Metoda pobierajaca plik od klienta. Zapisuje go w FILES_PATH/[login]/[data_modyfikacji]/
    Jako argumenty przyjmuje socket master serwera, nazwe pliku, login, ticket, i date modyfikacji.

    Zwraca "OK" jesli sie udalo, "FAILED" wpp.
    """
    try :
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

#        fallowers = []
#        for f_ip, f_addr in fallowersAddresses :
#        tmpSocket = socket.socket()
#        socket.connect((f_ip, f_addr))
#        tmpSocket.send(ticket)
#        fallowers.append(tmpSocket)
        answer = "READY\nPORT:" + str(port)
        s.send(answer.encode())
        s.close()
        sock.settimeout(TICKET_TIMEOUT)

        print("Waiting for client, port: " + str(port))

        sock.listen(10)
        (clientSocket, clientAddress) = sock.accept()
        request = clientSocket.recv(1024).decode()
        if request == ticket :
            clientSocket.send("READY\n".encode())
            try:
                os.mkdir(FILES_PATH + modified + "/" + user)
            except IOError :
                pass
            file = open(FILES_PATH + user + "/" + fileName, "wb")
            while True:
                data = clientSocket.recv(1024)
                if not data :
                    break
                file.write(data)
#                for f in fallowers :
#                    f.send(data)

        else :
            clientSocket.send("WRONG TICKET".encode())
            clientSocket.close()
            print(request)
            return "FAILED"

        clientSocket.close()
        print("Sending complete")
        sock.close()
        file.close()
    except socket.timeout :
        print("File from %s, ticket: %s timed out." % (user, ticket))
        return "FAILED"
    except socket.error :
        print("Error getting file: " + fileName + " from " + user)
        return "FAILED"


    return "OK"

def giveFile(s, fileName, user, ticket, modified):
    """
    Metoda do wyslania pliku do klienta.
    Jako argumenty przyjmuje socket master serwera, nazwe pliku, login, ticket, i date modyfikacji.

    Zwraca "OK" jesli sie udalo, "FAILED" wpp.
    """
    try:
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        if not os.path.isfile(FILES_PATH + user + "/" + fileName) :
            answer = "NOFILE"
            s.send(answer.encode())
            s.close()
            return "FAILED"

        if not os.path.isfile(FILES_PATH + user + "/" + + modified + "/" + fileName) :
            answer = "NOFILE"
            s.send(answer.encode())
            s.close()
            return "FAILED"


        answer = "READY\nPORT:" + str(port)
        s.send(answer.encode())
        s.close()
        sock.settimeout(TICKET_TIMEOUT)
        sock.listen(10)
        print("Waiting for client, port: " + str(port))
        (clientSocket, clientAddress) = sock.accept()
        request = clientSocket.recv(1024).decode()
        file = open(FILES_PATH + user + "/" + fileName, "rb")
        if request == ticket :
            print("Good ticket")
            print(FILES_PATH + user + "/" + fileName)
            while True:
                data = file.read(1024)
                print("Sending...")
                time.sleep(0.01)
                if not data :
                    print("End of data")
                    break
                clientSocket.send(data)

        else :
            print("wrong ticket")
            clientSocket.send("WRONG TICKET".encode())
            clientSocket.close()
            return "FAILED"

        clientSocket.close()
        print("Sending complete")
        sock.close()
        file.close()

    except socket.timeout :
        print("File to %s, ticket: %s timed out." % (user, ticket))
        return "FAILED"
    except socket.error :
        print("Error sending file: " + fileName + " to " + user)
        return "FAILED"
    return "OK"


if __name__ == '__main__' :
    giveFile(None, "file.jpg", "root", "A")