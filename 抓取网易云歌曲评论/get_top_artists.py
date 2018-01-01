# -*- coding: utf-8 -*-
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import BaseData
import json
import sql
import threading
import pymysql
import get_albums_byartist



# 抓取热门歌手集合 (限制前多少页的歌手信息)
def get_all_artists(limitpagenum):
    for page in range(limitpagenum):
        json_text = BaseData.get_hotartistsjson(page + 1)
        json_dict = json.loads(json_text)

        artistslist = json_dict['artists']

        # 开始抓取歌手信息
        for i in range(len(artistslist)):
            item = artistslist[i]

            id = item['id']  # 歌手id
            name = item['name']  # 歌手名字
            albumSize = item['albumSize']  # 歌手专辑总数量
            musicSize = item['musicSize'] #歌曲总数量
            picUrl = item['picUrl']  # 歌手头像
            img1v1Url = item['img1v1Url']  # 歌手头像(正方形头像)

            # 将歌手信息数据保存到数据库中
            sql.save_hot_artist(id, name, albumSize,musicSize, picUrl, img1v1Url)
            #根据歌手id获取并保存相应专辑信息:
            get_albums_byartist.get_album_byartistid(id)


            #汇报进度:
            print ('%s的id是:%s 有%s张专辑 有%s首歌曲 进度显示:(%d / %d)' % (name, id, albumSize , musicSize , 20*page + (i+1) , 20 *limitpagenum ))




if __name__ == "__main__":


    ifmaxnum = input("是否限制抓取的数量(限制输入1,在1~5范围内进行选择  不限制输入0,默认抓取前5页歌手,即前100位歌手)")
    if (int(ifmaxnum) == 1):
        #限制数量
        maxpagenum = input("你想要抓取多少页的歌手？直接输入数字就好(在1~5中选择哦)~~ ,一页有20个")
        print('你的目标是抓取%d个歌手的信息' % (int(maxpagenum) * 20))
        print ('开始抓取……')

        t0 = threading.Thread(target=get_all_artists, args=(int(maxpagenum),))
        t0.start()

    else:
        #不限制数量
        print('你没有告诉我要抓取多少页的歌手信息,那么我就斗胆猜测一下,你想要100个歌手对吧~~')
        print ('开始抓取100位歌手的信息……')

        t1 = threading.Thread(target=get_all_artists, args=(5,))
        t1.start()

