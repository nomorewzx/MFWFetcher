#*-* coding: utf-8 *-*
"""
	This script collects information of tourists who visited the specific scenic spot.
	To accomplish goal above, we need firstly specify the spot url page, from which travelnotes can be parsed.
	Then the script parse the tourist home page url from travel note page.
	At last, the information of the tourist would be collected from tourist home page.
"""
import requests
from pyquery import PyQuery as pq
import csv

PREFIX = "www.mafengwo.cn"

def getPersonalUrls(spotUrl):
	document = requests.get(spotUrl)
	document.encoding = "utf-8"
	d = pq(document.text)
	authors = d(".author")
	personalUrls = []
	for a in range(0,len(authors)):
		personalUrls.append(PREFIX+authors.eq(a)("a").eq(0).attr('href'))
	return personalUrls

def getPersonalNotesUrls(personalUrls):
	personalNotesUrls = []
	for url in personalUrls:
		personalNotesUrls.append(url[:-5]+"/note"+url[-5:])
	return personalNotesUrls

def main(spotUrl):
	personalUrls = getPersonalUrls(spotUrl)
	personalNotesUrls = getPersonalNotesUrls(personalUrls)
	for url in personalNotesUrls:
		print url

if __name__ == '__main__':
	main("http://www.mafengwo.cn/yj/10195/1-0-1.html")