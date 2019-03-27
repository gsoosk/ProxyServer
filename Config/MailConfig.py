from socket import *
import base64
import time

class Mail :
    clientSocket = None
    msg = None
    mailServer = None
    endMsg = "\r\n.\r\n"
    def __init__(self):
        self.mailServer = ("mail.ut.ac.ir", 25)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

    def sendMail(self, msg):
        self.msg = msg
        self.clientSocket.connect(self.mailServer)
        recv = self.clientSocket.recv(1024)
        recv = recv.decode()
        print("Message after connection request:" + recv)



