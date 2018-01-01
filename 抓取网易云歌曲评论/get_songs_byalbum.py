# -*- coding: utf-8 -*-
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import BaseData
import sql
import threading
import pymysql
from bs4 import BeautifulSoup
import json
import bs4
import re
import get_comments_bysong




# 抓取专辑中的歌曲集合
def get_songs_byalbumid(albumid):

    html_text = BaseData.get_songsjson(albumid)
    #因为歌曲信息抓取下来不是Json数据，所以需要用BeautifulSoup进行提取

    #网页解析
    soup = BeautifulSoup(html_text, 'html.parser')
    body = soup.body

    #保存专辑简介信息
    try:
        # 简要介绍信息
        simpledes = body.select('div#album-desc-dot')[0].text
        # 详细介绍信息
        moredes = body.select('div#album-desc-more')[0].text

        # print ('该专辑的简要简介为:%s\n\n\n详细简介为:%s' %(simpledes,moredes))
        # 将专辑描述信息保存至数据库
        sql.save_des_album(albumid, simpledes, moredes)
    except:
        print ('获取专辑简介失败')


    #喜欢该专辑的几个用户信息
    favouriteusers = body.select('ul.m-piclist li')
    for i , user in enumerate(favouriteusers):

        # 用户id:
        User_id = user.a['href'].replace('/user/home?id=', '')  # 用户id

        #用户昵称:
        UserNickname = user.a['title']

        #用户头像:
        User_ImgUrl = user.a.img['src']

        i+=1
        #print('喜欢该专辑的第 %s/%s 用户信息为: 用户id为:%s 用户昵称为为:%s 用户头像图片地址为:%s' % (i,len(favouriteusers) , User_id, UserNickname, User_ImgUrl))

    #保存专辑歌曲信息
    songs = body.select('div.n-songtb li')  # 获取专辑的所有音乐
    for i , song in enumerate(songs):

        song = song.a
        song_id = song['href'].replace('/song?id=', '')#歌曲id
        song_name = song.text#歌曲名称

        # 将歌曲信息保存至数据库
        sql.save_song(song_id, song_name,albumid)

        #根据歌曲id获取并保存热门评论相关信息
        get_comments_bysong.get_hot_comments(song_id)

        #根据歌曲id获取并保存普通评论相关信息(限制前3页的评论)
        #get_comments_bysong.get_all_comments(song_id,True,3)

        # 汇报进度
        i+=1
        print('专辑id为:%s 歌曲id为:%s 歌曲名称为:%s 进度显示:%d / %d' % (albumid , song_id, song_name, i, len(songs)))

    #保存该专辑的热门评论信息
    # url = "http://music.163.com/weapi/v1/resource/comments/R_AL_3_" + str(albumid) + "/?csrf_token="
    # json_text = BaseData.get_commentsjson(url, 1)
    # # 容错
    # if (json_text):
    #     json_dict = json.loads(json_text)
    #
    #     hot_comments = json_dict['hotComments']  # 热门评论数组
    #     for index, item in enumerate(hot_comments):
    #         comment = item['content']  # 评论内容
    #         likedCount = item['likedCount']  # 点赞总数
    #         comment_time = item['time']  # 评论时间(时间戳)
    #         userID = item['user']['userId']  # 评论者id
    #         nickname = item['user']['nickname']  # 昵称
    #         avatarUrl = item['user']['avatarUrl']  # 头像地址
    #
    #         index+=1
    #         print ("保存该专辑的热门评论的进度:%d / %d , 评论人id:%s 评论人昵称:%s 评论人头像地址:%s 评论内容: %s 评论时间:%s 点赞数:%s" % (index, len(hot_comments) ,userID,nickname,avatarUrl,comment,comment_time,likedCount))
    #     print "\n\n\n-----------热门评论已经加载完成-------------------\n\n\n"
    #
    #     allnormalcommentsArr = [] #所有普通评论的合集数组
    #     totalcomments = int(json_dict['total']) #总的普通评论的全部数量 每一页是20条数据
    #
    #     #此处写死页数,加载3页评论即可
    #     totalpage = 3
    #     # totalpage =  totalcomments/20 if totalcomments%20 == 0 else totalcomments/20 +1
    #     for page in range(1,totalpage+1):
    #         #在每一页中解析普通评论数据
    #         json_text = BaseData.get_commentsjson(url, page)
    #         if(json_text):
    #             json_dict = json.loads(json_text)
    #             comments = json_dict['comments']  # 普通评论数组
    #             print "\n\n\n-----------普通评论加载进度: %d / %d-------------------\n\n\n" %(page,totalpage)
    #
    #             for index, item in enumerate(comments):
    #                 comment = item['content']  # 评论内容
    #                 likedCount = item['likedCount']  # 点赞总数
    #                 comment_time = item['time']  # 评论时间(时间戳)
    #                 userID = item['user']['userId']  # 评论者id
    #                 nickname = item['user']['nickname']  # 昵称
    #                 avatarUrl = item['user']['avatarUrl']  # 头像地址
    #
    #                 index += 1
    #                 print ("保存该专辑的普通评论的进度:%d / %d , 评论人id:%s 评论人昵称:%s 评论人头像地址:%s 评论内容: %s 评论时间:%s 点赞数:%s" % (
    #                 index, len(comments), userID, nickname, avatarUrl, comment, comment_time, likedCount))
    #
    #                 # 将评论逐条保存到数据库中
    #                 sql.save_commentsofalbum(albumid, nickname, userID, avatarUrl, comment, comment_time, likedCount,
    #                                          connection)
    #
    # else:
    #     print('专辑id为:%s的专辑热门或者普通评论加载失败' %(albumid))




if __name__ == "__main__":


    artistid = input("请输入你想抓取的专辑的id:<例如周杰伦的床边故事的id为 34720827>")
    print ('开始抓取专辑的信息……')
    t1 = threading.Thread(target=get_songs_byalbumid, args=(str(artistid),))
    t1.start()


