#-*- coding: utf-8 -*-
# 该文件用于批量递归地执行数据抓取操作。步骤为：
# 1. 从personalURL表中，抽取一个用户URL作为种子URL开始抓取操作。
# 2. 删除该URL；
# 3. 执行1.
import mafengwo
import travelnote
import MFWdb
import time

def fetchUsers():
    maFengWo = mafengwo.MaFengWo()
    conn = MFWdb.MFWConnect()
    cur = conn.cursor()
    cur.execute('select perUrl from personalUrl')
    personalUrls = cur.fetchall()
    for personalUrl in personalUrls:
        #sleep for 2 seconds.
        time.sleep(2)
        maFengWo.startMaFengWo(personalUrl[0])
        MFWdb.deletePersonalUrl(personalUrl[0])
    cur.close()
    conn.close()
if __name__ == '__main__':
        fetchUsers()
