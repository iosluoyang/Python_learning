# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import sys
sys.path.append("/var/www/html/python_projects/publicTools")





# 识别验证码相关的库
from PIL import Image,ImageEnhance
import pytesseract
import requests
import time

import logging #日志记录

import public  #公共方法文件
from config import EmailAddressEnum #配置文件中的邮件地址集合
from selenium import webdriver #打开浏览器文件
from sendEmailTools import SendMailClass #发送邮件文件

import datetime
import json
from datetime import datetime
from  apscheduler.schedulers.blocking import  BlockingScheduler #定时任务


Cookies = "" #全局cookies变量,在获取不到Json数据之后就开始请求新的cookies更新全局变量

#模拟登录获取cookies
def Updatecookies():
    url = "http://as.hda.gov.cn/company_login.jsp" #登录页面地址
    browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
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
    time.sleep(1)

    #页面源码:
    html = browser.page_source
    #print html + "\n\n\n\n\n\n\n"

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
        response = requests.post(url, headers=headers, data=data, proxies=proxies,timeout=60)
        #print "获取到的申报数据信息为:" + response.content
        #将Json数据转换为字典对象
        currentstatusdic = json.loads(response.content)
        print currentstatusdic
        #获取最新的数据情况
        newestdata = currentstatusdic["rows"][0]
        #店名:
        storename = newestdata["comMc"]
        #审核状态:
        shstatus = "未审核" if newestdata["logShjg"] == "0" else "已审核"
        #是否受理
        slstatus = "未受理" if newestdata["sqSlbz"] == "0" else "已受理"

        print storename + "   " + "受理状态为:" + slstatus+ "   " +  "审核状态是:" + shstatus


    except Exception as e:
        print "cookies失效,正在重新获取新的cookies,此次错误原因是:" +  e.message
        #如果发生错误说明cookies失效,重新获取一次cookies然后进行访问
        Updatecookies()
        GetJsonDataWithCookies()


Updatecookies()
GetJsonDataWithCookies()




