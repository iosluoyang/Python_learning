#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='wyhhsh1993',
                             db='NetEase_Music',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



# 保存热门歌手的信息   artist_id 歌手id artist_name 歌手名字   albumSize 歌手专辑总数量   musicSize 歌曲总数量 picUrl 歌手头像 img1v1Url 歌手头像(正方形头像)
def save_hot_artist(artist_id, artist_name,albumSize,musicSize,picUrl,img1v1Url):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `hotartists` (`artist_id`, `artist_name`, `album_size`, `song_size`, `artist_pic`, `artist_pic1v1`) VALUES (%s, %s,%s,%s, %s,%s)"
        cursor.execute(sql, (artist_id, artist_name,albumSize, musicSize , picUrl,img1v1Url))
    connection.commit()


# 保存专辑的基本信息 albumId 专辑ID albumcoverName 专辑名称 albumTime 专辑发布时间 albumcoverUrl 专辑封面图片URL artistid 该专辑所从属的歌手ID
def save_album(albumId, albumcoverName,albumTime,albumcoverUrl,artistid):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `albums` (`album_id`, `album_coverame`,`album_time`,`album_coverurl`,`artist_id`) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (albumId, albumcoverName,albumTime,albumcoverUrl,artistid))
    connection.commit()


# 保存专辑的简要信息和详细信息 album_id专辑id simpledes简要描述信息 moredes 详细描述信息
def save_des_album(album_id,simpledes, moredes):
    with connection.cursor() as cursor:
        sql = 'update albums set album_simpledes = %s,album_moredes = %s where album_id = %s'
        cursor.execute(sql, (simpledes, moredes,album_id))
    connection.commit()


# 保存歌曲的信息 song_id 歌曲id, song_name 歌曲名称  ,album_id 歌曲所属专辑id
def save_song(song_id, song_name,album_id):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `songs` (`song_id`, `song_name`,`album_id`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (song_id, song_name,album_id))
    connection.commit()




# 保存歌曲详情的热门评论 song_id 歌曲ID userID 评论人Id nickname 评论人昵称 avatarUrl 评论人头像地址 comment_time 评论时间 likedCount 点赞数 comment 评论内容commentId 评论Id
def save_hotcomments_by_a_song(song_id,userID,nickname,avatarUrl,comment_time,likedCount,comment,commentId):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `hotcomments` (`song_id`,`user_id`,`user_nickname`,`user_avatarurl`,`comment_time`,`comment_likedcount`, `comment_content`,`comment_id`) VALUES (%s, %s, %s,%s, %s, %s,%s,%s)"
        cursor.execute(sql, (song_id, userID, nickname,avatarUrl,comment_time,likedCount,comment,commentId))
    connection.commit()



# 保存歌曲详情的普通评论 song_id 歌曲ID userID 评论人Id nickname 评论人昵称 avatarUrl 评论人头像地址 comment_time 评论时间 likedCount 点赞数 comment 评论内容commentId 评论Id
def save_normalcomments_by_a_song(song_id,userID,nickname,avatarUrl,comment_time,likedCount,comment,commentId):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `normalcomments` (`song_id`,`user_id`,`user_nickname`,`user_avatarurl`,`comment_time`,`comment_likedcount`, `comment_content`,`comment_id`) VALUES (%s, %s, %s,%s, %s, %s,%s,%s)"
        cursor.execute(sql, (song_id, userID, nickname, avatarUrl, comment_time, likedCount, comment, commentId))
    connection.commit()







# 获取所有歌手的 ID
def get_all_artist():
    with connection.cursor() as cursor:
        sql = "SELECT `ARTIST_ID` FROM `artists` ORDER BY ARTIST_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取所有专辑的 ID
def get_all_album():
    with connection.cursor() as cursor:
        sql = "SELECT `ALBUM_ID` FROM `albums` ORDER BY ALBUM_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取所有音乐的 ID
def get_all_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取前一半音乐的 ID
def get_before_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 0, 800000"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取后一半音乐的 ID
def get_after_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 800000, 1197429"
        cursor.execute(sql, ())
        return cursor.fetchall()


def dis_connect():
    connection.close()
