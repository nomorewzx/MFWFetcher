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
def fetchNotes():
    travelNote = travelnote.TravelNote()
    conn = MFWdb.MFWConnect()
    cur = conn.cursor()
    cur.execute('select noteUrl from travelNoteUrl')
    noteUrls = cur.fetchall()
    for noteUrl in noteUrls:
        time.sleep(2)
        print noteUrl[0]
        travelNote.startTravelNote(noteUrl[0])
        #delete travelNoteUrl that has been fetched.
        MFWdb.deleteTravelNoteUrl( noteUrl[0] )
if __name__ == '__main__':
    #fetchUsers()
    fetchNotes()
