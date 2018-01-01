# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
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

tulingKey = "8d8c36e424b6fd2d7faab69c8a6e39b7"
myUserName = ''
leave = False
peer_list = []

#获取微信登录的uuid
def getuuid():
    for get_count in range(10):
        uuid = itchat.get_QRuuid()
        while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
        if itchat.get_QR(uuid,picDir='QR.jpg'): break  #将获取到的二维码图片存到本地叫做QR.jpg的图片
    return uuid
#登录微信
def loginwechat():

    #首先先判断是否已经登录了微信,如果是已经登录了则直接return掉
    status = itchat.check_login(getuuid())
    if status == '200':
        # 登录成功
        return
    else:
        print ('未登录,正在尝试登录……')
        # 如果是登陆失败的情况，则开始尝试登录
        # 登录微信   热登录
        itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='自动登录日志记录文件')


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
    friends_list = itchat.get_friends()
    JsonStr = json.dumps(friends_list, ensure_ascii=False, encoding='UTF-8')
    print "您的好友通讯录为:" + JsonStr



    itchat.run()

startrun()








