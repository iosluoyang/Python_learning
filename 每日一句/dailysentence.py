# encoding: utf-8

from pyquery import PyQuery as pq
import sys
sys.path.append("..")
from publicTools.sendEmailTools import SendMailClass

import datetime
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

sendcount = 1 #发送次数,从1开始
currentindex = 0 #在当前页选择的帖子的索引
lasttotalpage = 0
def getnewestzhiliti():

    pagehtml = pq('http://tieba.baidu.com/p/3433462927?see_lz=1')
    #首先获取总页码 获取li.l_reply_num中第二个span里的内容
    totalpage = pagehtml("li.l_reply_num")('span').eq(1).text()
    # 当前需要抓取的页码起始页 总页码数 - 上一次记录的总页码数
    global  lasttotalpage
    currentpage = str(int(totalpage) - int(lasttotalpage))


    url = "http://tieba.baidu.com/p/3433462927?see_lz=1&pn=" + currentpage
    html = pq(url)
    #注意，由于百度贴吧的限制，在同步请求时，只能获取到p_content中的内容，即发布的帖子内容，不能获取到core_reply即帖子的发布时间和回复等信息
    contentitems = html("div.d_post_content").items()  # 获取该页所有的帖子内容集合
    totalitems = [];

    for contentitem in contentitems:

        stritem = str(contentitem.text().decode('utf-8')) if contentitem.text() else ""
        imgitem = contentitem("img").attr('src') if contentitem("img").attr('src')  else ""  # python的三目和其他语言不同


        # 将文本和图片组合为字典对象存入数组中
        itemdic = {"content": stritem, "img": imgitem}
        # 将获取到的数据存储到数组中，并且声明为全局变量
        totalitems.append(itemdic)


    #将帖子数组倒叙排列，即最老的在最前面
    totalitems = totalitems[::-1]
    global  currentindex
    #取当前的第currentindex个帖子,如果这个时候currentindex等于该帖子集合的总数-1，说明本次已经是取当前页的最后一个帖子，这个时候应该取完之后将上次页码+1 ，将当前索引置为0
    #先取出来当前的帖子
    tiezidic = totalitems[currentindex]
    #每取完一次，将currentindex的值增加1
    currentindex += 1

    #然后进行判断
    if currentindex == len(totalitems) - 1:

        lasttotalpage+=1
        currentindex = 0

    tiezicontent = tiezidic["content"]
    tieziimg = tiezidic["img"]
    #tieziimgs = [] if tieziimg=="" else [tieziimg] #注意,此处发送百度贴吧的图片链接会有问题，其他链接图片就没有问题，此问题待之后解决
    tieziimgs = []
    #网页背景图片
    bodybgimg = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1508411212578&di=56baf79e5fb6b7f6645e2c25ab3dd92e&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F3b292df5e0fe9925a0ce2f4e3ea85edf8cb171e9.jpg"



    print "当前是第%s页,第%s个帖子,帖子内容为:%s,帖子图片为:%s" %(currentpage ,currentindex, tiezicontent,tieziimg)



    #发送邮件
    datestr = datetime.strftime(datetime.now(), '此刻是%Y年%m月%d日的%H:%M:%S')
    global  sendcount

    sendmail = SendMailClass()

    sendmail.sendmail(
        ["3029068348@qq.com"],
        "<h4 style='color: orange;font-weight: 100'>嗨,我亲爱的你," + datestr +
        ",这是小海哥第"+"<span style='color: black'>"+str(sendcount)+"</span>"+"次和你见面" "</h4>" +
        "<h3 style='color: black;font-weight: 100'>"+tiezicontent+"</h3>",
        emailimgArr=tieziimgs,
        emailsubject="早上好啊,有句话想对你说",
        fromNickname="小海哥每日一句",
        emailfooter="——小海哥每日一句",
        #emailbodybgimg=bodybgimg

    )
    print ("邮件已经发送,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    sendcount += 1 #发送次数增加1




# #以下为定时任务的代码
sched = BlockingScheduler()
#通过add_job来添加作业
sched.add_job(getnewestzhiliti, 'cron', day_of_week='mon-fri',hour=9,minute=30,end_date='2017-12-31')  #每周的周一至周五早上9:30的时候执行
sched.start()



