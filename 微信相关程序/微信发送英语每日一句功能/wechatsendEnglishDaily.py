# encoding: utf-8


import os
import shutil

#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import sys
sys.path.append("/var/www/html/python_projects/publicTools")

reload(sys)
sys.setdefaultencoding('utf8')


from selenium import webdriver #打开浏览器文件
import requests #下载图片到本地使用
from datetime import datetime
import time
import json
from  apscheduler.schedulers.blocking import  BlockingScheduler
import public
from sendEmailTools import  SendMailClass
from config import EmailAddressEnum

import itchat
from itchat.content import *

tulingKey = "8d8c36e424b6fd2d7faab69c8a6e39b7"
myUserName = ''
leave = False
peer_list = []
# 获取当前月和日
datestr = datetime.strftime(datetime.now(), '%m月%d日')


#注册文字消息
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isMpChat=True)
def text_reply(msg):
    global myUserName,leave,peer_list

    '''
    itchat中消息体的各关键字段含义
    FromUserName    发送消息的人唯一标识
    Type            消息类型    文字消息Text 语音消息Recording  图片消息Picture  小视频消息Video 位置信息Map 名片消息Card  附件消息Attachment
    MsgType         消息体类型标识 1文字或者位置信息   34语音消息  名片消息42 小视频消息43 3图片消息   附件消息49
    Content         发送消息的内容
    ToUserName      接收者的唯一标识
    User            发送者自己的用户信息字典(参考用户信息字典字段参数)
                    发送者自己的唯一标识 注意如果是文件传输助手的话则该字段为filehelper 并且没有其他User的字段
                    RemarkName      备注名称   注意如果是自己发送的消息,则备注名称为空 如果是文件传输助手发送的消息则没有该项
                    NickName        发送者自己的微信昵称
                    Signature       发送者的签名
                    HeadImgUrl  头像地址
                    Sex         性别 1是男
    CreateTime      消息发送的时间

    '''
    #消息发送者的唯一标识: 文件传输助手和本人一致
    FromUserName = msg['FromUserName']

    #本人给发送者备注的昵称:
    MsgRemarkName = "文件传输助手" if msg.User.UserName == "filehelper"  else   msg.User.RemarkName if msg.User.RemarkName != '' else "自己本人"

    #消息发送时间: 转换为指定格式的日期时间
    MsgCreateTime = msg.CreateTime
    timeArray = time.localtime(MsgCreateTime)
    MsgCreateTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    # 消息内容:
    MsgContent = msg.Content

    print "您在%s收到了%s的消息,消息内容为:\n%s" %(MsgCreateTime,MsgRemarkName,MsgContent)



    #如果是收到本人的消息则根据消息内容进行开启离开模式或者关闭离开模式
    if FromUserName == myUserName:

        #开启离开模式
        if MsgContent == '开启离开模式':
            leave = True
            print ("您已经开启了离开模式,如果有人给您发消息的话,会有小海哥陪聊哦~~")
            itchat.send('您已经开启了离开模式,如果有人给您发消息的话,会有小海哥陪聊哦~~', toUserName='filehelper')
        #关闭离开模式
        elif MsgContent == '关闭离开模式':
            leave = False
            print ("您已经关闭了离开模式,注意查收您的消息哦~~")
            itchat.send('您已经关闭了离开模式,注意查收您的消息哦~~', toUserName='filehelper')
        #收到本人的其他消息
        else:
            itchat.send('小海哥管家在'+MsgCreateTime+'收到了主人的消息:\n' + MsgContent, toUserName='filehelper')

    #收到别人的消息,根据开启的模式进行场景选择
    else:

        # 发送者自己的微信昵称
        MsgOwnNickName = msg.User.NickName if msg.User.NickName  else "你"

        # 首先根据别人发送的消息标识判断是否是开启或者关闭小海哥智能聊天模式

        # 对方要求开启智能聊天模式
        if MsgContent == '小海哥上班':

            # 根据唯一标识开始找该位用户
            findtheperson = [person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName]
            if len(findtheperson)>0:
                findtheperson = [person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName][0]
            else:findtheperson = False

            # 如果能找到,看其开启的状态
            if findtheperson:
                #已经是开启状态了
                if findtheperson['ifrobot']:
                    itchat.send_msg('喂,主人忘记了嘛,小海哥已经上班了啊~', toUserName=FromUserName)

                #还没有开启,更改开启状态即可
                else:
                    findtheperson['ifrobot'] = True
                    itchat.send_msg('哎……又要上班了!不过一想到能见到亲爱的'+MsgOwnNickName+'小海哥顿时觉得浑身充满了力量!',
                                    toUserName=FromUserName)

            # 如果找不到该人说明该人还没有开启智能回复,直接开启智能回复即可
            else:
                # 构造记录对方是否要求开启的字典:
                thisUser = {"FromUserName": FromUserName, "ifrobot": True}
                # 将记录的字典添加到全局的人员记录表中
                peer_list.append(thisUser)
                itchat.send_msg('小海哥开始上班了!\n从现在起和你聊天的就是小海哥我了,不是炫酷无敌的主人哦~~\n\n'
                                '如果不想和小海哥聊天了,试试输入 <小海哥下班> 挥泪告别\n'
                                '讲笑话查天气陪聊天知识百科,炫酷无敌就是我,宇宙最强小海哥~~',
                                toUserName=FromUserName)

        # 对方要求关闭智能聊天模式
        elif MsgContent == '小海哥下班':


            #根据唯一标识开始找该位用户
            findtheperson =  [person for i,person in enumerate(peer_list) if person['FromUserName'] == FromUserName][0]

            #如果能找到说明该人已经开启了智能回复,直接改为关闭即可
            if findtheperson:
                #查看该人的开启状态
                #已经是开启状态,则关闭即可
                if findtheperson['ifrobot']:
                    findtheperson['ifrobot'] = False
                    itchat.send_msg('小海哥下班了,很高兴和你聊天哦,我们下次再会~~[不舍]', toUserName=FromUserName)
                #已经关闭了,报都已经下班了
                else:
                    itchat.send_msg('你不是让小海哥早都下班了嘛,怎么？想念小海哥了?\n试试输入: <小海哥上班> 来和小海哥聊天~~', toUserName=FromUserName)

            #如果找不到该人说明该人还没有开启智能回复,引导该人开启智能回复
            else:
                itchat.send_msg('亲,小海哥都还没有上班,怎么会下班?[囧]\n试试输入: <小海哥上班> 来和小海哥聊天~~', toUserName=FromUserName)

        # 对方跟你随便聊聊天
        else:

            #判断自己是否开启了离开模式,如果已经开启,则进入智能聊天模式判断,如果未开启,则不处理任何的信息
            if leave:
                # 判断该用户是否开启了智能聊天模式,如果已经开启,则开始智能聊天,如果没有开启或者不在列表中,则依旧报固定的离开文本

                # 根据唯一标识开始找该位用户
                findtheperson = [person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName]
                if len(findtheperson) > 0:
                    findtheperson =[person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName][0]
                else:
                    findtheperson = False

                # 如果能找到
                if findtheperson:
                    # 查看该人是否已经开启了智能回复

                    # 已经开启,直接智能聊天
                    if findtheperson['ifrobot']:

                        # 从图灵接口处获取智能回复的内容
                        cont = requests.get(
                            'http://www.tuling123.com/openapi/api?key=%s&info=%s' % (tulingKey, MsgContent)).content
                        # 解析内容并发送
                        m = json.loads(cont)
                        itchat.send(m['text'], FromUserName)
                        if m['code'] == 200000:  # 链接内容
                            itchat.send(m['url'], FromUserName)
                        if m['code'] == 302000:  # 列表内容
                            itchat.send(m['list'], FromUserName)
                        if m['code'] == 308000:  # 列表内容
                            itchat.send(m['list'], FromUserName)
                    # 未开启智能聊天,引导用户开启智能聊天模式
                    else:
                        itchat.send_msg('嗨,亲爱的' + MsgOwnNickName + ':\n' +
                                        '小海哥温馨提示您,炫酷无敌的主人现在有事儿出去了,'
                                        '等主人回来后我会告诉主人您来过了哦\n\n'
                                        'Tips:可以试试输入: <小海哥上班> 来和小海哥聊天~~',
                                        toUserName=FromUserName)

                # 如果找不到该人说明该人还没有开启过智能回复,引导该人开启智能回复
                else:
                    itchat.send_msg('嗨,亲爱的' + MsgOwnNickName + ':\n' +
                                    '小海哥温馨提示您,炫酷无敌的主人现在有事儿出去了,'
                                    '等主人回来后我会告诉主人您来过了哦\n\n'
                                    'Tips:可以试试输入: <小海哥上班> 来和小海哥聊天~~',
                                    toUserName=FromUserName)
            #如果没有开启离开模式,则忽略用户的其他信息
            else:
                itchat.send('小海哥管家在' + MsgCreateTime + '收到了'+MsgRemarkName+'的消息:\n' + MsgContent + '\n请注意查看哦', toUserName='filehelper')


