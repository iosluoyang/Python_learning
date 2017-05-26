# -*- coding:utf-8 -*-
from get_recommends import deal_recommends_infos


# 根据输入的商品详情链接直接进行抓取和解析并不保存相应数据
def from_input():
    print u'请输入宝贝链接:'
    url = raw_input()
    driver = config.DRIVER
    driver.get(config.LOGIN_URL)
    print u'完成登录之后，请输入任意键，开始执行爬取'
    raw_input()
    scrap(url)
    print u'采集结束'

def scrap(url):
    deal_recommends_infos(url)

from_input()
