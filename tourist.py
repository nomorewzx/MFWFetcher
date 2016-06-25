#-*- coding: utf-8 -*-
# 该脚本以蚂蜂窝旅行网中的用户为中心进行数据抓取。抓取的步骤如下：
# 1. 指定一个用户主页URL；
# 2. 抓取该用户关注的其它用户URL，并放入mafengwo数据库的personalURL表中；
# 3. 抓取该用户基本信息，存入mafengwo数据库的tourist表中；
# 4. 抓取用户所发表的所有游记信息，并将信息放入travelnote表中，该步骤使用travelnote.py完成
import MySQLdb
import requests
from pyquery import PyQuery as pq
import MFWdb
import geocode
import re
import travelnote

PREFIX = "http://www.mafengwo.cn"

# 根据用户URL抓取页面
def getUserPage(userUrl):
	try:
		document = requests.get(userUrl)
		document.encoding = 'utf-8'
		d = pq(document.text)
		return d
	except requests.ConnectionError, e:
		print 'requests %s error %d, %s' % (userUrl,e.args[0],e.args[1])

# 抓取用户基本信息，包括id,name,gender,residence以及residence的经纬度(lon,lat)
def getBasicInfo(userUrl):
	page = getUserPage(userUrl)
	uid = getUserID(userUrl)
	name = getName(page)
	gender = getGender(page)
	residence,lon,lat = getResidence(page)
	return (uid,name,gender,residence,lon,lat)

# 从用户主页URL中提取uid
def getUserID(userUrl):
	match = re.search(r'/u/(.*)\.html',userUrl)
	if match:
		return match.group(1)

def getName(page):
	return page(".MAvaName").text()

def getGender(page):
	if page(".MGenderFemale").length>0:
		return 'female'
	if page(".MGenderMale").length>0:
		return 'male'

def getResidence(page):
	residence = page(".MAvaPlace").attr('title')
	if residence != None:
		latlon = LatlonResidence(residence)
		return residence,latlon[0],latlon[1]
	else:
		return '',0,0

# 将用户居住地转化为经纬度值并返回（经度，纬度）
def LatlonResidence(residence):
	geoCodeDict = geocode.genGeoCodeDict()
	for k,v in geoCodeDict.items():
		if k.decode('utf-8') in residence:
			return v
		elif residence in k.decode('utf-8'):
			return v
	return (0,0)

# 获取用户主页中的最近访问用户列表
def getFollowingList(userUrl):
	foList= []
	listOfRecentViewers = []
	d = getUserPage(userUrl)
	liList = d("#_j_followcnt ul li p a")
	liCount = liList.length
	for i in range(0,liCount):
		foList.append(PREFIX+liList.eq(i).attr("href"))
	return foList

def fetchUserAndNotes(url):
	# 1.获取用户基本信息basic并插入tourist表
	basicInfo = getBasicInfo(url)
	MFWdb.insertUserBasicInfo(basicInfo)

	# 2.获取用户关注列表中其它用户的url，并插入personalUrl表
	foList = getFollowingList(url)
	MFWdb.insertUserUrlList(foList)

	# 3.从personalUrl表中，删除已抓取过的用户url
	MFWdb.deleteUserUrl(url)

	# 4.获取用户的游记url列表，并抓取游记信息，存入travelnote表中
	noteUrlList = travelnote.getNoteUrlList(url)
	for noteUrl in noteUrlList:
		noteInfo = travelnote.fetchTravelNote(noteUrl)
		# 将uid插入noteInfo中，得到(nid,uid,travelDate,travelDays,travelCost,spot,lon,lat)
		noteInfo.insert(1,basicInfo[0])
		MFWdb.insertTravelNoteInfo(noteInfo)

def main():
	url = u"http://www.mafengwo.cn/u/11003586.html"
	fetchUserAndNotes(url)

if __name__ == '__main__':
	main()