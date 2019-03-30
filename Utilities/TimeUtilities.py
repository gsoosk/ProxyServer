import email.utils as eut
import datetime

class TimeUtilities:
    @staticmethod
    def convertToDate(string):
        return datetime.datetime(*eut.parsedate(string)[:6])

    @staticmethod
    def nowTime():
        return datetime.datetime.now()