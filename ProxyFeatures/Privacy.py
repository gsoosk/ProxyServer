import re

class Privacy:
    enable = None
    userAgent = None

    def __init__(self , config):
        self.enable = config['enable']
        self.userAgent = config['userAgent']

    def setUserAgent(self , request):
        
        if self.enable :
            lines = request.splitlines()
            newRequest = ""
            for line in lines:
                if line.find("User-Agent:") is not -1:
                    line = ""
                    line = "User-Agent: "
                    line += self.userAgent
                    
                newRequest += line
                newRequest += "\r\n"
            return newRequest.encode()
        else:
            return request.encode()


