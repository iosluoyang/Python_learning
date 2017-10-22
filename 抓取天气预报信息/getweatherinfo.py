#encoding: utf-8
# import sys
# sys.path.append("..")
from public import hasNumbers
from public import TranslateLanguage
from sendEmailTools import SendMailClass

from selenium import webdriver


import datetime
from datetime import datetime
from  apscheduler.schedulers.blocking import  BlockingScheduler

#参数定义，传进来的参数为一个数组和一个日期索引，数组中每一个元素为一个城市字典，字典包含城市的代码/名称以及对应要发送的邮件接受者地址数组
#执行函数时，循环每一个城市字典，发送完毕之后再次循环下一个城市字典
#日期索引dayindex代表的是发送今天的还是明天的还是后几天的天气,0代表今天的天气情况，数值为0~6，默认为明天的天气情况,即dayindex = 1
def getweatherinfomsg(CityArr,dayindex=1):
    #循环每一个城市，给该城市下对应的邮件接收者发送对应日期的天气预报
    for citydic in CityArr:
        #城市编码/名称
        city = citydic["city"]
        #tolanguage 目标语言类型
        tolanguagetype = citydic["tolanguage"] #需要转化的目标语言类型
        #该城市对应的邮件接收者数组
        toemailaddressArr = citydic["toemailaddressArr"]

        # 因为米胖的接口设计，如果是一线城市的话可以直接输入城市全程的拼音作为拼接参数进行接口请求，如果是其他城市则进行城市编码拼接请求
        # 所以此处做一个判断，如果传过来的参数带有数字，则说明是城市编码，这时完整链接为 https://weather.mipang.com/tianqi- + 城市编码
        # 如果参数内不含数字，则完整链接为 https://weather.mipang.com/ + 城市全称拼音
        url = "https://weather.mipang.com/tianqi-" + str(city) if hasNumbers(
            str(city)) else "https://weather.mipang.com/" + str(city)
        # 因为是js加载的，所以使用phantomjs来加载
        browser = webdriver.PhantomJS()
        browser.get(url)
        # 城市名称+天气两个字:
        cwrname = browser.find_element_by_css_selector(".page-title").text
        # 一周的天气信息
        weatherinfos = browser.find_elements_by_css_selector(".box1 div.item")
        # 明天的穿衣建议
        dresssuggest = browser.find_element_by_css_selector(".box1 div.chuanyi").text  # 穿衣建议 只有明天才有穿衣建议

        # 数组中元素按照顺序解释为从今天到往后的7天内的天气信息
        AweekWeatherInfoArr = []
        for weatherinfo in weatherinfos:
            # 每一个天气信息中包含6个div,分别代表日期 温度 天气图标 天气描述 风的来向 风级
            # 日期(包含week和day)
            week = weatherinfo.find_element_by_css_selector("div.t1 div.week").text #eg: 今天 明天 星期一 星期二 ……
            date = weatherinfo.find_element_by_css_selector("div.t1 div.day").text  #eg: 10月21日

            # 温度:
            lowtemp = weatherinfo.find_element_by_css_selector("div.t2 span.temp1").text #eg: 20
            hightemp = weatherinfo.find_element_by_css_selector("div.t2 span.temp2").text #eg: 28℃

            # 天气图标
            weathericonUrl = weatherinfo.find_element_by_css_selector("div.t3 img").get_attribute("src")
            #eg: https://tq-s.malmam.com/images/icon/256/02.png

            # 天气描述
            weatherdes = weatherinfo.find_element_by_css_selector("div.t4").text #eg: 阴转小雨

            # 风向图标
            windiconUrl = weatherinfo.find_element_by_css_selector("div.t5 img").get_attribute("src")
            #eg: https://tq-s.malmam.com/images/direct/3.png

            # 风向及级别描述
            winddes = weatherinfo.find_element_by_css_selector("div.t6").text  #eg: 东南风3级

            weatherdic = {
                "week": week,                       #eg:今天 明天 星期一 星期二 ……
                "date": date,                       #eg:10月21日
                "lowtemp":lowtemp,                  #eg:20
                "hightemp": hightemp,               #eg:28℃
                "weathericonUrl":weathericonUrl,    #eg:https://tq-s.malmam.com/images/icon/256/02.png
                "weatherdes":weatherdes,            #eg:阴转小雨
                "windiconUrl":windiconUrl,          #eg:https://tq-s.malmam.com/images/direct/3.png
                "winddes":winddes                   #eg:东南风
            }

            #加入到数组中
            AweekWeatherInfoArr.append(weatherdic)

        #取出相应日期对应的天气情况 0~6代表从今天开始的往后7天
        #取数组中第一个天气字典，代表的是今天的天气
        #取数组中第二个天气字典，代表的是明天的天气 ……以此类推
        weatherinfodic = AweekWeatherInfoArr[int(dayindex)]

        #发送指定日期的天气情况
        week = weatherinfodic["week"]  # eg:今天 明天 星期一 星期二 ……
        date = weatherinfodic["date"]  # eg:10月21日
        lowtemp = weatherinfodic["lowtemp"]  # eg:20
        hightemp = weatherinfodic["hightemp"]  # eg:28℃
        weathericonUrl = weatherinfodic["weathericonUrl"]  # eg:https://tq-s.malmam.com/images/icon/256/02.png
        weatherdes = weatherinfodic["weatherdes"]  # eg:阴转小雨
        windiconUrl = weatherinfodic["windiconUrl"]  # eg:https://tq-s.malmam.com/images/direct/3.png
        winddes = weatherinfodic["winddes"]  # eg:东南风3级

        #发送邮件
        sendmail = SendMailClass()

        #根据参数tolanguage来判断是否需要进行翻译,如果需要进行翻译则规定目标文本类型


        # 小海哥问候语
        timestr = datetime.strftime("此刻是") + datetime.now(), '%Y/%m/%d. %H:%M:%S'
        content1 = "<h4 style='color: orange;font-weight: 100'>" +getTranslateresult("嗨,我亲爱的你," + timestr + ":",tolanguagetype) + "</h4>"

        # 城市天气名字字样
        cityweathername = cwrname.strip("天气")  # 北京
        content2 = "<span style='color: black;font-size:2rem'>" + getTranslateresult(cityweathername,tolanguagetype) + "</span>"
        # 日期称呼
        datename = week if dayindex != 2 else "后天"  # 设置日期称呼，暂时设置为第一二三天称呼为今天 明天 后天 其他的称呼为星期几
        content3 = getTranslateresult(datename + "是" + date +  ",",tolanguagetype)
        # 温度显示
        content4 = getTranslateresult("温度为:",tolanguagetype) + "<span style='color: orange;font-weight: 200;font-size=x-large'>" + lowtemp + "~" + hightemp + "</span>" + ","
        # 天气描述
        content5 = getTranslateresult(weatherdes,tolanguagetype) + "<img src='cid:image0' width:30px height=30px>"
        # 风向描述
        content6 = getTranslateresult(winddes,tolanguagetype) + "<img src='cid:image1'>"
        # 穿衣建议
        content7 = "<h3 style='color: orange;font-weight: 250'>" + getTranslateresult(dresssuggest,tolanguagetype) + "</h3>"
        # 低温高温提醒
        content8 = ""

        # 关于温度和穿衣建议的提示  此处设置为最低温度低于10℃时提醒温度较低，最高温度高于32℃时提醒气温过高
        lowtempint = float(lowtemp)
        hightempint = float(hightemp.strip("℃"))
        if lowtempint < 10:
            content8 = "<h4 style='color: #1C3B6E;font-weight: 200'>" + getTranslateresult("小海哥都觉得冷了,亲也要注意保暖御寒哦~~",tolanguagetype) + "</h4>"
        if hightempint > 32:
            content8 = "<h4 style='color: #FA331C;font-weight: 200'>" + getTranslateresult("小海哥都热疯了,亲也要注意防暑哦~~",tolanguagetype) + "</h4>"

        content9 = "<p><h4 style='color: darkgray;font-weight: 100;font-size:small'>"+getTranslateresult("小海哥每分每秒每行代码的运行,只是为了提醒你,照顾好自己。"
                                                                                                         "该程序现为测试阶段,如果正文中图片显示不出来,请点击信任该发件人即可,不信你试试(傲娇脸~~)。"
                                                                                                         "如有打扰,请回复本邮件'你为什么这么帅'退订",tolanguagetype)+"</h4></p>"

        totalhtml = content1 + content2 + content3 + content4 + content5 + content6 + content7 + content8 + content9
        totalimgs = [weathericonUrl, windiconUrl]
        totalsubject = getTranslateresult("嗨," + week + lowtemp + "~" + hightemp + "——" + dresssuggest,tolanguagetype)

        # #小海哥问候语
        # timestr = datetime.strftime(datetime.now(), '此刻是%Y年%m月%d日的%H:%M:%S')
        # content1 = "<h4 style='color: orange;font-weight: 100'>"+ "嗨,我亲爱的你," + timestr + ",小海哥炫酷无敌地提示您:" + "</h4>"
        #
        # #城市天气名字字样
        # cityweathername = cwrname.strip("天气") # 北京
        # content2 = "<span style='color: #5db0fd;font-size:2rem'>"+cityweathername+"</span>"
        #
        # #日期称呼
        # datename = week if dayindex !=2 else "后天" #设置日期称呼，暂时设置为第一二三天称呼为今天 明天 后天 其他的称呼为星期几
        # content3 = datename + "是" + "<span style='color: orange;font-weight: 100'>" + date + "</span>" + ","
        #
        # #温度显示
        # content4 = "温度为:" + "<span style='color: #5db0fd;font-weight: 200;font-size=large'>" + lowtemp + "~" + hightemp + "</span>" + ","
        #
        # #天气描述
        # content5 = weatherdes + "<img src='cid:image0' width:30px height=30px>" + ","
        #
        # #风向描述
        # content6 = winddes + "<img src='cid:image1'>"
        #
        # #穿衣建议
        # content7 = "<h3 style='color: darkorange;font-weight: 250'>" + dresssuggest + "</h3>"
        #
        # #低温高温提醒
        # content8 = ""
        #
        # #关于温度和穿衣建议的提示  此处设置为最低温度低于10℃时提醒温度较低，最高温度高于32℃时提醒气温过高
        # lowtempint = float(lowtemp)
        # hightempint = float(hightemp.strip("℃"))
        # if lowtempint < 10:
        #     content8 = "<h4 style='color: #1C3B6E;font-weight: 200'>" +"小海哥都觉得冷了,亲也要注意保暖御寒哦~~"+"</h4>"
        # if hightempint > 32:
        #     content8 = "<h4 style='color: #FA331C;font-weight: 200'>" +"小海哥都热疯了,亲也要注意防暑哦~~"+"</h4>"
        #
        # content9 = "<p><h4 style='color: darkgray;font-weight: 100;font-size:small'>小海哥每分每秒每行代码的运行,只是为了提醒你,照顾好自己。"+\
        #            "该程序现为测试阶段,如果正文中图片显示不出来,请点击信任该发件人即可,不信你试试(傲娇脸~~)。如有打扰,请回复本邮件'你为什么这么帅'退订</h4></p>"
        #
        # totalhtml = content1 + content2 + content3 + content4 + content5 + content6 + content7 + content8 + content9
        # totalimgs = [weathericonUrl,windiconUrl]
        # totalsubject = "嗨,你还好吗？" +week + lowtemp + "~" + hightemp + "——" + dresssuggest


        sendmail.sendmail(
            toemailaddressArr,
            totalhtml,
            emailimgArr=totalimgs,
            emailsubject=totalsubject,
            fromNickname=getTranslateresult("小海哥天气管家",tolanguagetype),
            emailfooter="——" + getTranslateresult("小海哥天气管家",tolanguagetype),
            # emailbodybgimg=bodybgimg

        )
        print ("邮件已经发送,发送时间:" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

#进行翻译转化过滤
def getTranslateresult(str,tolanguagetype):
    #不是中文的话就需要进行翻译
    if tolanguagetype != "zh":
        return TranslateLanguage(str,totype=tolanguagetype)

    else:
        return str


def sendthetomorrowinfo():
    getweatherinfomsg([
        {"city": "beijing", "tolanguage": "zh",
         "toemailaddressArr": ["891508172@qq.com", "48527544@qq.com", "670125193@qq.com",
                               "3282309044@qq.com", "952999576@qq.com", "2542863509@qq.com",
                               "982639828@qq.com", "1778714848@qq.com"]},
        {"city": "2311", "tolanguage": "zh", "toemailaddressArr": ["1558639281@qq.com"]},  # 周慧巧
        {"city": "52707", "tolanguage": "en", "toemailaddressArr": ["capt.titanic@yandex.com"]},  # Neung
        {"city": "xiamen", "tolanguage": "zh", "toemailaddressArr": ["435031804@qq.com"]}  # 厦门susan姐
    ], dayindex=1)  # 发送明天的天气预报


#以下为定时任务的代码
sched = BlockingScheduler()
#通过add_job来添加作业
sched.add_job(sendthetomorrowinfo, 'cron', day_of_week='mon-sun',hour=17,minute=50)  #每天下午17：50自动发送
sched.start()