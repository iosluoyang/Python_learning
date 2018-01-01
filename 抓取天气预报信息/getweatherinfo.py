# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import os
import sys
import random
sys.path.append("/usr/pythonprojects/publicTools")

from config import EmailAddressEnum #配置文件
import public  #公共方法文件
from selenium import webdriver  #打开浏览器文件
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  #伪装模块

#显式等待
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from sendEmailTools import SendMailClass #发送邮件文件


import datetime
from datetime import datetime
import time
from time import sleep

from  apscheduler.schedulers.blocking import  BlockingScheduler

#进行翻译转化过滤
def getTranslateresult(str,tolanguagetype):
    #不是中文的话就需要进行翻译
    if tolanguagetype != "zh":
        return public.TranslateLanguage(str,totype=tolanguagetype)

    else:
        return str

#参数定义，传进来的参数为一个数组和一个日期索引，数组中每一个元素为一个城市字典，字典包含城市的代码/名称以及对应要发送的邮件接受者地址数组
#执行函数时，循环每一个城市字典，发送完毕之后再次循环下一个城市字典
#日期索引dayindex代表的是发送今天的还是明天的还是后几天的天气,0代表今天的天气情况，数值为0~6，默认为明天的天气情况,即dayindex = 1
def getweatherinfomsg(CityArr,dayindex=1):
    #循环每一个城市，给该城市下对应的邮件接收者发送对应日期的天气预报
    for cityindex, citydic in enumerate(CityArr):
        #城市编码/名称
        city = citydic["city"]
        #tolanguage 目标语言类型
        tolanguagetype = citydic["tolanguage"] #需要转化的目标语言类型
        #该城市对应的邮件接收者数组
        toemailaddressArr = citydic["toemailaddressArr"]

        # 因为米胖的接口设计，如果是一线城市的话可以直接输入城市全程的拼音作为拼接参数进行接口请求，如果是其他城市则进行城市编码拼接请求
        # 所以此处做一个判断，如果传过来的参数带有数字，则说明是城市编码，这时完整链接为 https://weather.mipang.com/tianqi- + 城市编码
        # 如果参数内不含数字，则完整链接为 https://weather.mipang.com/ + 城市全称拼音
        url = "https://weather.mipang.com/tianqi-" + str(city) if public.hasNumbers(
            str(city)) else "https://weather.mipang.com/" + str(city)

        # 首先将DesiredCapabilities转换为一个字典，方便添加键值对
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 然后添加一个浏览器标识的键值对：
        dcap['phantomjs.page.settings.userAgent'] = (random.choice(public.User_Agent_List))
        # 因为是js加载的，所以使用phantomjs来加载  注意此处需要增加这两个参数,否则有些网站获取不到网页源码！！！

        browser = webdriver.PhantomJS(desired_capabilities=dcap,
                                      service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1',
                                                    '--webdriver-loglevel=NONE'])
        # 使用while循环
        i = 0
        while i < 10:
            try:
                print ('开始今日第' + str(i) + '次抓取网页数据……')
                #browser.implicitly_wait(60)  # 隐式等待，最长等60秒
                print "开始抓取网页的时间为:" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                browser.get(url)

                sleep(10)  # 强制等待10秒再执行下一步



                # 开始解析数据:
                print "开始解析数据的时间为:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


                # 城市名称+天气两个字:
                cwrname = browser.find_element_by_css_selector(".page-title").text
                # 一周的天气信息
                weatherinfos = browser.find_elements_by_css_selector(".box1 div.item")
                # 天气概况
                weathersimpledes = browser.find_element_by_css_selector("div.sidebar div.br1 div.row1").text
                # 明天的穿衣建议
                dresssuggest = browser.find_element_by_css_selector(".box1 div.chuanyi").text  # 穿衣建议 只有明天才有穿衣建议

                # 数组中元素按照顺序解释为从今天到往后的7天内的天气信息
                AweekWeatherInfoArr = []
                for weatherinfo in weatherinfos:
                    # 每一个天气信息中包含6个div,分别代表日期 温度 天气图标 天气描述 风的来向 风级
                    # 日期(包含week和day)
                    week = weatherinfo.find_element_by_css_selector("div.t1 div.week").text  # eg: 今天 明天 星期一 星期二 ……
                    date = weatherinfo.find_element_by_css_selector("div.t1 div.day").text  # eg: 10月21日

                    # 温度:
                    lowtemp = weatherinfo.find_element_by_css_selector("div.t2 span.temp1").text  # eg: 20
                    hightemp = weatherinfo.find_element_by_css_selector("div.t2 span.temp2").text  # eg: 28℃

                    # 天气图标
                    weathericonUrl = weatherinfo.find_element_by_css_selector("div.t3 img").get_attribute("src")
                    # eg: https://tq-s.malmam.com/images/icon/256/02.png

                    # 天气描述
                    weatherdes = weatherinfo.find_element_by_css_selector("div.t4").text  # eg: 阴转小雨

                    # 风向图标
                    windiconUrl = weatherinfo.find_element_by_css_selector("div.t5 img").get_attribute("src")
                    # eg: https://tq-s.malmam.com/images/direct/3.png

                    # 风向及级别描述
                    winddes = weatherinfo.find_element_by_css_selector("div.t6").text  # eg: 东南风3级

                    weatherdic = {
                        "week": week,  # eg:今天 明天 星期一 星期二 ……
                        "date": date,  # eg:10月21日
                        "lowtemp": lowtemp,  # eg:20
                        "hightemp": hightemp,  # eg:28℃
                        "weathericonUrl": weathericonUrl,  # eg:https://tq-s.malmam.com/images/icon/256/02.png
                        "weatherdes": weatherdes,  # eg:阴转小雨
                        "windiconUrl": windiconUrl,  # eg:https://tq-s.malmam.com/images/direct/3.png
                        "winddes": winddes  # eg:东南风
                    }

                    # 加入到数组中
                    AweekWeatherInfoArr.append(weatherdic)

                # 取出相应日期对应的天气情况 0~6代表从今天开始的往后7天
                # 取数组中第一个天气字典，代表的是今天的天气
                # 取数组中第二个天气字典，代表的是明天的天气 ……以此类推
                weatherinfodic = AweekWeatherInfoArr[int(dayindex)]

                # 发送指定日期的天气情况
                week = weatherinfodic["week"]  # eg:今天 明天 星期一 星期二 ……
                date = weatherinfodic["date"]  # eg:10月21日
                lowtemp = weatherinfodic["lowtemp"]  # eg:20
                hightemp = weatherinfodic["hightemp"]  # eg:28℃
                weathericonUrl = weatherinfodic["weathericonUrl"]  # eg:https://tq-s.malmam.com/images/icon/256/02.png
                weatherdes = weatherinfodic["weatherdes"]  # eg:阴转小雨
                windiconUrl = weatherinfodic["windiconUrl"]  # eg:https://tq-s.malmam.com/images/direct/3.png
                winddes = weatherinfodic["winddes"]  # eg:东南风3级

                print("抓取第" + str(cityindex) + "个城市的天气信息成功:" + cwrname + week + " " + date + " " + lowtemp + " " + hightemp + " "+ weathericonUrl + " " + weatherdes + " " + windiconUrl + " " + winddes + " ")



                # 发送邮件
                sendmail = SendMailClass()

                # 根据参数tolanguage来判断是否需要进行翻译,如果需要进行翻译则规定目标文本类型

                # 小海哥问候语
                timestr = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
                content1 = "<h4 style='color: orange;font-weight: 100'>" + getTranslateresult(
                    "嗨,我亲爱的你,此刻是 " + ":" + " ", tolanguagetype) + timestr + "</h4>"

                # 城市天气名字字样
                cityweathername = cwrname.strip("天气")  # 北京
                content2 = "<span style='color: black;font-size:2rem'>" + getTranslateresult(cityweathername,
                                                                                             tolanguagetype) + " " + "</span>"
                # 日期称呼
                datename = week if dayindex != 2 else "后天"  # 设置日期称呼，暂时设置为第一二三天称呼为今天 明天 后天 其他的称呼为星期几
                content3 = getTranslateresult(datename + "是" + date + ",", tolanguagetype) + "  "
                # 温度显示
                content4 = getTranslateresult("温度为:",
                                              tolanguagetype) + "<span style='color: orange;font-weight: 200;font-size=x-large'>" + lowtemp + "~" + hightemp + "</span>" + "  "
                # 天气描述
                content5 = getTranslateresult(weatherdes,
                                              tolanguagetype) + "<img src='cid:image0' width:30px height=30px>" + "  "
                # 风向描述
                content6 = getTranslateresult(winddes, tolanguagetype) + "<img src='cid:image1'>" + "  "
                # 穿衣建议
                content7 = "<span style='color: orange;font-weight: 200'>" + getTranslateresult(dresssuggest,
                                                                                                tolanguagetype) + "</span>"

                # 关于极端温度的提示  此处设置为最低温度低于-8℃时提醒温度较低，最高温度高于35℃时提醒气温过高
                content8 = ""
                lowtempint = float(lowtemp)
                hightempint = float(hightemp.strip("℃"))
                if lowtempint < -8:
                    content8 = "<span style='color: #1C3B6E;font-weight: 200'>" + "————" + getTranslateresult(
                        "天气虽冷,我心火热", tolanguagetype) + "</span>"
                if hightempint > 35:
                    content8 = "<span style='color: #FA331C;font-weight: 200'>" + "————" + getTranslateresult(
                        "天气虽热,我心似冰", tolanguagetype) + "</span>"

                # 天气简述:(单独成段落展示)
                content9 = "<p style='color:darkgray;font-weight: 100;font-size:small'>" + getTranslateresult(
                    weathersimpledes + "(如文中图片未正常显示,请信任该发件人)", tolanguagetype) + "--" + getTranslateresult(
                    "时刻运行,只为守护你的每一度", tolanguagetype) + "</p>"

                totalhtml = content1 + content2 + content3 + content4 + content5 + content6 + content7 + content8 + content9
                totalimgs = [weathericonUrl, windiconUrl]
                totalsubject = getTranslateresult("嗨," + week,
                                                  tolanguagetype) + " " + lowtemp + "~" + hightemp + " " + getTranslateresult(
                    dresssuggest, tolanguagetype)

                sendmail.sendmail(
                    toemailaddressArr,
                    totalhtml,
                    emailimgArr=totalimgs,
                    emailsubject=totalsubject,
                    fromNickname=getTranslateresult("小海哥天气管家", tolanguagetype),
                    emailfooter="——" + getTranslateresult("小海哥天气管家", tolanguagetype),
                    # emailbodybgimg=bodybgimg

                )
                # 每发送成功一组就进行一次日志记录
                print("第" + str(cityindex) + "组城市天气邮件已经发送,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
                #成功之后结束退出本次循环
                print ('第'+str(cityindex)+'组城市程序运行完毕')
                break
            except Exception as e:
                if e != KeyboardInterrupt:
                    i += 1
                    # 达到10次的尝试次数之后return掉整个方法
                    if i == 10:
                        print ("该城市今日尝试次数已经达到10次,将结束该城市的程序运行")
                    continue

        print ('第'+str(cityindex)+'个城市程序运行完毕,将自动关闭浏览器!')
        # 抓取完数据之后将Phantom浏览器关闭！非常重要,否则会导致程序永远不会停止
        browser.quit()

    print("所有城市天气邮件已经发送完毕,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))


#发送明天的天气预报
def sendthetomorrowinfo():

    #从本地csv文件中获取到最新的接收人数组 注意此处要把本地的相对路径转换为Linux上的绝对路径
    ABSPATH = os.path.abspath(sys.argv[0])
    ABSPATH = os.path.dirname(ABSPATH) + "/toUserList.csv"
    toUserlist = public.returndatafromreadcsvfile(ABSPATH)

    toUserlistArr = []#发送人字典数组
    for User in toUserlist:
        city = User["city"] #城市名称或者编码
        cityremarkname = User['cityremarkname']#城市昵称
        language = User["language"] #该城市的接收人的语言种类
        EmailAddressStr = User["EmailAddressStr"] #邮件地址(多个以逗号分隔)
        EmailArr = EmailAddressStr.split("-") #同一个城市的接收人邮件地址数组
        toEmailArr = [] #将单纯的邮件地址数组转换为带有昵称和邮件地址的对象字典数组,以便于正确显示收件人信息
        for emailaddress in EmailArr:
            dict = {"nickname":"那个在"+cityremarkname+"的你","address":emailaddress}
            toEmailArr.append(dict)


        #只增加有效的城市名称或者id
        if city:
            # 构建发送对象
            citydict = {
                           "city": city,
                           "tolanguage": language,
                           "toemailaddressArr": toEmailArr
                       }
            #将城市字典对象加入到数组中
            toUserlistArr.append(citydict)

#开始发送天气预报


    getweatherinfomsg(
        toUserlistArr,
        dayindex=1
    )  # 发送明天的天气预报



import logging  #记录定时任务的运行情况

# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)  # DEBUG
#
# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)

# 以下为定时任务的代码
sched = BlockingScheduler()
# 通过add_job来添加作业
sched.add_job(sendthetomorrowinfo, 'cron', day_of_week="mon-sun", hour=17, minute=49,second=50,max_instances=100)  # 每天下午17:49:50自动发送
sched.start()

