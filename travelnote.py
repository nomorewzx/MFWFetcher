#*-* coding *-*
# there are url of user's travel notes which contain information such as user's id, days of traveling, number of people who travels, expenses of travel of everyone
#the date of travel and the type of travel(through angencies or travel personaly) and, of course,  where did the author visit during the tour.
#so, it is greatly useful to fetch information from travel notes.
import codecs
import urllib
import urllib2
import re

class TravelNote:
    def __init__(self,urlTravelNotes='http://www.mafengwo.cn/i/1292266.html' ):
        self.urlTravelNote=urlTravelNotes
    #get page of urlTravelNote
    def GetTravelNote(self):
        myUrl = self.urlTravelNote
        myUrlReq = urllib2.Request(myUrl)
        myUrlReq.add_header('User-Agent','Mozilla/4.0')
        try:
            myResp = urllib2.urlopen(myUrlReq)
            myPage = myResp.read()
            myResp.close()
            return myPage
        except:
            print 'fail to connect %s' % myUrl
            return None
    #the function GetTripInfo() fetch basic information 
    def GetTripInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="basic-info">(.*?)</div>'
        reObj = re.compile(s,re.S)
        infoBoxes = reObj.findall(unicodePage)
        return infoBoxes
    def GetSpotsInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="keyword-info">(.*?)</div>'
        reObj = re.compile(s,re.S)
        spotsInfo = reObj.findall(unicodePage)
        return spotsInfo
    def startTravelNote(self):
        page = self.GetTravelNote()
        print 'page is fetched!!!!'
        infoBoxes = self.GetTripInfo(page)
        for infoBox in infoBoxes:
            print 'infobox is:'
            print infoBox
        print 'infobox is over!!!!!!'
        spotsInfo = self.GetSpotsInfo(page)
        for spotInfo in spotsInfo:
            print 'spots is:'
            print spotInfo

__author__ = 'zhenxuan wang'
if __name__ == '__main__':
    print 'start travel_info.py'
    travelNote = TravelNote()
    travelNote.startTravelNote()




