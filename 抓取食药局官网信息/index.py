# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import sys
sys.path.append("/var/www/html/python_projects/publicTools")





# 识别验证码相关的库
from PIL import Image,ImageEnhance
import pytesseract
import requests
import time


import public  #公共方法文件
from config import EmailAddressEnum #配置文件中的邮件地址集合
from selenium import webdriver #打开浏览器文件
from sendEmailTools import SendMailClass #发送邮件文件

import datetime
import json
from datetime import datetime
from  apscheduler.schedulers.blocking import  BlockingScheduler #定时任务


Cookies = "" #全局cookies变量,在获取不到Json数据之后就开始请求新的cookies更新全局变量
#设置标识每种状态的邮件只发一次,发送完毕之后就改变全局变量的值导致后续的邮件都不会被发送,等到审核完毕之后直接取消该定时器
ifshouli = False
ifbuyushouli = False
ifweitongguo = False


#模拟登录获取cookies
def Updatecookies():
    url = "http://as.hda.gov.cn/company_login.jsp" #登录页面地址
    browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1','--webdriver-loglevel=ERROR'])
    browser.maximize_window()  # 将浏览器最大化
    browser.get(url)

    #首先获取验证码
    browser.save_screenshot('webscreenshot.png')  # 截取当前整个网页，该网页有我们需要的验证码
    imgelement = browser.find_element_by_css_selector("img#yzmimg") #定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height'])) #根据验证码元素的位置写成我们需要截取的位置坐标
    i = Image.open('webscreenshot.png') #打开整个网页的截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域,即验证码的截图

    #frame4.save('verificationimg.png') #保存验证码的截图
    #time.sleep(3) #防止由于网速，可能图片还没保存好，就开始识别
    #verification_img = Image.open('verificationimg.png')  # 打开保存的验证码截图
    #imgry = verification_img.convert('L')  # 图像加强，二值化

    imgry = frame4.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("verificationimg_final.png")
    time.sleep(1)
    verification_finalimg = Image.open('verificationimg_final.png')
    verificationCode = pytesseract.image_to_string(verification_finalimg).strip()  # 使用image_to_string识别验证码

    print "验证码是:" + verificationCode

    #模拟手动登录
    #用户名:
    elem_user = browser.find_element_by_css_selector('#userName')
    elem_psw = browser.find_element_by_css_selector('#userPwd')
    elem_code = browser.find_element_by_css_selector('#userYzm')
    elem_loginbtn = browser.find_element_by_css_selector('#loginBtn')

    #填表单
    elem_user.send_keys('411282199108151091')#用户名
    elem_psw.send_keys('152640')#密码
    elem_code.send_keys(verificationCode)#验证码

    #点击登录
    elem_loginbtn.click()
    #登录进去之后休眠5秒
    time.sleep(5)



    #获取页面cookies
    cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    print  "获取到的cookies是:" + cookiestr

    browser.quit()

    global Cookies
    Cookies = cookiestr

