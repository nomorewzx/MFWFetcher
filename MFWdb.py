#-*- coding:utf-8 -*-
import MySQLdb

def MFWConnect():
    conn = MySQLdb.connect(host = 'localhost',user = 'root',passwd='4364410',db='mafengwo',charset='utf8')
    return conn