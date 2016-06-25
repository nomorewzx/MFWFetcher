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

def getUserUrlPairValue(userUrl):
    uid = getUserID(userUrl)
    value = (uid,userUrl)
    return value

def insertUserUrlList(userUrlList):
    try:
        conn = MFWConnect()
        cur = conn.cursor()
        insertValues = []
        for url in userUrlList:
            value = getUserUrlPairValue(url)
            insertValues.append(value)
        query = "insert into personalUrl values (%s, %s)"
        n = cur.executemany(query, insertValues)
        conn.commit()
        print 'insert %d url into personalUrl table' % len(userUrlList)
        return n
    except MySQLdb.Error,e:
        print 'insert to personalUrl error%d, %s' % (e.args[0], e.args[1])
        return -1
    finally:
        cur.close()
        conn.close()

# delete user's url.
def deleteUserUrl(url):
    try:
        conn  = MFWConnect()
        cur = conn.cursor()
        value = getUserUrlPairValue(url)
        query = 'delete from personalUrl where uid= %s'
        param = (value[0])
        cur.execute(query,param)
        conn.commit()
        print "delete "+url+"..."
        return True
    except MySQLdb.Error, e:
        print 'error occurs when delete meaningless personal url %d,%s' % (e.args[0],e.args[1])
    finally:
        cur.close()
        conn.close()

def insertUserBasicInfo(basicInfoList):
    try:
        conn = MFWConnect()
        cur = conn.cursor()
        query = "insert into tourist values (%s,%s,%s,%s,%s,%s)"
        cur.execute(query, basicInfoList)
        conn.commit()
        print 'insert %s into tourist table' % basicInfoList[1]
    except MySQLdb.Error,e:
        print 'insert into tourist table error %d, %s' % (e.args[0], e.args[1])
        return -1
    finally:
        cur.close()
        conn.close()
if __name__ == '__main__':
    print "......"
