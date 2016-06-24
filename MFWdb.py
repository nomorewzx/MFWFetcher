#-*- coding:utf-8 -*-
import MySQLdb
import MFWurl
import re

def getUserID(userUrl):
    match = re.search(r'/u/(.*)\.html',userUrl)
    if match:
        return match.group(1)

def MFWConnect():
    conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd='12345678',db='mafengwo',charset='utf8')
    return conn

def getInsertValue(userUrl):
    uid = getUserID(userUrl)
    return value = (uid,userUrl)

def insertUserUrlList(userUrlList):
    try:
        conn = MFWConnect()
        cur = conn.cursor()
        insertValues = []
        for url in userUrlList:
            value = getInsertValue(url)
            insertValues.append(value)
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

# delete meaningless personla urls.
def deletePersonalUrl(url):
    try:
        conn  = MFWConnect()
        cur = conn.cursor()
        reObj = re.compile(r'([0-9]{2,})')
        Id = reObj.findall(url)
        query = 'delete from personalUrl where uid= %s'
        param = (Id[0])
        cur.execute(query,param)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error, e:
        print 'error occurs when delete meaningless personal url %d,%s' % (e.args[0],e.args[1])

def deleteTravelNoteUrl(url):
    try:
        conn = MFWConnect()
        cur = conn.cursor()
        reObj = re.compile(r'([0-9]{2,})')
        Id = reObj.findall(url)
        query = 'delete from travelNoteUrl where nid = %s'
        param = Id[0]
        cur.execute(query,param)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error, e:
        print 'error occurs when delete note url that has been fetched %d,%s ' % (e.args[0],e.args[1])
if __name__ == '__main__':
    getTravelNoteUrl()