#抓取英语每日一句的网站,返回具有四个元素的内容字典对象
def getEnglishDaily():

    # 首先获取当前日期
    timestr = datetime.strftime(datetime.now(), '%Y-%m-%d')
    url = "http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/" + timestr
    browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    #设置加载超时时长
    browser.set_page_load_timeout(60)
    browser.set_script_timeout(60)  # 这两种设置都进行才有效
    #尝试获取获取网页数据,如果超过1分钟还没有加载完,则尝试重新加载
    try:
        browser.get(url)
    except Exception as e:
        if e != KeyboardInterrupt:
            browser.execute_script('window.stop()')
            getEnglishDaily()
            return

    #休眠3秒钟之后开始解析数据:
    time.sleep(3)

    #每日一句 en:
    dailyEnglish = browser.find_element_by_css_selector("div.detail-content-en").text

    #每日一句 zh:
    dailyChinese = browser.find_element_by_css_selector("div.detail-content-zh").text


    #每日一句 图片地址:
    dailyImgUrl = browser.find_element_by_css_selector("img.detail-banner-img").get_attribute("src")

    #点赞数量
    dailyZanNumber = browser.find_element_by_css_selector("div.detail-content-numbers span.numbers-zan").text

    #如果这4个数据其中有一个数据缺失的话都重新加载数据
    if (not dailyEnglish or  not dailyChinese or not dailyImgUrl or not dailyZanNumber):
        print ("抓取数据中有缺失的数据,故重新开始加载")
        getEnglishDaily()
        return


    print (datestr +":------"+ "抓取英语每日一句数据成功:\n" + dailyEnglish + "\n" + dailyChinese + "\n"  + "图片地址:  " + dailyImgUrl + "\n" + "点赞数量:" + dailyZanNumber)

    ContentDic = {"dailyEnglish":dailyEnglish,"dailyChinese":dailyChinese,"dailyImgUrl":dailyImgUrl,"dailyZanNumber":dailyZanNumber,}
    return ContentDic

