# -*- coding:UTF-8 -*-
# encoding: utf-8
import httplib
import urllib2
import hashlib  #用于MD5签名获取
import json     #用于json数据解析
import re
import random
import time
import threading
import telnetlib #用来测试代理IP地址是否有效
import logging #日志模块
import sendEmailTools #发送邮件模块



#全局宏
#User_Agent数组
User_Agent_List = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
#IP文件存储的路径       注意此处因为其他文件引用了该文件，所以如果使用相对路径会有问题，改为绝对路径
IPListFilePath = "/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/publicTools/IPListFile.txt"

#获取网页数据类 (包含随机IP地址 User_Agent等信息)
class GetHtmlDataClass:


    #初始化方法
    def __init__(self):
        self.user_agent_list = User_Agent_List
        self.IPListArr = []

        #没有必要每次运行程序都抓取最新的IP地址，这个IP地址的文件手动来控制，如果内容为空时即自动抓取

        f = open(IPListFilePath,'r')
        contents = f.readlines()
        f.close()

        #如果没有代理IP则进行抓取
        if (len(contents) == 0):
            #没有内容，说明已经没有可用的IP地址了
            self.IPList = []
            # 从西刺代理中获取可用的IP地址
            # 抓取西刺代理第2~4页总共3页的网页数据
            for page in range(2, 4):
                IPUrl = 'http://www.xicidaili.com/nn/' + str(page)  # 西刺代理url
                IPHeaders = {"User-Agent": random.choice(self.user_agent_list)}
                IPRequest = urllib2.Request(IPUrl, headers=IPHeaders)
                IPhtml = urllib2.urlopen(IPRequest).read().decode('utf-8')
                pattern = re.compile(r"<td>(\d.*?)</td>", re.S)  # 截取<td></td>之间第一个字符为数字的内容
                IP_page = re.findall(pattern, IPhtml)
                for IP in IP_page:
                    IP = IP.strip()
                    self.IPList.append(IP)  # 将获取的IP加入数组中


                time.sleep(random.choice(range(1, 3)))  # 每抓取一页IP地址就间歇1~3秒，以防止被封

            # 抓取完毕之后进行IP地址的整理和检验
            proxy_file = open(IPListFilePath, "w")
            lock = threading.Lock()  # 建立一个锁
            for i in range(0, len(self.IPList), 4):  # 最后一个参数说明每次的循环都是4个4个的遍历

                try:
                    telnetlib.Telnet(self.IPList[i], port=str(self.IPList[i + 1]),
                                     timeout=10)  # 使用telnetlib模块来检测IP地址是否可用
                except Exception as e:
                    #print '链接失败，该IP地址无效,原因是: ' + str(e)
                    continue
                else:
                    #print '链接成功，该IP地址可用'
                    proxy_host = "http://" + self.IPList[i] + ':' + self.IPList[i + 1]
                    proxy_temp = {"http": proxy_host}
                    lock.acquire()  # 获得锁
                    proxy_file.write("%s\n" % proxy_temp)  # 写入该有效的IP地址
                    lock.release()  # 释放锁
            proxy_file.close()  # 关闭文件
            self.IPListArr = self.IPList
        else:
            #从文件中获取代理IP
            self.IPListArr = contents




    def gethtml(self,url,data=None,ifuseProxy=False,decodestyle='utf-8'):
        # 开始抓取网页数据
        proxy = eval(random.choice(self.IPListArr)) #将储存在文件中的代理IP字符串转换为字典对象
        data = data
        headers = {"User-Agent": random.choice(self.user_agent_list)}
        request = urllib2.Request(url,headers= headers)

        #根据参数决定是否使用代理IP
        if ifuseProxy: #使用代理IP
            proxy_support = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

        try:
            html = urllib2.urlopen(request).read().decode(decodestyle)  # 获取到源码
            return html
        except Exception as e:
            print '使用代理IP获取数据失败，原因是:' + e.message
            #如果请求失败的话则换作使用代理IP进行请求
            self.gethtml(url,data,True,decodestyle)

#检查字符中是否存在数字，是返回True 否返回False
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


#语言翻译方法  默认传入类型是自动检测,totype是输出类型,默认为翻译为英文,即en,如果是泰文则为th,详见:http://api.fanyi.baidu.com/api/trans/product/apidoc
def TranslateLanguage(inputString,fromtype='auto',totype='en'):

    #首先初始化百度翻译API所需要的数据
    q = str(inputString)  #这里不需要进行encode转化,即在获取到sign之前都是不需要进行encode转化的！！！
    myfromtype = fromtype
    mytotype = totype
    appid = "20171022000090209"
    key = 'WFOiHRMxcqMKb6XkILxV'
    salt = random.randint(10001, 99999) #随机数

    #获取签名
    m = str(appid) + q + str(salt) + key
    m_MD5 = hashlib.md5(m)
    sign = m_MD5.hexdigest()

    #拼接参数 注意此处就要对输入内容q进行encode转化了,使用url
    Url_1 = '/api/trans/vip/translate' #翻译原始链接
    Url_2 = '?q=' + urllib2.quote(q) + '&from=' + myfromtype + '&to=' + mytotype + '&appid=' + str(appid) + '&salt=' + str(salt) + '&sign=' + sign  #需要拼接的参数
    Url = Url_1 + Url_2
    PostUrl = Url.decode()
    httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', PostUrl)
    # response是HTTPResponse对象
    response = httpClient.getresponse()
    TransResult = response.read()
    #获取到翻译内容,进行解析
    data = json.loads(TransResult)
    if 'error_code' in data:
        #翻译出错,返回默认的字符串-"百度翻译出错了哦,正在努力抢修中……"
        print '翻译出错,原因为:', data['error_msg']
        return "百度翻译出错了哦,正在努力抢修中……"
    else:
        #翻译成功,返回翻译结果
        result = data['trans_result'][0]['dst']
        return result

#日志记录功能
def recordlogging():

#     logging.basicConfig函数各参数:
#     filename: 指定日志文件名
#     filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
#     format: 指定输出的格式和内容，format可以输出很多有用信息，如上例所示:
#     % (levelno)s: 打印日志级别的数值
#     % (levelname)s: 打印日志级别名称
#     % (pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
#     % (filename)s: 打印当前执行程序名
#     % (funcName)s: 打印日志的当前函数
#     % (lineno)d: 打印日志的当前行号
#     % (asctime)s: 打印日志的时间
#     % (thread)d: 打印线程ID
#     % (threadName)s: 打印线程名称
#     % (process)d: 打印进程ID
#     % (message)s: 打印日志信息
#
#     datefmt: 指定时间格式，同time.strftime()
#     level: 设置日志级别，默认为logging.WARNING
#     stream: 指定将日志的输出流，可以指定输出到sys.stderr, sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略
#     日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，当然也可以自己定义日志级别。
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='logfile.txt',
                        filemode='w')

    #################################################################################################
    #定义一个StreamHandler，将DEBUG级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################

#向小海哥发送错误提醒邮件
def senderrtoXHG(projectname,errmsg):
    errtoXHG = sendEmailTools.SendMailClass()
    errtoXHG.sendmail(
        ["891508172@qq.com"],
        "工程名称:"+projectname+"  错误:" +errmsg,
        emailsubject="程序《"+projectname+"》发生错误,小海哥点击查看吧~",
        emailfooter="——小海哥Bug纠察中心",
    )
    print "Bug纠察中心已经收到程序的反馈日志,请耐性等待小海哥的处理"











