class HttpParser:
    @staticmethod
    def getUrl(request):
        # parse the first line
        first_line = request.split('\n')[0]
        # get url
        url = first_line.split(' ')[1]
        return url

    @staticmethod
    def findWebserverPosAndPortPos(url):
        http_pos = url.find("://")  # find pos of ://
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]  # get the rest of url

        port_pos = temp.find(":")  # find the port pos (if any)

        # find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        return temp, webserver_pos, port_pos

    @staticmethod
    def getHostAndIp(url):

        newUrl, webserver_pos, port_pos = HttpParser.findWebserverPosAndPortPos(url)

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:

            # default port
            port = 80
            webserver = newUrl[:webserver_pos]

        else:  # specific port
            port = int((newUrl[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = newUrl[:port_pos]

        return webserver, port

    @staticmethod
    def getResponseHeader(data):

        for i in range(len(data)):
            r = b'\r'[0]
            n = b'\n'[0]
            #when we have \r\n\r\n we reached end of header
            if i <= len(data) - 4 and data[i] == r and data[i+1] == n and data[i+2] == r and data[i+3] == n:
                return data[:i+2]


    @staticmethod
    def changeHttpVersion(request):
        reqStr = request.decode(errors = 'ignore')
        reqStr = reqStr.replace('HTTP/1.1', 'HTTP/1.0', 1)
        return reqStr.encode()

    @staticmethod
    def removeHostname(request):
        reqStr = request.decode(errors = 'ignore')
        reqStr = reqStr.split('\r\n')

        httpFirstLine = reqStr[0].split(' ')
        url = httpFirstLine[1]

        newUrl, webserverPos, portPos = HttpParser.findWebserverPosAndPortPos(url)

        if webserverPos == len(newUrl):
            newUrl = '/'
        else:
            newUrl = newUrl[webserverPos:]


        httpFirstLine[1] = newUrl
        reqStr[0] = ' '.join(httpFirstLine)
        reqStr = '\r\n'.join(reqStr)
        return reqStr.encode()

    @staticmethod
    def removeProxyConnection(request):
        reqStr = request.decode(errors = 'ignore')
        reqStr = reqStr.split('\r\n')
        for i in range(len(reqStr)) :
            if reqStr[i].split(' ')[0] == 'Connection:' :
                reqStr[i] = 'Connection: Close'
                break

        for i in range(len(reqStr)) :
            if reqStr[i].split(' ')[0] == 'Proxy-Connection:' :
                reqStr.pop(i)
                break

        reqStr = '\r\n'.join(reqStr)
        return reqStr.encode()

    @staticmethod
    def isIndexReq(request):

        reqStr = request.decode(errors = 'ignore')
        try:
            return reqStr.split('\r\n')[0].split(' ')[1] == '/'
        except :
            return False
    @staticmethod
    def isResponseStatusOk(responseHeader):
        resStr = responseHeader.decode(errors = 'ignore')
        try:
            return resStr.split('\n')[0].split(' ')[1] == '200'
        except:
            return False

    @staticmethod
    def changeAcceptEncoding(request):
        reqStr = request.decode(errors = 'ignore')
        reqStr = reqStr.split('\r\n')
        for i in range(len(reqStr)) :
            if reqStr[i].split(' ')[0] == 'Accept-Encoding:' :
                reqStr[i] = 'Accept-Encoding: identity'
                break
        reqStr = '\r\n'.join(reqStr)
        return reqStr.encode()

    @staticmethod
    def getHostName(request):
        reqStr = request.decode(errors = 'ignore')
        reqStr.split('\r\n')
        reqStr = reqStr.split('\r\n')
        for i in range(len(reqStr)) :
            if reqStr[i].split(' ')[0] == 'Host:' :
                return reqStr[i].split(' ')[1]
        return ''