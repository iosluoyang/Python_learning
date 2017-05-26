# -*- coding:utf-8 -*-
import config
import re
import sys
from get_recommends import deal_recommends_infos

reload(sys)
sys.setdefaultencoding("utf-8")


# 对某一个商品详情链接进行爬取，其中包括解析链接和存储相应数据
def scrap(url):
    deal_recommends_infos(url)


# 从存储商品详情的URL文件中开始抓取
def from_file():
    # 打开浏览器
    driver = config.DRIVER
    # 跳转淘宝首页
    driver.get(config.LOGIN_URL)
    print u'在浏览器中完成登录之后，请输入任意键，开始执行爬取'
    # 等待用户登录之后的操作提示
    raw_input()
    # 加载URL合集文件中的所有urls
    urls = get_urls()
    # 赋值给配置文件中的所有URL数量
    config.TOTAL_URLS_COUNT = len(urls)
    print u'共有', config.TOTAL_URLS_COUNT, u'个链接'
    # 获取链接url计数文件中的数量，如果文件不存在或者数量为0则都返回0
    count = int(get_urlindex_count())
    print u'上次爬取到第', int(count) + 1, u'个链接, 继续爬取'
    print u'输入 1 继续爬取,输入 2 重新爬取:'
    num = raw_input()
    # 重新爬取
    if num == '2':
        count = 0
        print u'开始重新爬取……'

    # 如果小于最后一个链接的索引数
    if count < config.TOTAL_URLS_COUNT:
        # 通过差值算出共需爬取多少个链接
        tempcount = config.TOTAL_URLS_COUNT - count

        for count in range(count, config.TOTAL_URLS_COUNT):
            write_urlindex_count(count, config.COUNT_TXT)
            url = urls[count]
            print u'正在爬取第', count + 1, u'个网页, 共需要爬取:', tempcount, u'个'
            # 设置配置文件当前爬取的链接索引
            config.NOW_URL_COUNT = count

            # 开始爬取商品详情页的url,其中包含解析和存储到文件中
            scrap(url)
            count = count + 1
            print u'当前已完成采集', config.NOW_URL_COUNT + 1, u'个, 共', tempcount, u'个'
        print u'采集结束,本次共完成了', tempcount, u'个链接的采集'
    else:
        print u'链接上次已经全部爬取完毕'


# 从本地URL集合文件中获取URL数组返回
def get_urls():
    try:
        file = open(config.URLS_FILE, 'r')
        content = file.read()
        # 使用正则匹配所有的链接地址,然后返回为集合
        pattern = re.compile(r'(.*?//.*?)\s', re.S)
        urls = re.findall(pattern, content)
        return urls

    except Exception, e:
        print u'从URL集合文件中获取URL集合失败', e.message


# 从本地存储URL数量的文本中读取需要爬取的链接个数
def get_urlindex_count():
    try:
        with open(config.COUNT_TXT, 'r') as f:
            page = f.read()
            if not page:
                return 0
            else:
                return page
    except Exception:
        print '不存在计数文件，可从开头开始抓取'
        return 0


# 将链接的索引写入存储URL数量的文本中
def write_urlindex_count(count, file):
    try:
        with open(file, 'w') as f:
            f.write(str(count))
            f.close()
    except TypeError:
        print u'链接索引写入失败'


from_file()







