#coding=utf-8
import re
import time
from wxpy import *
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler


#z摘要网址获取
def get_url(url):
    r = requests.get(url)
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text, "html.parser")
    t=soup.find_all("script")[2].string
    #pattern=re.compile("[a-zA-z]+://[^\s]*")
    url_list=re.findall("[讯].*\s.*\s.*[a-zA-z]+://[^\s]*",t)[0]
    url_title=re.findall("[a-zA-z]+://[^\s]*",url_list)[0][:-1]
    return url_title

#摘要内容提取函数
def get_title(url_title):
    r = requests.get(url_title)
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text, "html.parser")
    title=soup.find("div",class_="TRS_Editor").get_text()
    return title
#发送新闻
def send_news():
   #my_friend=bot.friends().search("")
    my_group = bot.groups().search("狗崽子又装逼了！")[0]
    url = "http://china.cnr.cn"
    url_title=get_url(url)
    news=get_title(url_title)
    my_group.send(news)
#每日定时发送
def my_scheduler():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(send_news, 'date', run_date="2018-07-16 21:36:00")
    scheduler.add_job(send_news,"cron",hour=7,minute=30)
    scheduler.start()

if __name__=="__main__":
    bot = Bot()
    my_scheduler()
    embed()


