import jsonParser

def main():
    configFile = open("config.json","r")
    config = jsonParser.JsonParser(configFile.read())


if __name__ == "__main__":
    main()