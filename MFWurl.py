# -*- coding: utf-8 -*-
#Firstly, the file resolve urls from personal home page, transforming relative urls into absolute urls and storing urls into file personalPageUrls.txt
#Second, the file resolve travel notes urls, same as personal home page urls, program transforms relative urls into absolute urls and store them in 
#     travelNoteUrl.txt.
#When resolve personal home page urls, noticing that users who use pp48.gif as their head portraits is much likely wirting few notes, which is not
#helpful, so this program will not resolve those users' home page urls and, of course, not store the urls.
import codecs
import re
import urllib
import urllib2

# resolve relative url as absolute url
def toAbsUrl(relativeUrl):
    return "http://www.mafengwo.cn"+relativeUrl