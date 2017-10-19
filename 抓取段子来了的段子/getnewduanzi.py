# encoding: utf-8

import re
import sys
sys.path.append("..")
from publicTools.public import GetHtmlDataClass
from publicTools.sendEmailTools import SendMailClass

import datetime
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def getnewestduanzi():

    gethtml = GetHtmlDataClass()
    html = gethtml.gethtml('http://www.qiushibaike.com/')

    pattern = re.compile('<div\s*?class="content">.*?<span>(.*?)</span>', re.S)  # 使用点匹配模式 re.S
    match = re.findall(pattern, html)  # 获取段子集合
    totalstr = ""  # 注意在使用str函数的时候不能定义变量名为str
    for i, result in enumerate(match):
        result = re.sub("<br/>", "", result)  # 使用re.sub方法将字符串中的空格替换为空字符串,即删除空格
        numberstr = "<h3 style='color:orange'>" + str(i + 1) + "/" + str(len(match)) + ":  " + "</h3>"
        duanzistr = "<p>" + result.strip() + "</p>"
        result = numberstr + duanzistr
        totalstr += result
        # print(result)

    #每次抓取完之后就直接发送邮件
    sendmail(totalstr)

def sendmail(totalstr):
    datestr = datetime.strftime(datetime.now(), '(%m月/%d日)')

    sendmail = SendMailClass()
    sendmail.sendmail(
                        ["vb9547n@dingtalk.com","891508172@qq.com"],
                        "<h1 style='color: red'>拯救不开心"+datestr+"~~</h1>"+totalstr+"<p style='text-align: right;font-size: 3rem;color: #5db0fd'>——小海哥倾情奉献</p>",
                        emailimgArr=["http://cdn.iciba.com/news/word/big_20171014b.jpg","http://imgsrc.baidu.com/forum/w%3D580/sign=8f5a7c18cacec3fd8b3ea77de689d4b6/d1d5eef81a4c510fefb163ce6959252dd52aa57a.jpg"],
                        emailsubject="拯救不开心"+datestr,
                        fromNickname="全世界充满笑容委员会"
                    )
    print ("邮件已经发送,发送时间:" + datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))




# #以下为定时任务的代码
# sched = BlockingScheduler()
# #通过add_job来添加作业
# sched.add_job(getnewestduanzi, 'interval', minutes=2)   #每隔1分钟发送一次
# #sched.add_job(getnewestduanzi, 'date', run_date='2017-10-17 12:02:00') #在指定的时间，只执行一次
# #sched.add_job(getnewestduanzi, 'cron', day_of_week='1', second='*/5')  #每周二的时候执行，每过5秒钟便执行一次任务
# sched.start()

getnewestduanzi()












