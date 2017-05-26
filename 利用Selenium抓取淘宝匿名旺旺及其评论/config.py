# -*- coding:utf-8 -*-
from selenium import webdriver

URLS_FILE = '/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/利用Selenium抓取淘宝匿名旺旺及其评论/file/抓取的urls.txt'

OUT_FILE = '/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/利用Selenium抓取淘宝匿名旺旺及其评论/file/抓取的匿名用户评论.xls'

COUNT_TXT = '/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/利用Selenium抓取淘宝匿名旺旺及其评论/file/记录抓取链接进度.txt'

DRIVER = webdriver.Chrome()

TIMEOUT = 30

MAX_SCROLL_TIME = 5

TOTAL_URLS_COUNT = 0

NOW_URL_COUNT = 0

LOGIN_URL = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.50862.754894437.1.MVF6jc&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F'

SEARCH_LINK = 'https://www.tmall.com/?spm=a220m.1000858.a2226n0.1.kM59nz'

CONTENT = ''

PAGE = 1

FILTER_SHOP = False
FILTER_USER = False

ANONYMOUS_STR = '***'
