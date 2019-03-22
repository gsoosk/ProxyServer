import json

class JsonParser(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)