from Parsers.HttpParser import HttpParser
from Config.HtmlConfig import getAlertHtml
from Config.HttpConfig import getOkResponseData
class Alert:

    enable = None
    targets = None
    alertMsg = 'شما توانایی اتصال به این وبسایت را ندارید.' \
                '\n'\
               '\n این وبسایت توسط پروکسی مسدود شده است.'
    def __init__(self, config):
        self.enable = config['enable']
        self.targets = config['targets']

    def doesItRestricted(self, request):
        hostname = HttpParser.getHostName(request)
        for target in self.targets:
            if hostname == target['URL']:
                return True
        return False

    def handleRestrictedRequest(self, clientSocket, log, request):
        html = getAlertHtml(self.alertMsg)
        data = getOkResponseData(html)

        clientSocket.send(data)
        log.addRestricted()

        if self.shouldNotify(request) :
            self.notifyAdmin()
            log.addAdminNotified()

    def shouldNotify(self, request):
        hostname = HttpParser.getHostName(request)
        for target in self.targets:
            if hostname == target['URL']:
                return target['notify']
        return False

    def notifyAdmin(self):
        #TODO:Complete email notification
        print('notif')
