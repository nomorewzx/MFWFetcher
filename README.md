MFWFetcher
==============
MFWFetcher fetches public users' history data from MaFengwo.
Specifically, this program will fetch users' historical data from MFW, including where did they go,when did they go and how often did user travel.

Usage:
   To use the fetcher, `mafengwo` should be created by executing tables.sql
   
   1. MFWFetcher needs a user's home page of mafengwo.cn to start fetching. Thus, the url should be placed right at '__main__' part of mafengwo.py like blows:
      if __name__ == '__main__':
         maFengWo = MaFengWo()
         result = maFengWo.startMaFengWo('http://www.mafengwo.cn/u/34917925.html')
         print result
  
   2. The MFWFetcher is designed to crawl user's follwers' data, so once start fetching somebody's homepage, his/her followers' homepage url would be inserted right in table `personalUrl`. 
   3. According to #2, after repeat #1 one or several(if necessary) times, MFW_main.py should be executed without params needed. Note: MFW_main.py dose not crawl data recursively for the limitations of mafengwo.cn that would require identifying codes after many requests in a short time, which makes rescursion useless for MFWFetcher will always be interrupted after some mininutes.
   4. The result will all be in `mafengwo`, users' info is stored in `tourist`, travelnotes' info is stored in `travelNote`.

MFWFetcher
==============
MFWFetcher 用于抓取mafengwo.cn网站的公开用户历史数据，具体包括用户公开的个人信息，用户旅游目的地，旅游日期，旅游花费，日志发表日期等；

使用说明：
    在使用MFWFetcher之前,应创建数据库 `mafengwo`,执行tables.sql即可完成创建
    
    1. MFWFetcher需要用户个人主页地址开始爬取工作.因此需首先编辑 mafengwo.py中的 '__main__' 部分代码,将用户主页地址添加进
该段代码,如下所示:
      if __name__ == '__main__':
         maFengWo = MaFengWo()
         result = maFengWo.startMaFengWo('http://www.mafengwo.cn/u/34917925.html')
         print result
         
    2. MFWFetcher 会爬取用户的粉丝们的数据，因此 爬取一位用户的数据时，他/她的粉丝主页地址将会被插入`personalUrl`表.
    
    3. 根据#2,在执行完#1,或者重复多次#1(如果需要)后,执行 MFW_main.py,执行该程序不需要任何参数。需要注意的是:由于
mafengwo.cn在一个IP地址短时间发出多次请求后会要求填写页面验证码,所以MFW_main.py并没有递归执行——这样做意义不大，因为程
序在执行一段时间后,总会自己停止.
    4. 结果会存储在 `mafengwo`数据库中,用户数据存储在`tourist`表中,旅游日志数据存储在`travelNote`表中。
