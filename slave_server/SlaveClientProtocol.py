__author__ = 'ciemny'

import socket
from  slave_server.SlaveConfig import *

def getFile(s, fileName, user, ticket, fallowersAddresses):
    try:
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        fallowers = []
        for f_ip, f_addr in fallowersAddresses :
            try :
                tmpSocket = socket.socket()
                socket.connect((f_ip, f_addr))
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

            file = open(FILES_PATH + user + "/" + fileName, "wb")
            while True:
                data = clientSocket.recv(1024)
                if not data :
                    break
                file.write(data)
                for f in fallowers :
                    f.send(data)

        else :
            clientSocket.send("WRONG TICKET".encode())
            clientSocket.close()
            return "FAILED"

        clientSocket.close()

    except socket.timeout :
        print("File from %s, ticket: %stimed out." % (user, ticket))
        return "FAILED"
    except socket.error :
        print("Error getting file: " + fileName + " from " + user)
        return "FAILED"
    finally:
        sock.close()
        file.close()

    return "OK"

def giveFile(s, fileName, user, ticket):
    try:
        sock = socket.socket()
        sock.bind(("", 0))
        port = sock.getsockname()[1]

        if not os.path.isfile(FILES_PATH + user + "/" + fileName) :
            answer = "NOFILE"
            s.send(answer.encode())
            s.close()
            return

        answer = "READY\nPORT:" + str(port)
        s.send(answer.encode())
        s.close()
        sock.settimeout(TICKET_TIMEOUT)
        (clientSocket, clientAddress) = sock.accept()
        request = clientSocket.recv(1024)
        if request == ticket :

            file = open(FILES_PATH + user + "/" + fileName, "rb")
            while True:
                data = file.read(1024)
                if not data :
                    break
                clientSocket.send(data)

        else :
            clientSocket.send("WRONG TICKET".encode())
            clientSocket.close()
            return "FAILED"

        clientSocket.close()

    except socket.timeout :
        print("File to %s, ticket: %stimed out." % (user, ticket))
        return "FAILED"
    except socket.error :
        print("Error sending file: " + fileName + " to " + user)
        return "FAILED"
    finally:
        sock.close()
        file.close()

    return "OK"
