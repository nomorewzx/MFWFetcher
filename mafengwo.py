# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import codecs
import MFWdb
import MySQLdb
import MFWurl

from platform import python_version

class HtmlTools:
    BngCharToNoneRex = re.compile(r'(\t|\n| |<a.*?>|<img.*?>)')
    EndCharToNoneRex = re.compile(r'<.*?>')
    BngPartRex = re.compile(r'<p.*?>')
    CharToNewLineRex = re.compile(r'(<br/>|</p>|)<tr>|</?div>')
    CharToNextTabRex = re.compile(r'<td>')
    ReplaceTable = [
        ('&','\"'),
        ]
    def ReplaceChar(self,x):
        x = self.BngCharToNoneRex.sub('',x)
        x = self.EndCharToNoneRex.sub('',x)
        x = self.BngPartRex.sub('\n',x)
        x = self.CharToNextTabRex.sub('\t',x)
        for tab in self.ReplaceTable:
            x = x.replace(tab[0],tab[1])
            return x

class MaFengWo:
    def __init__(self):
        self.HtmlTool = HtmlTools()
    #取得网页
    def GetPages(self,myurl=''):
        myUrl = myurl
        myUrlReq = urllib2.Request(myUrl)
        myUrlReq.add_header('User-Agent','Mozilla/4.0')
        try:
            myResp = urllib2.urlopen(myUrlReq)
            myPage = myResp.read()
            myResp.close()
            print 'Connect Success!'
            return myPage
        except:
            print 'Fail to connect %s' % myUrl
            return 'NoUser'

    #get user's id (included in url)
    def GetUserId(self,myUrl):
        reObj = re.compile(r'([0-9]+)')
        userIds = reObj.findall(myUrl)
        return userIds[0]
    #获取用户名
    def GetUser(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<li.*?class="name">(.*?)</li>')
        users = reObj.findall(unicodePage)
        user = users[0]
        user = self.HtmlTool.ReplaceChar(user)
        return user
    #get user's residence
    def GetCity(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<li.*?class="city">(.*?)</li>',re.S)
        cities = reObj.findall(unicodePage)
        city = self.HtmlTool.ReplaceChar(cities[0])
        return city
    #get user's gender
    def GetGender(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<li.*?class="gender">(.*?)</li>',re.S)
        genders = reObj.findall(unicodePage)
        for gender in genders:
            if gender.find('girl')>1:
                 gender = 'female'
                 return gender
            else:
                gender = 'male'
                return gender 
    #fetch personal urls from fansList and return lists that contains urls.
    #leaving resolving and storing urls to start() function
    def GetPersonalUrl(self,page):
        unicodePage = page.decode('utf-8')
        reObjRaw = re.compile(r'<div class="fansList">(.*?)</div>',re.S)
        lists = reObjRaw.findall(unicodePage)
        reObj = re.compile(r'<span><a href="(.*?)">',re.S)
        personalUrls = reObj.findall(lists[0])
        return personalUrls            
    #fetch travel notes urls and returns lists that contains notes urls. leaving resolving and storing urls to start() funciton
    def GetTravelNoteUrls(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<h2><a href="(.*?)">', re.S)
        noteUrls  = reObj.findall(unicodePage)
        return noteUrls
    #get html code segment whcih contains page number of personal home page.
    def GetPageNumRaw(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<div.*?class="turn_page">(.*?)</div>',re.S)
        try:
            pageNumRaws = reObj.findall(unicodePage)
            return pageNumRaws[0]
        except IndexError, e:
        	print 'No any content'
        	return 'NoContent'

    def GetTotalPageNum(self,pageNumRaw):
        #pageNumRaw中<a></a>的个数n,再加1，即n+1，即为总页数
        reObj = re.compile(r'<a.*?href.*?>(.*?)</a')
        totalPageNums = reObj.findall(pageNumRaw)
        totalPageNum = totalPageNums.__len__()
        totalPageNum+=1
        return totalPageNum


    #get pages urls if there are more than 1 pages
    def GetPageUrl(self,pageNumRaw):
        if pageNumRaw == 'NoContent':
            return 'noTravelNotes'
        n = self.GetTotalPageNum(pageNumRaw)
        if (1==n):
            return -1
        reObj = re.compile(r"""href='(.*?)'  class="ti">""",re.S)
        pageUrls = reObj.findall(pageNumRaw)
        return pageUrls

    def startMaFengWo(self,myPUrl):

        print 'This is startMaFengWo()========='
        page = self.GetPages(myPUrl)
        if page =='NoUser':
        	print 'no this user'
        	n = MFWdb.deletePersonalUrl(myPUrl)
        	return None
        pageRaw = self.GetPageNumRaw(page)
        if pageRaw == 'NoContent':
            print 'unworth fetching!'
            n = MFWdb.deletePersonalUrl(myPUrl)
            return None
        personalUrls = self.GetPersonalUrl(page)
        userId = self.GetUserId(myPUrl)
        print userId
        user = self.GetUser(page)
        print 'user name is %s' % user
        gender = self.GetGender(page)
        city = self.GetCity(page)
        i = MFWdb.insertUrls(personalUrls, 'personalUrl')
        print 'insert  personal urls'
        noteUrls = self.GetTravelNoteUrls(page)
        j = MFWdb.insertUrls(noteUrls,'travelNoteUrl')
        print 'insert travel note urls'

        pageUrls = self.GetPageUrl(pageRaw)
        print pageUrls
        if(pageUrls != -1):
            for pageUrl in pageUrls:
                pageUrl = MFWurl.toAbsUrl(pageUrl,myPUrl)
                print pageUrl
                pageOther = self.GetPages(pageUrl)
                travelNoteOtherPageUrls = self.GetTravelNoteUrls(pageOther)
                n = MFWdb.insertUrls(travelNoteOtherPageUrls, 'travelNoteUrl')
                print 'insert %d travel notes urls' % n

        try:
            conn = MFWdb.MFWConnect()
            cur = conn.cursor()
            cur1 = conn.cursor()
            param = [userId, user, gender,city]
            query = "insert into tourist (uid, uname, gender, residence) values (%s, %s, %s, %s)"
            n = cur.execute(query,param)
            cur.close()
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])



__author__ = 'WangZhenXuan'
if __name__ == '__main__':
    maFengWo = MaFengWo()
    maFengWo.startMaFengWo('http://www.mafengwo.cn/u/5131692.html')