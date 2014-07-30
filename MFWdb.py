#-*- coding:utf-8 -*-
import MySQLdb
import MFWurl
import re
def MFWConnect():
    conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd='4364410',db='mafengwo',charset='utf8')
    return conn

def insertUrls(urls, table):
    try:
        conn = MFWConnect()
        cur = conn.cursor()
        insertValues = []
        for url in urls:
            reObj = re.compile(r'([0-9]{2,})')
            Id = reObj.findall(url)
            url = MFWurl.toAbsUrl(url)
            insertValues.append([Id[0],url])
        query = "insert into "+table+" values (%s, %s)"
        n = cur.executemany(query, insertValues)
        cur.close()
        conn.commit()
        conn.close()
        return n
    except MySQLdb.Error,e:
        print 'insert to table %s error%d, %s' % (table, e.args[0], e.args[1])
        return -1

def getTravelNoteUrl():
    try:
        conn = MFWConnect()
        cur = conn.cursor()
        query = "select noteUrl from travelNoteUrl"
        n = cur.execute(query)
        print "%d urls is fetched!!!!" % n
        urls = cur.fetchall()
        return 
    except MySQLdb.Error, e:
        print "error occurs when getting urls from table travelNoteUrl %d,%s" % (e.args[0],e.args[1])

if __name__ == '__main__':
    getTravelNoteUrl()
