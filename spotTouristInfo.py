#*-* coding: utf-8 *-*
"""
	This script collects information of tourists who visited the specific scenic spot.
	To accomplish goal above, we need firstly specify the spot url page, from which travelnotes can be parsed.
	Then the script parse the tourist home page url from travel note page.
	At last, the information of the tourist would be collected from tourist home page.
"""
import requests
from pyquery import PyQuery as pq
import re
import csv

PREFIX = "http://www.mafengwo.cn"
USER_INFO = {}

def getPersonalUrls(spotUrl):
	document = requests.get(spotUrl)
	document.encoding = "utf-8"
	d = pq(document.text)
	authors = d(".author")
	personalUrls = []
	for a in range(0,len(authors)):
		personalUrls.append(PREFIX+authors.eq(a)("a").eq(0).attr('href'))
	return personalUrls

def getPersonalNotesUrls(spotUrl):
	personalUrls = getPersonalUrls(spotUrl)
	personalNotesUrls = []
	for url in personalUrls:
		personalNotesUrls.append(url[:-5]+"/note"+url[-5:])
	return personalNotesUrls

def getUserId(url):
	match = re.search(r'/u/(.*)/note',url)
	if match:
		return match.group(1)

def getUserResidence(pqPage):
	d = pqPage
	nameAndResidence = d(".MAvaName").text().encode('utf-8')
	try:
		index = nameAndResidence.index('(')
		residence = nameAndResidence[index+1:-1]
		return residence
	except:
		print 'fail to find residence of '+nameAndResidence
		return 'null'

def getNumNotes(pqPage):
	d = pqPage
	numNotes = d(".MAvaNums strong").eq(0).text()
	return numNotes

def getUserInfo(personalNotesUrl):
	userInfo = {}
	document = requests.get(personalNotesUrl)
	document.encoding = "utf-8"
	d = pq(document.text)
	userId = getUserId(personalNotesUrl)
	residence = getUserResidence(d)
	numNotes = getNumNotes(d)
	USER_INFO[userId] = (residence, numNotes)

def getUsers(spotUrl):
	personalNotesUrls = getPersonalNotesUrls(spotUrl)
	for url in personalNotesUrls:
		getUserInfo(url)


def genSpotUrlPages(spotUrl):
	for i in range(1,3):
		url = spotUrl % i
		print "processing page "+url+"................"
		getUsers(url)

def main(spotUrl):
	genSpotUrlPages(spotUrl) 
	

if __name__ == '__main__':
	main("http://www.mafengwo.cn/yj/10195/1-0-%d.html")