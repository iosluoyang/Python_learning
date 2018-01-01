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



def get_htmlcontent_by_offset(artistid,offset):

    html_text = BaseData.get_ablumsjson(artistid, offset)

    # 因为专辑信息抓取下来不是Json数据，所以需要用BeautifulSoup进行提取
    soup = BeautifulSoup(html_text, 'html.parser')
    body = soup.body
    #f返回该页的HTML内容
    return body



def get_album_byartistid(artistid):

    allalbumsArr = [] #所有的专辑信息合集数组

    #offset代表页码数,所有歌手的专辑信息均从0开始,然后在第0页中的页码数据中提取出来所有的offset再接着进行遍历爬取即可
    html_text = get_htmlcontent_by_offset(artistid,0)
    #根据该页的页码数返回该歌手所有专辑的总共页码数,然后从2开始遍历即可
    allpage = int(html_text.select('div.u-page > a')[-2].text)  #找到倒数第二个a的页码数即为最大的页码值 (最后一个是下一页的字样)

    albums = html_text.select('#m-song-module')[0].select('li')
    allalbumsArr.extend(albums)  # 将第0页数据先加入到数组中

    #从第2页开始抓取(不包含最后一页)
    for page in range(1,allpage):

        newoffset = str(page * 12)
        html_text = get_htmlcontent_by_offset(artistid, newoffset)
        albums = html_text.select('#m-song-module')[0].select('li')
        allalbumsArr.extend(albums)  # 将每一页的数据加入到数组中

    #解析每一张专辑
    for i,albumli in enumerate(allalbumsArr):
        #专辑id
        albumId = albumli.select("div.u-cover a.msk")[0]["href"].replace("/album?id=", '')

        # 专辑名称
        albumcoverName = albumli.select("div.u-cover")[0]['title']


        #专辑发布时间
        albumTime = albumli.select("span.s-fc3")[0].text

        # 专辑封面图片地址
        albumcoverUrl = albumli.select("div.u-cover img")[0]['src']


        # 将专辑信息保存至数据库
        sql.save_album(albumId, albumcoverName,albumTime,albumcoverUrl,artistid)

        # 根据专辑id获取并保存相应歌曲信息
        get_songs_byalbum.get_songs_byalbumid(albumId)

        # 汇报进度
        i += 1
        print('专辑id为:%s 专辑名称为:%s 专辑封面链接为:%s 专辑发布时间为:%s 该专辑所属的歌手的id为:%s 进度显示:%d / %d' % (albumId , albumcoverName , albumcoverUrl , albumTime , artistid , i ,len(allalbumsArr)))



if __name__ == "__main__":

    artistid = input("请输入你想抓取的歌手的id:<例如周杰伦为6452,五月天为13193>")
    print ('开始抓取该歌手所有专辑的信息……')
    t1 = threading.Thread(target=get_album_byartistid, args=(str(artistid),))
    t1.start()


