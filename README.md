MFWFetcher
==============

MFWFetcher fetches users' history data from MaFengwo.
Specifically, this program will fetch users' historical data from MFW, including where did they go,when did they go and how often did user travel.

Usage:
   To use the fetcher, database mafengwo should be established by using tables.sql
   
   1. MFWFetcher needs a user's home page of mafengwo.cn to start fetching. Thus, the url should be palced right at '__main__' part of mafengwo.py like blows:
   if __name__ == '__main__':
    maFengWo = MaFengWo()
    result = maFengWo.startMaFengWo('http://www.mafengwo.cn/u/34917925.html')
    print result
  
   2. The friends' home pages url will be stored in personalUrl table. And to continue fetch data, We need just run 
      MFW_main.py
    
   3. If necessary, we can run procedure 1 several times to store more urls in personalUrl table.
   4. The result will all be in mafengwo database.
