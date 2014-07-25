# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import codecs
import MySQLdb
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
    def __init__(self,urlPara="http://www.mafengwo.cn/u/347077.html",pagePara=1,):
        self.page = pagePara
        self.pages = []
        self.url = "http://www.mafengwo.cn/u/347077.html"
        self.HtmlTool = HtmlTools()
        #从字符串中提取数字
    def GetNums(self,uniString):
    #得到的参数为unicode编码
        NumString = filter(unicode.isdigit,uniString)
        return NumString
        #取得网页
    def GetPages(self):
        myUrl = self.url
        myUrlReq = urllib2.Request(myUrl)
        myUrlReq.add_header('User-Agent','Mozilla/4.0')
        try:
            myResp = urllib2.urlopen(myUrlReq)
            myPage = myResp.read()
            myResp.close()
            print 'Connect Success!'
            return myPage
        except:
            print 'Fail to connect %s' % self.url
            return None
     #获取文章标题
    def GetTitles(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<h2>(.*?)</h2>')
        titles = reObj.findall(unicodePage)
        return titles
    #获取文章中目的地
    def GetSenicSpot(self,page):
        unicodePage = page.decode('utf-8')
        s = r'<a.*href="/travel-scenic-spot/.*>(.*?)</a></span>'
        reObj = re.compile(r'travel-scenic-spot(.*?)</a></span>',re.S)
        senicSpots = reObj.findall(unicodePage)
        return senicSpots
    #get user's id (included in url)
    def GetUserId(self):
        reObj = re.compile(r'[0-9]+')
        userIds = reObj.findall(self.url)
        return userIds[0]
    #获取用户名
    def GetUser(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<li.*?class="name">(.*?)</li>')
        users = reObj.findall(unicodePage)
        user = users[0]
        user = self.HtmlTool.ReplaceChar(user)
        return user

    def GetCity(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<li.*?class="city">(.*?)</li>',re.S)
        cities = reObj.findall(unicodePage)
        city = self.HtmlTool.ReplaceChar(cities[0])
        return city

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

    def GetPageNumRaw(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<div.*?class="turn_page">(.*?)</div>',re.S)
        pageNumRaws = reObj.findall(unicodePage)
        for pageNumRaw in pageNumRaws:
            return pageNumRaw

    def GetCurrentPageNum(self,pageNumRaw):
        reObj = re.compile(r'this-page(.*?)</span>',re.S)
        currentPageNums = reObj.findall(pageNumRaw)
        for currentPageNum in currentPageNums:
            currentPageNum = self.GetNums(currentPageNum)
            return currentPageNum

    def GetTotalPageNum(self,pageNumRaw):
        #pageNumRaw中<a></a>的个数n,再加1，即n+1，即为总页数
        reObj = re.compile(r'<a.*?href.*?>(.*?)</a')
        totalPageNums = reObj.findall(pageNumRaw)
        totalPageNum = totalPageNums.__len__()
        totalPageNum+=1
        return totalPageNum

    def GetPageUrl(self,pageNumRaw):
        print 'nothing'
        return 'nothing'

    def startMaFengWo(self):

        f=codecs.open("user","a","utf-8")
        print 'This is startMaFengWo()========='
        page = self.GetPages()
        pageRaw = self.GetPageNumRaw(page)
        print '=============current page==========='
        currentPageNum = self.GetCurrentPageNum(pageRaw)
        print '%s' % currentPageNum
        print'==============number of total page===='
        totalPageNum = self.GetTotalPageNum(pageRaw)
        print '%s' % totalPageNum
        print '==============the user==============='
        user = self.GetUser(page)
        print '%s' % user
        print '==============user id==============='
        userId=self.GetUserId()
        print userId
        print '=============the gender============='
        gender = self.GetGender(page)
        print '%s' % gender
        print '=============the city================'
        city = self.GetCity(page)
        print '%s' % city
        print '==============the title==============='
        titles = self.GetTitles(page)
        for title in titles:
            title = self.HtmlTool.ReplaceChar(title)
            print '%s' % title
        print '==============senic spots=============='
        senicSpots = self.GetSenicSpot(page)
        print 'the length of senicSpots is %d' % senicSpots.__len__()
        for senicSpot in senicSpots:
            senicSpot = self.HtmlTool.ReplaceChar(senicSpot)
            print '%s' % senicSpot
        spot = senicSpots[0]
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd='4364410',db='mafengwo',charset='utf8')
            cur = conn.cursor()
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
    maFengWo.startMaFengWo()