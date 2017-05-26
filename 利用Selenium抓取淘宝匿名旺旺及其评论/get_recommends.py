# -*- coding:utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import sys
from write_to_excel import write_info,repeat_excel

reload(sys)
sys.setdefaultencoding("utf-8")

#单次获取是否加载完成的标识,实现下拉操作，目的是为了让商品推荐的那个模块加载完成之后才好获取其相应的源码
def scroll_bottom_recommends(driver, count):
    print u'正在尝试第', count, u'次下拉'
    try:
        js = "window.scrollTo(0,document.body.scrollHeight-" + str(count * count* 100) + ")"
        driver.execute_script(js)
    except WebDriverException:
        print u'下拉寻找橱窗宝贝时出现问题'
    time.sleep(2)
    try:
        #看了又看模块的标识为 #J_TjWaterfall li
        driver.find_element_by_css_selector('#J_TjWaterfall li')
    except NoSuchElementException:
        return False
    return True

#是否加载完成的标识，首先实现自动下拉功能，最大尝试次数默认为10，目的是确保页面下方的HTML已经完全加载出来了
def is_recommends_appear(driver, max_time=10):
    count = 1
    result = scroll_bottom_recommends(driver, count)
    while not result:
        count = count + 1
        result = scroll_bottom_recommends(driver, count)
        if count == max_time:
            return False
    return True


#根据商品详情链接返回该商品详情的HTML源码(其中包含多次下拉页面以确定页面加载完成,HTML源码完整)
def scrap_recommends_page(url):
    print u'开始寻找下方橱窗推荐宝贝', url
    driver = config.DRIVER
    timeout = config.TIMEOUT
    max_scroll_time = config.MAX_SCROLL_TIME
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "J_TabBarBox"))
        )
    except TimeoutException:
        return False

    if is_recommends_appear(driver, max_scroll_time):
        print u'已经成功加载出下方橱窗推荐宝贝信息'
        return driver.page_source
    else:
        return False


def get_recommends_infos(url):
    info = []
    if not url.startswith('http'):
        url = 'https:' + url
    #获取加载完成之后的页面源码
    html = scrap_recommends_page(url)
    if html:
        doc = pq(html)
        #根据特定的标识获取到每一个评论,标识为#J_TjWaterfall > li
        items = doc('#J_TjWaterfall > li')
        print u'分析得到下方宝贝中的用户评论:'
        for item in items.items():
            url = item.find('a').attr('href')
            if not url.startswith('http'):
                url = 'https:' + url
            comments_info = []
            comments = item.find('p').items()
            for comment in comments:
                #评论的人
                comment_user = comment.find('b').remove().text()
                #评论的内容
                comment_content = comment.text()
                
                anonymous_str = config.ANONYMOUS_STR#***
                #将评论内容和评论人写入数组当中
                comments_info.append((comment_content, comment_user))
                    #for循环结束之后将链接和评论数组加入到info中返回
            info.append({'url': url, 'comments_info': comments_info})
                #info为该商品的链接以及该商品下面所有相关商品的评论（人和内容）
        return info
    else:
        print u'抓取网页失败，跳过'
        return []




#对某一商品详情进行抓取解析和保存数据
def deal_recommends_infos(url):
    #infos为某一商品的链接以及该商品底下所有的评论内容
    infos = get_recommends_infos(url)
    for info in infos:
        url = info.get('url')
        comments_info = info.get('comments_info')
        for comment_info in comments_info:
            comment_content = comment_info[0]
            comment_user = comment_info[1]
            print 'comment_user', comment_user
            #如果数组中有值并且评论人在excel中不存在，则将其评论人，评论内容以及对应的商品链接写入到文件中
            if len(comments_info) > 0 and not repeat_excel(comment_user):
                write_info((comment_user, comment_content, url))




