from Proxy import Proxy
from Parsers import JsonParser

def main():
    configFile = open("config.json","r")
    config = JsonParser.JsonParser(configFile.read())
    proxy = Proxy(config.__dict__)
    proxy.acceptClients()


if __name__ == "__main__":
    main()