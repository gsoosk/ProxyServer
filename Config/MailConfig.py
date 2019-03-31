from socket import *
import base64
import time

class Mail :
    clientSocket = None
    msg = None
    mailServer = None
    endMsg = "\r\n.\r\n"
    adminMail = 'farzad.habibi@ut.ac.ir'
    mailSubject = None

    myMail = 'farzad.habibi@ut.ac.ir'
    myUserName = "farzad.habibi"
    myPass = "%fH12345678"
    def __init__(self):
        self.mailServer = ("mail.ut.ac.ir", 25)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

    def sendMail(self, msg, mailSubject, log):
        self.mailSubject = mailSubject
        self.msg = msg
        try :
            self.connectServer(log)
            self.helloServer(log)
            self.authorize(log)
            self.sendToAdminMail(log)
            self.quitServer(log)
        except Exception as e :
            log.addMailLog('Error : ' + e.__str__())

    def connectServer(self, log):
        self.clientSocket.connect(self.mailServer)
        recv = self.clientSocket.recv(1024)
        recv = recv.decode()
        log.addMailLog("Message after connection request:" + recv[:-1])
        if recv[:3] != '220':
            raise Exception('220 reply not received from server.')

    def helloServer(self, log):
        heloCommand = 'HELO mail.ut.ac.ir\r\n'
        self.clientSocket.send(heloCommand.encode())
        recv = self.clientSocket.recv(1024)
        recv = recv.decode()
        log.addMailLog("Message after EHLO command:" + recv[:-1])
        if recv[:3] != '250':
            raise Exception('250 reply not received from server.')

    def authorize(self, log):
        # Info for username and password
        username = self.myUserName
        password = self.myPass
        base64_str = ("\x00" + username + "\x00" + password).encode()
        base64_str = base64.b64encode(base64_str)
        authMsg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
        self.clientSocket.send(authMsg)
        recv_auth = self.clientSocket.recv(1024)
        log.addMailLog("Message after AUTH command:" + recv_auth.decode()[:-1])

    def sendToAdminMail(self, log):
        mailFrom = "MAIL FROM: <{}>\r\n".format(self.myMail)
        self.clientSocket.send(mailFrom.encode())
        recv = self.clientSocket.recv(1024)
        log.addMailLog("After MAIL FROM command: " + recv.decode()[:-1] )

        rcptTo = "RCPT TO:<{}>\r\n".format(self.adminMail)
        self.clientSocket.send(rcptTo.encode())
        recv = self.clientSocket.recv(1024)
        log.addMailLog("After RCPT TO command: " + recv.decode()[:-1])

        data = "DATA\r\n"
        self.clientSocket.send(data.encode())
        recv = self.clientSocket.recv(1024)
        log.addMailLog("After DATA command: " + recv.decode()[:-1])

        self.sendHeaders()

        self.clientSocket.send(self.msg.encode())
        self.clientSocket.send(self.endMsg.encode())
        recv_msg = self.clientSocket.recv(1024)
        log.addMailLog("Response after sending message body:" + recv_msg.decode()[:-1])

    def sendHeaders(self):
        date = 'Date: '
        date += time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        date += "\r\n"
        self.clientSocket.send(date.encode())

        sender = 'Sender: "CN PROXY" <{}>\r\n'.format(self.myMail)
        fromMsg = 'From: "CNPROXY" <{}>\r\n'.format(self.myMail)
        self.clientSocket.send(sender.encode())
        self.clientSocket.send(fromMsg.encode())

        to = 'To: {}\r\n'.format(self.adminMail)
        self.clientSocket.send(to.encode())

        subject = "Subject: {}\r\n\r\n".format(self.mailSubject)
        self.clientSocket.send(subject.encode())

    def quitServer(self, log):
        quit = "QUIT\r\n"
        self.clientSocket.send(quit.encode())
        recv = self.clientSocket.recv(1024)
        log.addMailLog(recv.decode())
        self.clientSocket.close()