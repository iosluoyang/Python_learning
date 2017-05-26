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



# 保存热门歌手的信息
def save_hot_artist(artist_id, artist_name,albumSize,picUrl,img1v1Url,connection):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `Hot_Artists` (`ARTIST_ID`, `ARTIST_NAME`, `ALBUM_SIZE`, `PICURL`, `IMG1V1URL`) VALUES (%s, %s,%s, %s,%s)"
        cursor.execute(sql, (artist_id, artist_name,albumSize,picUrl,img1v1Url))
    connection.commit()


# 保存专辑的信息
def save_album(album_id, album_name,artist_id,connection):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `Albums` (`ALBUM_ID`, `ALBUM_NAME`,`ARTIST_ID`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (album_id, album_name,artist_id))
    connection.commit()

# 保存歌曲的信息
def save_song(song_id, song_name,album_id,connection):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `Songs` (`SONG_ID`, `SONG_NAME`,`ALBUM_ID`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (song_id, song_name,album_id))
    connection.commit()




# 保存歌曲详情的热门评论
def save_hotcomments_by_a_song(song_id,userID,nickname,avatarUrl,comment_time,likedCount,comment, connection):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `HotComments` (`SONG_ID`,`USER_ID`,`NICKNAME`,`AVATARURL`,`COMMENT_TIME`,`LIKEDCOUNT`, `COMMENTSSTR`) VALUES (%s, %s, %s,%s, %s, %s,%s)"
        cursor.execute(sql, (song_id, userID, nickname,avatarUrl,comment_time,likedCount,comment))
    connection.commit()



# 保存歌曲详情的所有评论
def save_comments_by_a_song(song_id,userID,nickname,avatarUrl,comment_time,likedCount,comment, connection):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `Comments` (`SONG_ID`,`USER_ID`,`NICKNAME`,`AVATARURL`,`COMMENT_TIME`,`LIKEDCOUNT`, `COMMENTSSTR`) VALUES (%s, %s, %s,%s, %s, %s,%s)"
        cursor.execute(sql, (song_id, userID, nickname,avatarUrl,comment_time,likedCount,comment))
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
