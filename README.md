###MFWFetcher 说明文档
***
MFWFetcher 用于抓取[mafengwo.cn](www.mafengwo.com.cn)网站的公开用户历史数据,具体包括用户公开的个人信息,用户旅游目的地,旅游日期,旅游花费,日志发表日期等;

`MFW_mmain.py`脚本是整个爬虫的入口。有两个函数：`fetchMany`和`fetchSingle`，分别是自动抓取多个用户的信息以及只抓取单个用户的信息。区别在于其开始爬取时种子URL来源不同。
