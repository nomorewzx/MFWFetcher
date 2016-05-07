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
	if not d(".MAvaNums strong").eq(0):
		print 'fail to find the user url.......QUIT...'
		exit()

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

def writeToCSV(infoDict,url):
	writerRows = []
	for k,v in infoDict.items():
		row = (k,v[0],v[1])
		writerRows.append(row)

	filename = re.search(r'\d{2,}',url).group()
	with open(filename+'.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		for row in writerRows:
			writer.writerow(row)


def getUsers(spotUrl):
	personalNotesUrls = getPersonalNotesUrls(spotUrl)
	for url in personalNotesUrls:
		getUserInfo(url)
	writeToCSV(USER_INFO,spotUrl)



def genSpotUrlPages(spotUrl,startPage,endPage=10):
	if startPage > endPage:
		print 'Page number wrong, pelase check.......'
		exit()
	for i in range(startPage,endPage+1):
		url = spotUrl % i
		print "processing page "+url+"................"
		getUsers(url)

def main(spotUrl,startPage,endPage):
	genSpotUrlPages(spotUrl,startPage,endPage) 
	

if __name__ == '__main__':
	main("http://www.mafengwo.cn/yj/10195/1-0-%d.html",1,1)