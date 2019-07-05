from Parsers.HttpParser import HttpParser
class ResponseInjector:
    enable = None
    postBody = None
    def __init__(self, config):
        self.enable = config['enable']
        self.postBody = config['post']['body']
    def injectPostBody(self, header, response, request):
        res = response
        if not self.enable :
            return True
        if HttpParser.isIndexReq(request) and HttpParser.isResponseStatusOk(header):
            print(res.decode())
            # TODO: COMPLETE THIS FUNCTION
            return False
        else:
            return True
        return True



