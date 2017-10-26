# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import sys
sys.path.append("/var/www/html/python_projects/publicTools")

from config import EmailAddressEnum #配置文件
import public  #公共方法文件
import logging #日志记录
from sendEmailTools import SendMailClass #发送邮件文件

from selenium import webdriver

import datetime
from datetime import datetime
from  apscheduler.schedulers.blocking import  BlockingScheduler


#进行翻译转化过滤
def getTranslateresult(str,tolanguagetype):
    #不是中文的话就需要进行翻译
    if tolanguagetype != "zh":
        return public.TranslateLanguage(str,totype=tolanguagetype)

    else:
        return str

def sendEnglishDaily(languageArr):

    #首先获取当前日期
    timestr = datetime.strftime(datetime.now(), '%Y-%m-%d')
    url = "http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/" + timestr
    browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--ssl-protocol=TLSv1'])
    browser.get(url)

    #每日一句 en:
    dailyEnglish = browser.find_element_by_css_selector("div.detail-content-en").text

    #每日一句 zh:
    dailyChinese = browser.find_element_by_css_selector("div.detail-content-zh").text

    #每日一句 小编寄语:
    dailyDes = browser.find_element_by_css_selector("blockquote.detail-content-desc").text.strip("词霸小编：")

    #每日一句 图片地址:
    dailyImgUrl = browser.find_element_by_css_selector("img.detail-banner-img").get_attribute("src")

    #点赞数量
    dailyZanNumber = browser.find_element_by_css_selector("div.detail-content-numbers span.numbers-zan").text

    print dailyEnglish + "\n" + dailyChinese + "\n" + dailyDes + "\n" + dailyImgUrl + "\n" + dailyZanNumber


    #遍历目标语言数组，针对每一种语言进行翻译或不翻译，然后发送给该语种对应的邮件接收人
    for i,languagedic in enumerate(languageArr):
        #取出当前的语种
        languagetype = languagedic["tolanguage"]
        #该语种下对应的邮件接收人数组
        toemailaddressArr = languagedic["toemailaddressArr"]
        #下面根据具体需求进行翻译检测

        sendmail = SendMailClass()

        # 首先显示图片
        imgstr = "<img src='cid:image0' width=100% alt='"+getTranslateresult("我是一个图片,想要看我请点击信任该发件人哦",languagetype)+"'>"

        # 然后显示英语
        Enstr = "<p style='font-size: 26px;line-height: 34px;margin-top: 20px;font: 14px/1 'Microsoft Yahei',sans-serif,Arial,Verdana;color: #333333'>" + dailyEnglish + "</p>"

        # 然后显示中文
        Chstr = "<p style='font-size: 18px;line-height: 24px;margin-top: 8px;font: 14px/1 'Microsoft Yahei',sans-serif,Arial,Verdana;color: #333333'>" + dailyChinese + "</p>"

        # 然后显示小海哥寄语 + 点赞数量
        XHGDes = "<p style='font-size: 14px;line-height: 24px;margin-top: 16px;font: 14px/1 'Microsoft Yahei',sans-serif,Arial,Verdana;color:darkgray;'>" + "小海哥:   " + getTranslateresult(dailyDes + "(当前已有" + dailyZanNumber + "人点赞)",languagetype) + "</p>"

        totalHtml = imgstr + Enstr + Chstr + XHGDes
        totalimgs = [dailyImgUrl]
        # 获取当前月和日
        datestr = datetime.strftime(datetime.now(), '%m月%d日')
        totalsubject = getTranslateresult("嗨," + datestr + "," + "早上好",languagetype)

        sendmail.sendmail(
            toemailaddressArr,
            totalHtml,
            emailimgArr=totalimgs,
            emailsubject=totalsubject,
            fromNickname=getTranslateresult("小海哥每日一句",languagetype),
            emailfooter="--" + getTranslateresult("小海哥每日一句",languagetype)
        )
        print ("第"+str(i)+"组邮件发送完毕,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

    print ("邮件全部发送完毕,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

#开始发送
def send():
    try:
        sendEnglishDaily(
            [
                {"tolanguage":"en","toemailaddressArr":[EmailAddressEnum.Neung]},
                {"tolanguage": "zh", "toemailaddressArr": [
                    EmailAddressEnum.liuhaiyang1,
                    EmailAddressEnum.liuhaiyang2,
                    EmailAddressEnum.axin,
                    EmailAddressEnum.wenyuan,
                    EmailAddressEnum.junyan,
                    EmailAddressEnum.youyige,
                    EmailAddressEnum.hejun,
                    EmailAddressEnum.yunfei,
                    EmailAddressEnum.gezi,
                    EmailAddressEnum.zhouhuiqiao,
                    EmailAddressEnum.susanjie,
                ]}
            ]
        )
    except BaseException as e:
        # 在这里捕获所有的异常(除了用户手动操作中止以外的错误)
        if e.__class__ != KeyboardInterrupt:
            errmsg = e.message
            # 开始记录日志
            logging.debug(errmsg)
            # 向小海哥发送错误提醒邮件
            public.senderrtoXHG("抓取英语每日一句信息运行模块", errmsg)


#开始执行发送程序加入异常处理和日志记录
#配置日志记录功能
public.recordlogging()

try:
    #以下为定时任务的代码
    sched = BlockingScheduler()
    # 通过add_job来添加作业
    sched.add_job(send, 'cron', day_of_week="mon-sun", hour=9, minute=10)  # 每天早上9点10分自动发送
    sched.start()
except BaseException as e:
    #在这里捕获所有的异常(除了用户手动操作中止以外的错误)
    if e.__class__ != KeyboardInterrupt:

        errmsg = e.message
        # 开始记录日志
        logging.debug(errmsg)
        # 向小海哥发送错误提醒邮件
        public.senderrtoXHG("抓取英语每日一句定时模块", errmsg)
























