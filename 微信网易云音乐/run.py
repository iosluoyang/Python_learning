# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import sys
sys.path.append("/var/www/html/python_projects/publicTools")
import logging #日志记录
import public  #公共方法文件

import itchat
from itchat.content import *
import time
import netease
import subprocess


myUserName = ''
peer_list = []

will_play_list = []
process = None


def musicbox():

    itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='自动登录日志记录文件_网易音乐播放器')
    my = itchat.get_friends(update=True)[0]
    global myUserName
    myUserName = my.UserName
    mynickname = my.NickName
    print '嗨,亲爱的%s,您已经开启网易云音乐播放器模式' % mynickname
    itchat.run()


# 注册文字消息
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isMpChat=True)
def text_reply(msg):
    global myUserName, neteasestate, peer_list

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
    # 消息发送者的唯一标识: 文件传输助手和本人一致 但是发送消息的时候只能给文件助手发 filehelper
    FromUserName = msg['FromUserName']
    #消息的发送对象- 如果是文件传输助手则发送给文件传输助手,如果是是其他人则发送给信息的发送人作为回复
    MsgToUserName = 'filehelper' if msg.User.UserName == "filehelper" else FromUserName



    # 本人给发送者备注的昵称:(如果是文件传输助手的话则User没有RemarkName字段)
    MsgRemarkName = msg.User.RemarkName if msg.User.UserName != "filehelper" and msg.User.RemarkName != ''  else "本人"

    # 发送者自己的微信昵称
    MsgOwnNickName = msg.User.NickName if msg.User.UserName != "filehelper" and msg.User.RemarkName != '' and msg.User.NickName  else "本人"

    # 消息发送时间: 转换为指定格式的日期时间
    MsgCreateTime = msg.CreateTime
    timeArray = time.localtime(MsgCreateTime)
    MsgCreateTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    # 消息内容:
    MsgContent = msg.Content

    print "您在%s收到了%s的消息,消息内容为:\n%s" % (MsgCreateTime, MsgRemarkName, MsgContent)

    # 开启网易云音乐模式
    if MsgContent == '开启网易云音乐模式':

        # 根据唯一标识开始找该位用户
        findtheperson = [person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName]
        if len(findtheperson) > 0:
            findtheperson = findtheperson[0]
        else:
            findtheperson = None

        # 如果能找到,看其开启的状态
        if findtheperson:
            # 已经是开启状态了
            if findtheperson['ifnetease']:
                itchat.send_msg('亲,您已经开启了网易云音乐模式哦~~\n\n直接输入您想要听到的歌曲名称即可', toUserName = MsgToUserName)

            # 还没有开启,更改开启状态即可
            else:
                findtheperson['ifnetease'] = True

                itchat.send_msg('亲,欢迎您回来~~\n\n直接输入您想要听到的歌曲名称即可', toUserName = MsgToUserName)

        # 如果找不到该人说明该用户还没有开启网易云音乐模式,直接开启即可
        else:

            # 构造记录对方是否要求开启的字典:
            thisUser = {"FromUserName": FromUserName, "ifnetease": True}
            # 将记录的字典添加到全局的人员记录表中
            peer_list.append(thisUser)

            itchat.send("通知:用户--" + MsgRemarkName + "--已经成功解锁小海哥网易云音乐模式~~", toUserName='filehelper')
            itchat.send('终于等到你!伟大的--' + MsgOwnNickName + '--用户,您已经成功解锁小海哥网易云音乐模式~~\n\n直接输入您想要听到的歌曲名称即可', toUserName = MsgToUserName)

    # 用户要求关闭网易云音乐模式
    elif MsgContent == '关闭网易云音乐模式':

        # 根据唯一标识开始找该位用户
        findtheperson = [person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName][0]

        # 如果能找到说明该人已经开启了网易云音乐模式,直接改为关闭即可
        if findtheperson:
            # 查看该人的开启状态
            # 已经是开启状态,则改变记录的状态,如果已经关闭,则不做任何处理
            if findtheperson['ifnetease']:
                findtheperson['ifnetease'] = False
            itchat.send('小海哥网易云音乐模式已经关闭~~[不舍]', toUserName=MsgToUserName)

        # 如果找不到该人说明该人还没有开启网易云音乐音乐模式
        else:
            itchat.send_msg('亲,你还没有开启小海哥网易云音乐模式哦[囧]\n\n试试输入: "开启网易云音乐模式" 来解锁新技能~~', toUserName = MsgToUserName)

    # 判断该用户是否已经开启了网易云音乐模式,如果没有开启则引导开启,如果已经开启则进行分析阶段
    else:

        # 根据唯一标识开始找该位用户
        findtheperson = [person for i, person in enumerate(peer_list) if person['FromUserName'] == FromUserName]
        if len(findtheperson) > 0:
            findtheperson = findtheperson[0]
        else:
            findtheperson = False

        # 如果能找到该用户并且用户开启了网易云音乐模式的话进入下一阶段,否则一律忽略用户发送的消息
        if findtheperson and findtheperson['ifnetease']:

            content = MsgContent
            content_list = content.split()

            if len(content_list) == 1:
                song_name = content
                musicbox = netease.RasWxMusicbox(song_name)
                music_list = musicbox.gen_music_list()
                itchat.send('小海哥搜索到的歌曲列表如下:\n\n' + music_list,toUserName = MsgToUserName)
                itchat.send('挑选以上列表中您喜欢的歌曲,然后按照 歌曲名称+空格+歌曲编号 发送给小海哥即可自动选中歌曲\n\n例如:晴天 0', toUserName=MsgToUserName)

            elif len(content_list) == 2:
                try:
                    song_name = content_list[0]
                    song_index = int(content_list[1])
                    musicbox = netease.RasWxMusicbox(song_name)
                    music_info = musicbox.get_music(song_index)
                    mp3_url = music_info['mp3_url']
                    song_info = u'小海哥为您找到该歌曲的信息:\n\n' \
                                + u'专辑： ' + music_info['album_name'] + '\n' \
                                + u'演唱： ' + music_info['artist'] + '\n' \
                                + u'歌曲： ' +"《"+ music_info['song_name'] + "》" + '\n\n' \
                                +'点击播放:'+ mp3_url


                    itchat.send(song_info,toUserName = MsgToUserName)

                except:
                    itchat.send('输入有误，请重新输入\n\n挑选您喜欢的歌曲,然后按照 歌曲名称+空格+歌曲编号 发送给小海哥即可播放\n\n例如:晴天 0', toUserName=MsgToUserName)
            else:
                itchat.send('输入有误，请重新输入歌曲名称', toUserName=MsgToUserName)



if __name__ == '__main__':
    musicbox()

