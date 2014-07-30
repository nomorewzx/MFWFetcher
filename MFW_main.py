#-*- coding: utf-8 -*-
import mafengwo
import travelnote
import 	MFWdb

if __name__ == '__main__':
    travelNote = travelnote.TravelNote()
    maFengWo = mafengwo.MaFengWo()
    conn = MFWdb.MFWConnect()
    cur = conn.cursor()
    cur.execute('select noteUrl from travelNoteUrl')
    urls = cur.fetchall()
    for url in urls:
        print url[0]
        #travelNote.startTravelNote(url[0])
    cur.execute('select perUrl from personalUrl')
    urls = cur.fetchall()
    for url in urls:
        maFengWo.startMaFengWo(url[0])