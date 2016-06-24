#-*- coding: utf-8 -*-
# 该脚本以蚂蜂窝旅行网中的用户为中心进行数据抓取。抓取的步骤如下：
# 1. 指定一个用户主页URL；
# 2. 抓取最近访问用户主页的其它用户URL，并放入mafengwo数据库的personalURL表中；
# 3. 抓取该用户基本信息，存入mafengwo数据库的tourist表中；
# 4. 抓取用户所发表的所有游记信息，并将信息放入travelnote表中，该步骤使用travelnote.py完成
import MySQLdb
import requests
from pyquery import PyQuery as pq
import MFWdb
import geocode
import re

PREFIX = "http://www.mafengwo.cn"

# 根据用户URL抓取页面
def getUserPage(userUrl):
	document = requests.get(userUrl)
	document.encoding = 'utf-8'
	d = pq(document.text)
	return d

# 抓取用户基本信息，包括id,name,gender,residence以及residence的经纬度(lon,lat)
def getBasicInfo(userUrl):
	page = getUserPage(userUrl)
	uid = getID(userUrl)
	name = getName(page)
	gender = getGender(page)
	residence,lon,lat = getResidence(page)
	return (uid,name,gender,residence,lon,lat)

# 从用户主页URL中提取uid
def getID(userUrl):
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
	if residence != '':
		latlon = LatlonResidence(residence)
		if len(latlon) == 2:
			return residence,latlon[0],latlon[1]
		else:
			return residence,0,0

# 将用户居住地转化为经纬度值并返回（经度，纬度）
def LatlonResidence(residence):
	geoCodeDict = geocode.genGeoCodeDict()
	for k,v in geoCodeDict.items():
		if k.decode('utf-8') in residence:
			return v
		elif residence in k.decode('utf-8'):
			return v

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

def main():
	basicInfo = getBasicInfo("http://www.mafengwo.cn/u/nopa13.html")
	print basicInfo
	print getFollowingList("http://www.mafengwo.cn/u/nopa13.html")

if __name__ == '__main__':
	main()