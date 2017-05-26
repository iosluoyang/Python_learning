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
import get_songs_byalbum




# 抓取歌手专辑集合 (限制前多少页的专辑信息)
def get_album_byartistid(artistid,limitnum,connection):

    html_text = BaseData.get_ablumsjson(artistid,limitnum)
    #因为专辑信息抓取下来不是Json数据，所以需要用BeautifulSoup进行提取

    #网页解析
    soup = BeautifulSoup(html_text, 'html.parser')
    body = soup.body
    albums = body.find_all('a', attrs={'class': 'tit s-fc0'})  # 获取所有专辑

    i = 1
    totalcount = len(albums)

    for album in albums:
        albume_id = album['href'].replace("/album?id=", '')

        if type(album.string) == bs4.element.NavigableString:
            albume_name = album.string

            #将专辑信息保存至数据库
            sql.save_album(albume_id, albume_name,artistid, connection)

            #根据专辑id获取并保存相应歌曲信息
            get_songs_byalbum.get_songs_byalbumid(albume_id,connection)

            #汇报进度
            print('专辑id为:%s 专辑名称为:%s 进度显示:%d / %d' %(albume_id,albume_name,i,totalcount))
            i = i + 1



if __name__ == "__main__":

    # 开辟一个线程
    connection1 = pymysql.connect(host='localhost',
                                  user='root',
                                  password='wyhhsh1993',
                                  db='NetEase_Music',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
    artistid = input("请输入你想抓取的歌手的id:<例如周杰伦为6452,五月天为13193>")
    ifmaxnum = input("是否限制抓取的数量(限制输入1 不限制输入0,不限制默认抓取前200张专辑)")
    if (int(ifmaxnum) == 1):
        #限制数量
        maxnum = input("你想要抓取多少张专辑？直接输入数字就好~~")
        print('你的目标是抓取%d个专辑的信息' % int(maxnum))
        print ('开始抓取……')

        t0 = threading.Thread(target=get_album_byartistid, args=(str(artistid),int(maxnum),connection1))
        t0.start()

    else:
        #不限制数量
        print ('开始抓取所有专辑的信息……')
        t1 = threading.Thread(target=get_album_byartistid, args=(str(artistid),200,connection1))
        t1.start()

