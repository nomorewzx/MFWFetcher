#-*- coding: utf-8 -*-
# 该文件用于批量递归地执行数据抓取操作。步骤为：
# 1. 从personalURL表中，抽取一个用户URL作为种子URL开始抓取操作。
# 2. 删除该URL；
# 3. 执行1.
import tourist
import travelnote
import MFWdb
import time
import requests

# 循环抓取多用户
def fetchMany():
    conn = MFWdb.MFWConnect()
    cur = conn.cursor()
    cur.execute('select perUrl from personalUrl')
    personalUrls = cur.fetchall()
    for personalUrl in personalUrls:
        #sleep for 2 seconds.
        time.sleep(2)
        try:
            print personalUrl
            tourist.fetchUserAndNotes(personalUrl[0])
        except requests.ConnectionError,e:
            print 'error occurs in requests' %(personalUrl)
    cur.close()
    conn.close()

# 抓取单用户
def fetchSingleUser():
    userUrl = "http://www.mafengwo.cn/u/11003586.html"
    tourist.fetchUserAndNotes(userUrl)

if __name__ == '__main__':
        fetchSingleUser()
