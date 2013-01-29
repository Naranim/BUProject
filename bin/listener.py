__author__ = 'ciemny'

from socket import *
import sys


port = int(sys.argv[1])
s = socket(AF_INET, SOCK_STREAM)
s.bind(("", port))
s.listen(1)
(conn, client_addr) = s.accept()
print("New connection from: " + str(client_addr))
data = conn.recv(1000000)
try :
    conn.send("DELETE:\nala:heh|lol\nuser:cv.doc\n>>>".encode())
    data = data.decode("UTF-8")
    print(data)
finally:
    conn.close()
    s.close()


