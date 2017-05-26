# -*- coding: utf-8 -*-
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import BaseData
import sql
import threading
import pymysql
from bs4 import BeautifulSoup
import bs4
import re
import get_comments_bysong




# 抓取歌曲集合
def get_songs_byalbumid(albumid,connection):

    html_text = BaseData.get_songsjson(albumid)
    #因为歌曲信息抓取下来不是Json数据，所以需要用BeautifulSoup进行提取

    #网页解析
    soup = BeautifulSoup(html_text, 'html.parser')
    body = soup.body
    songs = body.find('div', class_="n-songtb").find_all('li')  # 获取专辑的所有音乐

    i = 1
    totalcount = len(songs)

    for song in songs:

        song = song.a
        song_id = song['href'].replace('/song?id=', '')#歌曲id
        song_name = song.string#歌曲名称

        # 将歌曲信息保存至数据库
        sql.save_song(song_id, song_name,albumid, connection)

        #根据歌曲id获取并保存热门评论相关信息
        get_comments_bysong.get_hot_comments(song_id,connection)

        #根据歌曲id获取并保存普通评论相关信息(限制前3页的评论)
        get_comments_bysong.get_all_comments(song_id,True,3,connection)

        # 汇报进度
        print('歌曲id为:%s 歌曲名称为:%s 进度显示:%d / %d' % (song_id, song_name, i, totalcount))
        i = i + 1


if __name__ == "__main__":

    # 开辟一个线程
    connection1 = pymysql.connect(host='localhost',
                                  user='root',
                                  password='wyhhsh1993',
                                  db='NetEase_Music',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
    artistid = input("请输入你想抓取的专辑的id:<例如周杰伦的床边故事的id为34720827>")
    print ('开始抓取专辑中歌曲的信息……')
    t1 = threading.Thread(target=get_songs_byalbumid, args=(str(artistid), connection1))
    t1.start()


