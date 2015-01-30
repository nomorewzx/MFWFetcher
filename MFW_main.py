#-*- coding: utf-8 -*-
import mafengwo
import travelnote
import 	MFWdb
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