import urllib.request
from bs4 import BeautifulSoup
from re import split, sub
from datetime import datetime
from datetime import timedelta

from requests import get

from datetime import datetime

import pickle
class grabber(object):
    pass
class Engine(object):
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

class User(object):
    def __init__(self, id, url = "http://baker-forum.ir/member.php?action=profile&uid=" + str(id)):
        print(url)
        raw = get(url)
        while raw.status_code != 200:
            print("problem with fetching " + url)
            raw = get(url)

        page = raw.text

        bs = BeautifulSoup(page, 'html.parser')
        self.name = bs.select("strong > span > strong")[0].string
class ChatBoxGrabber():


    class Data(object):

        def __init__(self, id, user, message, time):
            self.id = id
            self.message = message
            self.user = user
            self.time = time
        
        def __repr__(self):
                return self.user.__str__() + " at " + self.time.__str__() + " said : '" + self.message + "'" + "\n"
    
    def __init__(self):
        self.dataSet = {}

    def urlOf(self, pageNumber):
        return "http://baker-forum.ir/index.php?action=shoutbox_archive&page=" + pageNumber.__str__()
    
    @classmethod
    def getData(cls, url):
        start = datetime.now()
        raw = get(url)
        while raw.status_code != 200:
            print("problem with fetching " + url)
            raw = get(url)

        page = sub('" class=".*" />', ':' ,sub('<img src="h.*title="', ':' ,raw.text))

        bs = BeautifulSoup(page, 'html.parser')
        data = {}

        entries = bs.select(".entry")

        for entry in entries:
            id = int(entry["data-id"])
            user = int(entry.select("div.user > a")[0]["href"].split("member.php?action=profile&uid=")[1])
            message = str(entry.select(".text")[0].string)
            time = datetime.strptime(entry.select(".date")[0].string, '%H:%M:%S').time()
            data[id] = cls.Data(id, user, message, time)
        print (str(min(data.keys())) + " to " + str(max(data.keys())) + " page :" + url + " grabbed! time:" + int((datetime.now() - start).total_seconds()*1000).__str__() + " ms")
        return data
        


    def grabPageNumber(self, url = "http://baker-forum.ir/index.php?action=shoutbox_archive"):
        start = datetime.now()
        raw = get(url)
        while raw.status_code != 200:
            print("problem with fetching " + url)
            raw = get(url)

        page = raw.text

        bs = BeautifulSoup(page, 'html.parser')

        pages = int(bs.select(".pagination_last")[0].string)

        # print ("There are " + pages.__str__() + " pages ! time :" + (datetime.now() - start).total_seconds().__str__())
        return pages
    
    def grab(self, timeD):
        page = 1
        start = datetime.now()
        while datetime.now() < start + timeD:
            self.dataSet.update(self.getData(self.urlOf(page)))
            print("page " + page.__str__() + " done!")
            page += 1
        return self.dataSet

    def grabAll(self):
        page = 1
        while page <= 3546:
            self.dataSet.update(self.getData(self.urlOf(page)))
            print("page " + page.__str__() + " done!" + str(int(page*100/3546)) + "%")
            page += 1
        return self.dataSet

    def grabNew(self):
        page = 1
        counter = 0
        ans = {}
        while page <= self.grabPageNumber():
            lastPage = self.grabPageNumber()
            while page <= lastPage:
                temp = self.getData(self.urlOf(page))
                if len(temp)==0 or counter > 3:
                    page = lastPage+1
                counter += 2 * (min(temp.keys()) in self.dataSet.keys() and max(temp.keys()) in self.dataSet.keys())
                counter = max(counter, 0)
                ans.update(temp)
                page += 1
        self.dataSet.update(ans)
        print("Updated to " + self.grabPageNumber().__str__() + "!...")
        return self.dataSet


if __name__ == "__main__":
    a = ChatBoxGrabber()
    # print(a.getData("http://baker-forum.ir/index.php?action=shoutbox_archive"))
    a.dataSet = pickle.load(open('data.pickle', 'rb'))
    pickle.dump(a.grabNew(), open('data.pickle', 'wb'))
    input("done!")