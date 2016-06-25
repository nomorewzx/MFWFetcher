#-*- coding:utf-8 -*-
"""
	该脚本抓取一个游记页面，并将游记基本信息存入mafengwo数据库中的travelnote表中。
"""
import MySQLdb
import requests
from pyquery import PyQuery as pq
import MFWdb
import geocode
import re
import tourist

PREFIX = "http://www.mafengwo.cn"

def getNotePage(noteUrl):
	document = requests.get(noteUrl)
	document.encoding = 'utf-8'
	d = pq(document.text)
	return d

def getNoteID(noteUrl):
	match = re.search(r'/i/(.*)\.html',noteUrl)
	if match:
		return match.group(1)

def getUserID(page):
	print '.'
	print page(".person").length
	# userID = tourist.getUserID(userUrl)
	# return userID

# 获取旅行开始日期
def getTravelDate(page):
	date = page(".time").text()
	if date != '':
		match = re.search(r'\d{4}-\d{2}-\d{2}',date)
		if match:
			return match.group(0)
	else:
		return '0000-00-00'

# 获取旅行天数
def getTravelDays(page):
	day = page(".day").text()
	if day != '':
		match = re.search(r'\d{1,2}',day)
		if match:
			return match.group(0)
	else:
		return 0

# 获取人均消费
def getTravelPersonalCost(page):
	cost = page(".cost").text()
	if cost != '':
		match = re.search(r'\d{1,}',cost)
		if match:
			return match.group(0)
	else:
		return 0

def LatlonSpot(spot):
	geoCodeDict = geocode.genGeoCodeDict()
	for k,v in geoCodeDict.items():
		if k.decode('utf-8') in spot:
			return v
		elif spot in k.decode('utf-8'):
			return v
	return (0,0)


# 获取目的地
def getSpot(page):
	spot = page(".relation_mdd a").text()
	if spot != '':
		latlon = LatlonSpot(spot)
		return spot, latlon[0], latlon[1]
	else:
		return 'NoSpot',0,0

def getNoteInfo(noteUrl):
	page = getNotePage(noteUrl)
	nid = getNoteID(noteUrl)
	travelDate = getTravelDate(page)
	travelDays = getTravelDays(page)
	travelPersonalCost = getTravelPersonalCost(page)
	spot,lon,lat = getSpot(page)
	return [nid,travelDate,travelDays,travelPersonalCost,spot,lon,lat]

def getNoteUrlList(userUrl):
	noteList = []
	userNoteUrl = userUrl[:-5]+"/note"+userUrl[-5:]
	document = requests.get(userNoteUrl)
	document.encoding = 'utf-8'
	d = pq(document.text)
	notes = d(".notes_list li")
	for i in range(0,len(notes)):
		noteUrl = notes.eq(i)("a").attr('href')
		noteList.append(PREFIX+noteUrl)
	return noteList

def fetchTravelNote(noteUrl):
	noteInfo = getNoteInfo(noteUrl)
	return noteInfo

def main():
	noteUrl = "http://www.mafengwo.cn/i/5491437.html"
	# noteUrlWithourInformation = "http://www.mafengwo.cn/i/3194957.html"
	# fetchTravelNote(noteUrl)
	noteInfo = getNoteInfo(noteUrl)
	print noteInfo
if __name__ == '__main__':
	main()