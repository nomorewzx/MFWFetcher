#*-* coding: utf-8 *-*
# there are url of user's travel notes which contain information such as user's id, days of traveling, number of people who travels, expenses of travel of everyone
#the date of travel and the type of travel(through angencies or travel personaly) and, of course,  where did the author visit during the tour.
#so, it is greatly useful to fetch information from travel notes.
#http://www.mafengwo.cn/i/912729.html
#http://www.mafengwo.cn/i/1292266.html
#http://www.mafengwo.cn/i/2991875.html
import codecs
import urllib
import urllib2
import re
import MySQLdb
import mafengwo
class TravelNote:
    def __init__(self,urlTravelNotes='http://www.mafengwo.cn/i/2991875.html' ):
        self.urlTravelNote=urlTravelNotes
        self.HtmlTool = mafengwo.HtmlTools()
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
    #GetSpot() fetch the spot from block <p class="txt">.......</p>
    def GetSpot(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<p class="txt">(.*?)</p>'
        reObj = re.compile(s,re.S)
        spots = reObj.findall(unicodePage)
        spot = self.HtmlTool.ReplaceChar(spots[0])
        return spot
    #GetUserNoteInfo() fetch the div block <div class="a_con_text cont"......> which contains userId and dataId(note ID)
    def GetUserNoteInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="a_con_text cont".*?>'
        reObjRaw = re.compile(s,re.S)
        userNoteInfo = reObjRaw.findall(unicodePage)
        return userNoteInfo[0]
    #GetUserId() fetch userId from div block of GetUserNoteInfo()
    def GetUserId(self,userNoteInfo):
        s = r'ownerid="([0-9]{1,})"'
        reObj = re.compile(s,re.S)
        userId = reObj.findall(userNoteInfo)
        return userId[0]
    #GetNoteId() fetch note id from div block of GetUserNoteInfo()
    def GetNoteId(self,userNoteInfo):
        s = r'dataid="([0-9]{1,})"'
        reObj = re.compile(s,re.S)
        noteId = reObj.findall(userNoteInfo)
        return noteId[0]
    #the function GetTripInfo() fetch basic information 
    def GetTripInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="basic-info">(.*?)</div>'
        reObj = re.compile(s,re.S)
        infoBoxes = reObj.findall(unicodePage)
        if 0 == infoBoxes.__len__() :
            print 'this travel note %s does not contains the info box!!' % self.url
            return -1
        return infoBoxes[0]

    def GetDate(self,infoBox):
        s  = r'[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}'
        reObj  = re.compile(s,re.S)
        date = reObj.findall(infoBox)
        return date[0]

    def GetPeople(self,infoBox):
        s = r'<li class="item-people"><i></i>..<span><b>(.*?)</b></span></li>'
        reObj = re.compile(s,re.S)
        people = reObj.findall(infoBox)
        return people

    def GetPeopleAverageCost(self,infoBox):
        s = r'<li class="item-cost">.*?</li>'
        reObjRaw = re.compile(s,re.S)
        rawCost = reObjRaw.findall(infoBox)
        reObj = re.compile(r'[0-9]{1,}')
        peopleAverageCost = reObj.findall(rawCost[0])
        return peopleAverageCost[0]

    def GetTravelDays(self,infoBox):
        s = r'<li class="item-days">.*?</li>'
        reObjRaw = re.compile(s,re.S)
        rawDays = reObjRaw.findall(infoBox)
        reObj = re.compile(r'[0-9]{1,}',re.S)
        travelDays = reObj.findall(rawDays[0])
        return travelDays[0]
    #travel-type and travel-people is for future to fetch


    #GetSpotsInfo() fetch information of spots that traveler had been.
    def GetSpotsInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="keyword-info">(.*?)</div>'
        reObj = re.compile(s,re.S)
        spotsInfo = reObj.findall(unicodePage)
        return spotsInfo[0]
    def startTravelNote(self):
        page = self.GetTravelNote()
        spot = self.GetSpot(page)
        print 'SPOT IS: %s' % spot
        userNoteInfo = self.GetUserNoteInfo(page)
        userId = self.GetUserId(userNoteInfo)
        print "THE USER ID IS %s " % userId
        noteId = self.GetNoteId(userNoteInfo)
        print "THE NOTE ID IS  %s" % noteId
        infoBoxes = self.GetTripInfo(page)
        if infoBoxes == -1 :
            return None
        date = self.GetDate(infoBoxes)
        print date
        peopleACost = self.GetPeopleAverageCost(infoBoxes)
        print peopleACost
        travelDays = self.GetTravelDays(infoBoxes)
        days = int(travelDays)
        print travelDays
        print 'infobox is over!!!!!!'
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd='4364410',db='mafengwo',charset='utf8')
            cur = conn.cursor()
            param = [noteId, userId, date, int(travelDays), float(peopleACost), spot]
            query = "insert into travelNote (nid, uid, travelDate, travelDays,travelCost,spot) values (%s, %s, %s, %s, %s, %s)"
            n = cur.execute(query,param)
            cur.close()
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
__author__ = 'zhenxuan wang'
if __name__ == '__main__':
    print 'start travel_info.py'
    travelNote = TravelNote()
    travelNote.startTravelNote()