#用于检查登录状态时获取到的uuid 没有保存二维码图片的操作
def getuuid():
    uuid = itchat.get_QRuuid()
    while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
    return uuid
#登录微信
def loginwechat():
    uuid = getuuid()
    #无限循环中,一旦检测到已经登录成功了就结束循环
    while 1:

        # 首先先判断是否已经登录了微信,如果是已经登录了则直接break掉继续后面的操作即可
        status = itchat.check_login(uuid) #注意此处如果未登录,每次检查是否登录都需要32秒钟的时间
        if status == '200':
            # 登录成功
            print ("登录成功")
            break
        elif status == '201':
            #已经扫描二维码等待确认
            print ('已经扫描二维码,等待确认中……')

        elif status == '408':
            # 二维码已经失效 (如果是未登录,则经过32秒的检查时间会来到二维码失效的方法中)
            print "二维码失效,重新加载二维码"
            # 首先获取uuid
            uuid = getuuid()
            # 根据uuid获取到最新的二维码并打开
            itchat.get_QR(uuid=uuid,picDir='QR.jpg')
            #将存储在本地的二维码图片用邮件发送到指定邮箱使其用户进行扫描
            sendemail = SendMailClass()
            sendemail.sendmail([EmailAddressEnum.liuhaiyang1],"请点击以下二维码:",emailimgArr=["QR.jpg"],emailsubject='扫描二维码登录微信',emailfooter="小海哥微信登录中心")
            print "邮件发送完毕"




            # 如果是登陆失败的情况，则开始尝试登录
            # 登录微信   热登录
            # itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='微信英语每日一句登录日志')
    #userInfo = itchat.web_init()
    #itchat.show_mobile_login()



