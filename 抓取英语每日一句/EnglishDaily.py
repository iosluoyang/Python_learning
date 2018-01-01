# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import os
import sys
import random

sys.path.append("/usr/pythonprojects/publicTools")

import public  #公共方法文件
from selenium import webdriver #打开浏览器文件
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  #伪装模块
#显式等待
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from sendEmailTools import SendMailClass #发送邮件文件

import datetime
from datetime import datetime
from time import sleep

from apscheduler.schedulers.blocking import BlockingScheduler #定时任务


#进行翻译转化过滤
def getTranslateresult(str,tolanguagetype):
    #不是中文的话就需要进行翻译
    if tolanguagetype != "zh":
        return public.TranslateLanguage(str,totype=tolanguagetype)

    else:
        return str
#从网上获取数据并且发送
def sendEnglishDaily(languageArr):

    # 首先获取当前日期
    timestr = datetime.strftime(datetime.now(), '%Y-%m-%d')
    url = "http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/" + timestr

    # 首先将DesiredCapabilities转换为一个字典，方便添加键值对
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 然后添加一个浏览器标识的键值对：
    dcap['phantomjs.page.settings.userAgent'] = (random.choice(public.User_Agent_List))
    browser = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1','--webdriver-loglevel=NONE'])
    #设置加载超时时长
    #browser.set_page_load_timeout(60)
    #browser.set_script_timeout(60)  # 这两种设置都进行才有效

    #尝试获取获取网页数据,增加显示等待
    #使用while循环
    i = 0
    while i < 10:

        try:
            print ('开始今日第'+str(i)+'次抓取网页数据……')
            #browser.implicitly_wait(60)  # 隐式等待，最长等60秒
            browser.get(url)

            sleep(10)  # 强制等待10秒再执行下一步


            # 开始解析数据:

            # 每日一句 en:

            dailyEnglish = browser.find_element_by_css_selector("div.detail-content-en").text

            # 每日一句 zh:
            dailyChinese = browser.find_element_by_css_selector("div.detail-content-zh").text

            # 每日一句 小编寄语:
            dailyDes = browser.find_element_by_css_selector("blockquote.detail-content-desc").text.strip("词霸小编：")

            # 每日一句 图片地址:
            dailyImgUrl = browser.find_element_by_css_selector("img.detail-banner-img").get_attribute("src")

            # 点赞数量
            dailyZanNumber = browser.find_element_by_css_selector("div.detail-content-numbers span.numbers-zan").text


            print ("抓取到的数据为:\n" + dailyEnglish + "\n" + dailyChinese + "\n" + dailyDes + "\n" + dailyImgUrl + "\n" + dailyZanNumber)



            #遍历目标语言数组，针对每一种语言进行翻译或不翻译，然后发送给该语种对应的邮件接收人
            for i,languagedic in enumerate(languageArr):
                print ("开始发送第"+str(i)+"个语言组邮件")

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
                    fromNickname=getTranslateresult("小海哥每日一句", languagetype),
                    emailfooter="--" + getTranslateresult("小海哥每日一句", languagetype)
                )

                print ("第"+str(i)+"个语言组邮件发送完毕,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

            print ("邮件全部发送完毕,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

            print ("发送完成,程序将自动退出")

            break

        except Exception as e:
            if e != KeyboardInterrupt:
                i+=1
                #达到10次的尝试次数之后return掉整个方法
                if i == 10:
                    print ("今日尝试次数已经达到10次,程序将自动退出")
                continue

    print ('程序退出成功,浏览器将自动关闭!')
    # 抓取完数据之后将Phantom浏览器关闭！非常重要,否则会导致程序永远不会停止
    browser.quit()



#配置发送人信息等
def send():

    #从本地csv文件中获取到最新的接收人数组 注意此处要把本地的相对路径转换为Linux上的绝对路径
    ABSPATH = os.path.abspath(sys.argv[0])
    ABSPATH = os.path.dirname(ABSPATH) + "/toUserList.csv"
    toUserlist = public.returndatafromreadcsvfile(ABSPATH)

    languagesArr = []#专门记录语言种类的数组
    toUserlistArr = []#发送人字典的数组
    for User in toUserlist:

        language = User["language"] # 语言种类
        EmailAddress = User["EmailAddress"]#邮件地址
        name = User["name"]#昵称

        #只增加有效的邮件地址:
        if EmailAddress:

            #如果语言数组中没有包含该语言,则创建该语言字典对象
            if language not in languagesArr:
                #构建发送对象
                languagedict = {
                    "tolanguage":language,
                    "toemailaddressArr":[{"nickname":name,"address":EmailAddress}],
                }
                #将发送对象增加到数组中
                toUserlistArr.append(languagedict)
                #将该语言种类增加到语言数组中
                languagesArr.append(language)
            #已经存在该语言,说明发送人数组中已经有该语言种类的字典对象了,这个时候
            #只要找到对应的语言种类将邮件增加到其对象字典的邮件数组中即可
            else:
                for dict in toUserlistArr:
                    if dict["tolanguage"] == language:
                        dict["toemailaddressArr"].append({"nickname":name,"address":EmailAddress})
                        break

    #获取完之后执行抓取和发送的方法
    sendEnglishDaily(toUserlistArr)



# import logging  #记录定时任务的运行情况
#
# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)  # DEBUG
#
# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)


#以下为定时任务的代码
sched = BlockingScheduler()
#通过add_job来添加作业
sched.add_job(send, 'cron', day_of_week="mon-sun", hour=7 , minute=59 , second=50 ,max_instances=100)  # 每天早上7点59分50秒开始运行程序
sched.start()

