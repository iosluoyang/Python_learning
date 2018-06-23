# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
from apscheduler.schedulers.background import BackgroundScheduler #定时任务
import sys
sys.path.append("/var/www/html/python_projects/publicTools")
import logging #日志记录
import public  #公共方法文件

import itchat
from itchat.content import *

import sys
import time
import re
import requests, json
import aiml
import os

myUserName = ''
content = '微信轰炸~~~Boooooooooom'
latestcontent = content
ifstart = False
sched = BackgroundScheduler()

#登录微信
def loginwechat():

    itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='自动登录日志记录文件')


#注册文字消息
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isMpChat=True)
def text_reply(msg):
    global myUserName,ifstart,content,latestcontent,sched

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

    print "消息的发送者唯一标识为:%s" %(FromUserName)

    #如果是收到本人的消息则根据指令进行微信消息轰炸
    if FromUserName == myUserName:

        #开启微信轰炸模式
        if MsgContent == '开启微信轰炸模式':
            print ("您已经开启了微信轰炸模式")
        #关闭微信轰炸模式
        elif MsgContent == '关闭微信轰炸模式':
            print ("您已经关闭了离开模式,注意查收您的消息哦~~")
        #收到本人的其他消息
        else:
            itchat.send('小海哥管家在'+MsgCreateTime+'收到了主人的消息:\n' + MsgContent, toUserName='filehelper')

    #收到指定对方备注的消息,根据开启的模式进行场景选择
    elif MsgRemarkName.find("侯森") >= 0 or MsgRemarkName.find("温源") >= 0 or MsgRemarkName.find("友谊") >= 0 :

        # 对方要求开启微信轰炸模式
        if MsgContent == '轰炸':

            itchat.send_msg('请告诉小海哥您要轰炸的内容~~', toUserName=FromUserName)
            ifstart = True

        # 对方要求关闭微信轰炸模式
        elif MsgContent == '关闭轰炸':
            try:
                ifstart = False
                sched.remove_job(MsgRemarkName)
                itchat.send_msg('微信轰炸模式已经关闭', toUserName=FromUserName)
            except Exception as e:
                itchat.send_msg('亲,您还没有开启轰炸呢吧~~', toUserName=FromUserName)

        #进行内容的替换  恢复定时器
        elif MsgContent == '1':

            if ifstart:
                content = latestcontent

                itchat.send_msg('亲,已经将轰炸内容更改为:\n' + content, toUserName=FromUserName)

                sched.job.Job.resume()

        #不进行替换   恢复定时器
        elif MsgContent == '0':

            if ifstart:

                latestcontent = content

                itchat.send_msg('亲,您已经取消替换,轰炸将继续', toUserName=FromUserName)

                sched.job.Job.resume()

        #其他消息
        else:
            # 如果已经开启轰炸模式则直接设置定时器
            if ifstart:

                content = MsgContent

                try:

                    sched.add_job(sendmsg, 'interval', seconds=1, id=MsgRemarkName,args=[FromUserName])
                    sched.start()

                except Exception as e:

                    print "已经存在过定时器了,本次添加忽略~~"






                # #如果当前消息和之前消息不一致的话说明用户想替换轰炸内容,则根据用户指令进行操作
                # if MsgContent != content:
                #
                #     #暂停Job
                #     sched.job.Job.pause()
                #     latestcontent = MsgContent
                #     itchat.send_msg('检测到您发送了和之前轰炸内容不一致的消息,您是否要将轰炸内容替换为:\n'+latestcontent+'\n 0取消替换  1确认替换~~', toUserName=FromUserName)

            # 未开启轰炸模式 回复干哈~~
            else:
                itchat.send_msg('亲,你还未开启轰炸机功能,回复轰炸指令开启~~~~', toUserName=FromUserName)




def sendmsg(FromUserName):
    itchat.send_msg(content, toUserName=FromUserName)

def startrun():

    # 热登录
    loginwechat()

    '''
    关于itchat中用户的信息字典含义:
    UserName  微信的唯一id，一般用于判断是否是某个人的标准
    Signature   微信签名
    NickName    昵称
    HeadImgUrl  头像地址
    Sex         性别 1是男
    '''

    my = itchat.get_friends(update=True)[0]
    global myUserName
    myUserName = my.UserName
    mynickname = my.NickName
    mysex = "男" if my.Sex == 1 else "女"
    mysign = my.Signature

    print '嗨,%s,您的性别是%s,您的微信签名是:%s' % (mynickname, mysex, mysign)
    friends_list = itchat.get_friends(update=True)
    JsonStr = json.dumps(friends_list, ensure_ascii=False, encoding='UTF-8')
    print "您的好友通讯录为:" + JsonStr

    itchat.run()

startrun()