#将获取到内容使用微信发送
def wechatsendEnglishDaily():

    morningwords = "嗨," + datestr + "," + "早上好:"

    #登录完之后开始获取英语每日一句的内容
    ContentDic = getEnglishDaily()

    try:
        English = ContentDic["dailyEnglish"]
        Chinese = ContentDic["dailyChinese"]
        ImgUrl = ContentDic["dailyImgUrl"]
        ZanNumber = ContentDic["dailyZanNumber"]
    except Exception as e:
        wechatsendEnglishDaily()
        return


    #首先将图片下载到本地,命名统一规范为img.jpg
    try:
        pic = requests.get(ImgUrl, timeout=10)
        fp = open("img.jpg", 'wb')
        fp.write(pic.content)
        fp.close()
        #将当前的图片目录路径转移到对应工程下
        #shutil.copy(os.getcwd() + '/' + 'img.jpg', '/var/www/html/python_projects/微信相关程序/微信发送英语每日一句功能/img.jpg')
    except requests.exceptions.ConnectionError:
        print (datestr+':------'+'该图片无法下载')

    #组合微信要发送的内容(文字+图片):
    sendText = morningwords + "\n\n" + English + "\n\n" + Chinese + "\n\n" + "(当前已经有" + ZanNumber +"人点赞)" + "\n\n" + "    -----小海哥每日一句"


    #登录微信授权的操作
    loginwechat()

    #从本地文件中获取到要发送的人的信息 字典数组
    toUserlist = public.returndatafromreadcsvfile('toUsersList.csv')

    #遍历接收者数组,挨个发送
    for user in toUserlist:

        wechatID = user["username"]
        # 发送文字:
        itchat.send_msg(sendText, toUserName=wechatID)
        # 发送图片:
        itchat.send_image('img.jpg', toUserName=wechatID) #不存在该文件时将打印无此文件的提醒

    print "微信登录成功,信息发送成功"

    # #发送完毕之后即刻进入离线模式
    #
    # # 获取到自己的用户名
    #
    # '''
    # 关于itchat中用户的信息字典含义:
    # UserName  微信的唯一id，一般用于判断是否是某个人的标准
    # Signature   微信签名
    # NickName    昵称
    # HeadImgUrl  头像地址
    # Sex         性别 1是男
    # '''
    #
    # my = itchat.get_friends(update=True)[0]
    # global myUserName
    # myUserName = my.UserName
    # mynickname = my.NickName
    # mysex = "男" if my.Sex == 1 else "女"
    # mysign = my.Signature
    #
    # print '嗨,%s,您的性别是%s,您的微信签名是:%s' % (mynickname, mysex, mysign)
    # friends_list = itchat.get_friends()
    # JsonStr = json.dumps(friends_list, ensure_ascii=False, encoding='UTF-8')
    # print "您的好友通讯录为:" + JsonStr
    #
    # itchat.run()




# sched = BlockingScheduler()     #定义一个定时器,调度这些工作
# sched.add_job(wechatsendEnglishDaily, 'cron',second = '*/100')
# #sched.add_job(wechatsendEnglishDaily, 'cron', day_of_week="mon-sun", hour=8, minute=00)  #通过add_job来添加作业 每天上午8点自动发送
# sched.start()


loginwechat()




























