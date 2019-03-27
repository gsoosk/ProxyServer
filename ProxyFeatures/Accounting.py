from Config.HttpConfig import getOkResponseData
from Config.HtmlConfig import getAlertHtml
class Accounting:
    users = None
    userNotFoundMsg = 'شما اجازه استفاده از این پروکسی را ندارید.\n'
    usedDataOverMsg = 'شما تمام حجم حساب خود را مصرف کرده‌اید. ' \
                   '<br>' \
                   'تمامی فعالیت‌ها توسط پروکسی مسدود شده‌اند.'

    def __init__(self, config):
        self.users = config['users']
        self.initUsersUsedData()

    def initUsersUsedData(self):
        for i in range(len(self.users)):
            self.users[i]['usedData'] = 0


    def doesUserCanGetData(self, clientAddress, log):
        clientIp = clientAddress[0]
        if not self.doesUsersContainsIp(clientIp):
            log.addUserIsNotInProfiles(clientIp)
            return False

        if not self.doesUserHasVolume(clientIp):
            log.addUserUsedDataIsExtended(clientIp)
            return False

        return True


    def doesUsersContainsIp(self, IP):
        return  self.findUser(IP) >= 0

    def doesUserHasVolume(self, IP):
        userIndex = self.findUser(IP)
        return self.users[userIndex]['usedData'] < int(self.users[userIndex]['volume'])

    def findUser(self, IP):
        for i in range(len(self.users)):
            if self.users[i]['IP'] == IP:
                return i
        return -1

    def restrictUser(self, clientSocket, clientAddress, log):
        clientIp = clientAddress[0]
        msg = self.usedDataOverMsg
        if not self.doesUsersContainsIp(clientIp):
            msg = self.userNotFoundMsg

        html = getAlertHtml(msg)
        data = getOkResponseData(html)
        clientSocket.send(data)

        log.addRestricted()

    def addUserDataConsume(self, clientAddress, dataVol):
        clientIp = clientAddress[0]
        userIndex = self.findUser(clientIp)
        if userIndex < 0 :
            return
        self.users[userIndex]['usedData'] += dataVol




