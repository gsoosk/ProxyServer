def getOkResponseData(html):
    data = 'HTTP/1.1 200 OK' \
           'Server: Proxy' \
           'Content-Type: text/html; charset=utf-8\r\n\r\n'
    data += html
    return data.encode()
