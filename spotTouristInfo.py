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

def a_print(a):
	print a

def main(spotUrl):
	document = requests.get(spotUrl)
	document.encoding = "utf-8"
	d = pq(document.text)
	aElements = d(".tn-wrapper .hasxjicon a")
	for i in range(len(aElements)):
		print aElements.eq(i).attr('href')

if __name__ == '__main__':
	main("http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10195.html")