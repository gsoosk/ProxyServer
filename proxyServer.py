from Proxy import Proxy
from Parsers import JsonParser

def main():
    configFile = open("config.json","r")
    # config = JsonParser.JsonParser(configFile.read())
    config = {'port' : 8090}
    proxy = Proxy(config)
    proxy.acceptClients()


if __name__ == "__main__":
    main()