class HttpParser:
    @staticmethod
    def getUrl(request):
        # parse the first line
        first_line = request.split('\n')[0]
        # get url
        url = first_line.split(' ')[1]
        return url

    @staticmethod
    def getHostAndIp(url):
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

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:

            # default port
            port = 80
            webserver = temp[:webserver_pos]

        else:  # specific port
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

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
        reqStr = request.decode()
        reqStr = reqStr.replace('HTTP/1.1', 'HTTP/1.0', 1)
        return reqStr.encode()

