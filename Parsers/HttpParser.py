class HttpParser:
    @staticmethod
    def getUrl(request):
        # parse the first line
        first_line = request.split('\n')[0]
        # get url
        url = first_line.split(' ')[1]
        return url
