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
import MFWdb
class TravelNote:
    def __init__(self):
        self.HtmlTool = mafengwo.HtmlTools()
    #get page of urlTravelNote
    def GetTravelNote(self,myNoteUrl=''):
        myUrl = myNoteUrl
        myUrlReq = urllib2.Request(myUrl)
        myUrlReq.add_header('User-Agent','Mozilla/4.0')
        try:
            myResp = urllib2.urlopen(myUrlReq)
            myPage = myResp.read()
            myResp.close()
            return myPage
        except:
            print 'fail to connect %s' % myUrl
            MFWdb.deleteTravelNoteUrl(myUrl)
            return None
    #GetSpot() fetch the spot from block <p class="txt">.......</p>
    def GetSpot(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<p class="txt">(.*?)</p>'
        reObj = re.compile(s,re.S)
        try:
            spots = reObj.findall(unicodePage)
            spot = self.HtmlTool.ReplaceChar(spots[0])
            return spot
        except IndexError,e:
            print 'no spot found!'
            return 'NoSpot'
    #GetUserNoteInfo() fetch the div block <div class="a_con_text cont"......> which contains userId and dataId(note ID)
    def GetUserNoteInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="a_con_text cont".*?>'
        reObjRaw = re.compile(s,re.S)
        try:
            userNoteInfo = reObjRaw.findall(unicodePage)
            return userNoteInfo[0]
        except IndexError,e:
        	print 'no userInfo found'
        	return 'NoUserInfo'
    #GetUserId() fetch userId from div block of GetUserNoteInfo()
    def GetUserId(self,userNoteInfo):
        if userNoteInfo == 'NoUserInfo':
        	return 'No UserId'
        s = r'ownerid="([0-9]{1,})"'
        reObj = re.compile(s,re.S)
        userId = reObj.findall(userNoteInfo)
        return userId[0]
    #GetNoteId() fetch note id from div block of GetUserNoteInfo()
    def GetNoteId(self,userNoteInfo):
        if userNoteInfo == 'NoUserInfo':
            return 'No UserId'
        s = r'dataid="([0-9]{1,})"'
        reObj = re.compile(s,re.S)
        noteId = reObj.findall(userNoteInfo)
        return noteId[0]
    #get time of note published by users. 
    def GetNoteDate(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<span class="date">(.*?)</span>'
        reObj = re.compile(s,re.S)
        try:
            noteTime = reObj.findall(unicodePage)
            print noteTime[0]
            s1  = r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'
            reObjDate = re.compile(s1,re.S)
            dates = reObjDate.findall(noteTime[0])
            print dates[0]
            return dates[0] 
        except IndexError, e:
            print 'no note published date found!'
            return 'NoNoteDate'

    #the function GetTripInfo() fetch basic information 
    def GetTripInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="basic-info">(.*?)</div>'
        reObj = re.compile(s,re.S)
        try:
            infoBoxes = reObj.findall(unicodePage)
            return infoBoxes[0]
        except IndexError,e:
            return 'NoInfoBox'

    def GetDate(self,infoBox):
        if infoBox == 'NoInfoBox':
            return 'NoDateFound'
        s  = r'[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}'
        try:
            reObj  = re.compile(s,re.S)
            date = reObj.findall(infoBox)
            return date[0]
        except IndexError,e:
            print 'NoTravelDateFound'
            return 'NoTravelDateFound'

    def GetPeople(self,infoBox):
        if infoBox == 'NoInfoBox':
            return 'NoDateFound'
        s = r'<li class="item-people"><i></i>..<span><b>(.*?)</b></span></li>'
        try:
            reObj = re.compile(s,re.S)
            people = reObj.findall(infoBox)
            return people
        except IndexError, e:
            return 'No people found'

    def GetPeopleAverageCost(self,infoBox):
        if infoBox == 'NoInfoBox':
            return 'NoCostFound'
        s = r'<li class="item-cost">.*?</li>'
        reObjRaw = re.compile(s,re.S)
        rawCost = reObjRaw.findall(infoBox)
        reObj = re.compile(r'[0-9]{1,}')
        try:
            peopleAverageCost = reObj.findall(rawCost[0])
            return peopleAverageCost[0]
        except IndexError, e:
            return "NoCostFound"

    def GetTravelDays(self,infoBox):
        if infoBox == 'NoInfoBox':
            return 'NoDateFound'
        s = r'<li class="item-days">.*?</li>'
        reObjRaw = re.compile(s,re.S)
        rawDays = reObjRaw.findall(infoBox)
        reObj = re.compile(r'[0-9]{1,}',re.S)
        try:
            travelDays = reObj.findall(rawDays[0])
            return travelDays[0]
        except IndexError,e:
            return 'NoTravelDaysFound'
    #travel-type and travel-people is for future to fetch


    #GetSpotsInfo() fetch information of spots that traveler had been.
    def GetSpotsInfo(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<div class="keyword-info">(.*?)</div>'
        reObj = re.compile(s,re.S)
        spotsInfo = reObj.findall(unicodePage)
        return spotsInfo[0]

    def startTravelNote(self,myNoteUrl=''):
        page = self.GetTravelNote(myNoteUrl)
        spot = self.GetSpot(page)
        noteDate = self.GetNoteDate(page)
        print 'Note Date is %s' % noteDate
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
        print travelDays
        print 'infobox is over!!!!!!'
        try:
            conn = MFWdb.MFWConnect()
            cur = conn.cursor()
            param = [noteId, userId, date, travelDays, peopleACost, spot, noteDate]
            query = "insert into travelNote (nid, uid, travelDate, travelDays,travelCost,spot,noteDate) values (%s, %s, %s, %s, %s, %s,%s)"
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
    travelNote.startTravelNote('http://www.mafengwo.cn/i/504381.html')