#获取到cookies之后直接加上cookies访问申报数据的接口得到申报json数据
def GetJsonDataWithCookies():

    #根据全局变量cookies访问Json数据接口,如果能够获取到数据则说明cookies有效，如果获取不到数据则说明cookies失效，重新获取cookies

    url = "http://as.hda.gov.cn/spjy/spjysq_admin.action?tabStr=qyd"
    data = {
        "comMc": "",
        "sqSqbh": "",
        "qsSj": "",
        "fddbr": "",
        "jycs": "",
        "jzSj": "",
        "page": "1",
        "rows": "25",
    }
    # 头部信息:
    headers = {
        "Host": "as.hda.gov.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "54",
        "Cookie": Cookies,
        "Connection": "keep-alive"
    }

    # 设置代理服务器
    proxies = {
        'http:': 'http://121.232.146.184',
        'https:': 'https://144.255.48.197'
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies,timeout=300000)
        print "获取到的申报数据信息为:" + response.content
        #将Json数据转换为字典对象
        currentstatusdic = json.loads(response.content)
        #获取最新的数据情况
        newestdata = currentstatusdic["rows"][0]

        #核对码:
        sqHdm = newestdata["sqHdm"]
        #上报情况 sqSbbz 0未上报  1已上报 其他 上报审核未通过
        sbstatus = newestdata["sqSbbz"]
        #申请名称:
        storename = newestdata["comMc"]
        #申请编号:
        sqnumber = newestdata["sqSqbh"]
        #经营场所:
        storeplace = newestdata["jycs"]
        #申请日期:
        sqtime = newestdata["spjySqsj"]
        #上报时间:
        sbtime = newestdata["sqSbsj"]
        #法定代表人:
        fdpeople = newestdata["fddbr"]

        #审核状态 0未审核  1已审核  其他审核未通过
        shstatus =  newestdata["logShjg"]

        #审核人:
        shpeople = newestdata["logShrxm"]
        #审核时间:
        shtime = newestdata["logShsj"]
        #审核未通过原因:
        shrefusereason = newestdata["logShwtgyy"]
        #预约受理时间:
        yytime = newestdata["sqYysdsj"]
        #是否网络经营
        ifnetwork = newestdata["sfwljy"]

        #是否受理  0未受理  1已受理 2不予受理
        slstatus = newestdata["sqSlbz"]

        #受理编号
        slnumber = newestdata["sqlcSlbh"]
        #受理人
        slpeople = newestdata["sqSlrxm"]
        #受理时间
        sltime = newestdata["sqSlsj"]
        #打回原因
        slrefusereason = newestdata["sqlcDhyy"]
        #打回时间
        slrefusetime = newestdata["sqlcDhsj"]
        #评分
        rate = newestdata["sqPj"]


        toemailAddressArr = ["891508172@qq.com", "1029854245@qq.com"]

        global ifshouli
        global ifbuyushouli
        global ifweitongguo


        #判断逻辑
        #首先判断是否审核通过
        #未审核
        if shstatus == "0":
            #然后判断是否已经受理 0未受理  1已受理 2不予受理
            if slstatus == "0":

                str = "亲,您的 《" + storename + "》 项目还处于未受理的阶段呢,请耐心等待哦。程序会自动帮你查询受理状态,一有消息就通知您"
                print str
                #如果是未受理的阶段,则将记录发送状态的全局变量全部恢复初始值False

                ifshouli = False
                ifbuyushouli = False
                ifweitongguo = False

            elif slstatus == "1":

                str = "亲,有进展了,您的  《" + storename + "》 项目已经有人开始受理了,受理人是:  " + slpeople + " 受理时间: "+sltime + " 受理编号是:" +slnumber + "请耐心等待受理结果,一有消息马上通知您"
                print str
                #如果已经受理记录为False时,则将该值改为True并且发送邮件
                if not ifshouli:
                    # 发送邮件
                    sendmail = SendMailClass()
                    sendmail.sendmail(
                        toemailAddressArr,
                        str,
                        emailsubject="亲, <" + storename + "> 项目已经开始受理",
                        fromNickname="小海哥",
                        emailfooter="--" + "小海哥自动抓取审核状态程序"
                    )

                    print("邮件已发送")
                    ifshouli = True


            elif slstatus == "2":

                str = "亲,很抱歉,您的 《" + storename + "》  项目当前状态为不予受理,打回原因是:  " + slrefusereason + " 打回时间是: " + slrefusetime + " 请务必尽快修改重新提交,小海哥会自动为您检测最新一次的项目审核"
                print str

                if not ifbuyushouli:
                    # 发送邮件
                    sendmail = SendMailClass()
                    sendmail.sendmail(
                        toemailAddressArr,
                        str,
                        emailsubject="亲, <" + storename + "> 项目不予受理",
                        fromNickname="小海哥",
                        emailfooter="--" + "小海哥自动抓取审核状态程序"
                    )

                    print("邮件已发送")
                    ifbuyushouli = True

        #已审核
        elif shstatus == "1":
            #审核通过

            str = "亲,恭喜您的  《" + storename + "》项目已经通过审核啦!"
            print str

            # 发送邮件
            sendmail = SendMailClass()
            sendmail.sendmail(
                toemailAddressArr,
                str,
                emailsubject="亲, <" + storename + "> 项目通过审核啦!",
                fromNickname="小海哥",
                emailfooter="--" + "小海哥自动抓取审核状态程序"
            )
            print "邮件发送成功"

            #审核通过之后直接结束程序
            sys.exit()

        #审核未通过
        else:
            #查看审核未通过的原因
            str = "很抱歉,您的 《"+ storename +"》项目审核未通过,原因是:  " +  shrefusereason + ' 请尽快修改相关信息重新提交审核,小海哥会自动为您检测最新的审核状态'
            print str

            if not ifweitongguo:
                # 发送邮件
                sendmail = SendMailClass()
                sendmail.sendmail(
                    toemailAddressArr,
                    str,
                    emailsubject="亲, <" + storename + "> 项目审核未通过",
                    fromNickname="小海哥",
                    emailfooter="--" + "小海哥自动抓取审核状态程序"
                )

                print("邮件已发送")
                ifweitongguo = True



    except Exception as e:
        print("cookies失效,正在重新获取新的cookies,此次错误原因是:" +  e.message)
        #如果发生错误说明cookies失效,重新获取一次cookies然后进行访问
        begintocheck()


def begintocheck():
    Updatecookies()
    GetJsonDataWithCookies()



#以下为定时任务的代码
# sched = BlockingScheduler()
# #通过add_job来添加作业
# sched.add_job(begintocheck, 'interval', hours=1)  # 每隔一个小时运行一次,如果整个过程抓取完毕之后则直接终止此程序
# sched.start()


begintocheck()



