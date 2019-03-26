from Parsers.HttpParser import HttpParser
class ResponseInjector:
    enable = None
    postBody = None
    navbar = ""
    def __init__(self, config):
        self.enable = config['enable']
        self.postBody = config['post']['body']
        self.navbar = '''<nav style="background: rgb(0, 117, 108);position:fixed;top:0;width:100%;height:50px;z-index:100000;">
                            <p style="color:white; direction:rtl; display:flex; justify-content:center; padding:10px; font-family:sans-serif;">'''
        self.navbar += self.postBody
        self.navbar += '''   </p>
                        </nav>
                        <div style="width:100%;height:50px">
                        </div>'''
    def injectPostBody(self, header, response, request):
        if not self.enable :
            return True, response
        if HttpParser.isIndexReq(request) and HttpParser.isResponseStatusOk(header):
            resStr = response.decode(errors='ignore')
            if not resStr.find('<body') == -1 :
                bodyIndex = resStr.find('<body')
                endIndex = resStr.find('>', bodyIndex)
                newResStr = resStr[:endIndex + 1] + self.navbar + resStr[endIndex + 1:]
                print(newResStr)
                return True, newResStr.encode()
            else:
                return False, response
        else:
            return True, response


