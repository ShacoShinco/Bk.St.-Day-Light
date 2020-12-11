import urllib.request
from bs4 import BeautifulSoup
from re import split
from datetime import datetime
from datetime import timedelta

class MineEngine(object):
    def __init__(self):
        super().__init__()
        self.mainPage = self.getMainPage()

    @property
    def mainPage(self):
        if datetime.now() - self.main_cache[1] < timedelta(minutes=15):
            return self.main_cache[0]
        else:
            self.mainPage = getMainPage()
            return self.mainPage

    @mainPage.setter
    def mainPage(self, page):
        self.main_cache = self.getMainPage(), datetime.now()

    @staticmethod
    def getMainPage():
        return urllib.request.urlopen('http://baker-forum.ir/').read()

    @property
    def bsObject(self):
        return BeautifulSoup(self.mainPage, 'html.parser')

    def getOnlineUserNumber(self):
        bs = self.bsObject
        return split("\D+", bs.select("#boardstats_e > tr:nth-child(2) > td").__str__())[3]

    def getOnlineMemberNumber(self):
        bs = self.bsObject
        return split("\D+", bs.select("#boardstats_e > tr:nth-child(2) > td").__str__())[5]

    def getOnlineHiddenMemberNumber(self):
        bs = self.bsObject
        return split("\D+", bs.select("#boardstats_e > tr:nth-child(2) > td").__str__())[6]

    def getOnlineGuestNumber(self):
        bs = self.bsObject
        return split("\D+", bs.select("#boardstats_e > tr:nth-child(2) > td").__str__())[7]

print(MineEngine().getOnlineUserNumber())