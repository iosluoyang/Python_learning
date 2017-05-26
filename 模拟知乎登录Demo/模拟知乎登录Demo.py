# encoding: utf-8

import  requests
from bs4 import BeautifulSoup
import os, time
import re

#构造代理IP
proxies = {
  "http": "183.78.183.252:8081"
}

# 构造 Request headers
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}

homeurl = "https://www.zhihu.com/"
#构造用于网络请求的session
session = requests.session()
# 获取xsrf_token(登录时需要用的一个参数)
homeresponse = session.get(homeurl,headers = headers,proxies = proxies)

#使用bs4进行解析
homesoup = BeautifulSoup(homeresponse.text,'html.parser')
#找到xsrf元素element
xsrfinput = homesoup.find('input',{'name':'_xsrf'})
xsrf_token = xsrfinput['value']
print('获取到的登录参数xsrf_token的值为:' , xsrf_token)

#获取验证码 验证码图片中的一些参数是当前时间戳的转化(因为第一次获取验证码没有什么用，在后面重新获取之后再将其增加进提交数据当中)
# randomtime = str(int(time.time() * 1000))
# captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + randomtime+"&type=login"
# captcharesponse = session.get(url=captchaurl,headers = headers,proxies = proxies)
# with open('checkcode.gif','wb') as f:
#     f.write(captcharesponse.content)
#     f.close()
#
# captcha = input('请输入验证码:')
# print('验证码是:',captcha)

#开始登录
headers['X-Xsrftoken'] = xsrf_token
headers['X-Requested-With'] = 'XMLHttpRequest'
loginurl = 'https://www.zhihu.com/login/email'
postdata = {
    '_xsrf':xsrf_token,
    'email':'891508172@qq.com',
    'password':'wyhhsh1993'
}
loginresponse = session.post(url=loginurl,headers = headers,data=postdata)
print('第一次服务器端返回响应码:',loginresponse.status_code)
print('第一次获取到的json数据为:',loginresponse.json())
# 验证码问题输入导致失败: 猜测这个问题是由于session中对于验证码的请求过期导致
if loginresponse.json()['r'] ==1 :
    #重新输入验证码,再次运行代码则正常。也就是说可以在第一次不输入验证码，或者输入错的验证码，只有第二次才是有效的
    randomtime = str(int(time.time() * 1000))
    captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + \
                 randomtime + "&type=login"
    captcharesponse = session.get(url=captchaurl, headers=headers)
    with open('checkcode.gif', 'wb') as f:
        f.write(captcharesponse.content)
        f.close()
    captcha = input('请再次输入验证码：')
    print('第二次获取到的验证码是:',captcha)

#重新提交一次
    postdata['captcha'] = captcha
    loginresponse = session.post(url=loginurl, headers=headers, data=postdata)
    print('第二次服务器端返回响应码：', loginresponse.status_code)
    print('第二次获取的返回json数据为:',loginresponse.json())

#保存登录后的cookie信息
#首先判断是否登录成功
profileurl = 'https://www.zhihu.com/settings/profile'
profileresponse = session.get(url=profileurl,headers = headers)
print('profile页面响应码为:',profileresponse.status_code)
profilesoup = BeautifulSoup(profileresponse.text,'html.parser')
div = profilesoup.find('div',{'id':'rename-section'})
print(div)











