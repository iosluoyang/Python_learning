# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import config
import sys
import locale

reload(sys)
sys.setdefaultencoding("utf-8")

shop_list = []
link_list = []

#获取URL的集合文件
def find_urls():
    print u'请输入要提取链接的关键字'
    keyword = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    
    print u'您要提取的商品名称是', keyword
    print u'正在开始提取...'
    try:
        #清空文件记录的链接
        clear_file()
        #根据关键字获取相应的网页源码
        html = get_results(keyword)
        #分析源码，将该页搜索出来的所有商品详情链接写入到URL集合文件中
        parse_html(html)
        
        for i in range(1, config.PAGE + 1):
            print u'当前第',(i-1), u'页'
            #获取翻页的商品详情链接
            get_more_link()
    except Exception:
        print u'抓取过程出现异常，请检查'

        with open(config.URLS_FILE, 'w') as f:
            f.write(config.CONTENT)
            f.close()
            print u'出现异常，已还原内容'
    finally:
        config.DRIVER.close()
        print u'采集结束, 共采集', len(link_list), u'个链接'

#根据关键字获取网页源码
def get_results(keyword):
    #首先selenium用浏览器打开首页链接
    driver = config.DRIVER
    link = config.SEARCH_LINK
    driver.get(link)
    # 1. 等待页面加载完成(用ID=mq来判断搜索框是否已经出来了)
    try:
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "mq"))
        )
    except TimeoutException:
        print u'加载页面失败'

    # 2. 根据selector = #mq找到搜索框,让用户输入关键字来进行搜索
    try:
        element = driver.find_element_by_css_selector('#mq')
        print u'成功找到了搜索框'
        keyword = keyword.decode('utf-8', 'ignore')
        print keyword
        element.send_keys(keyword)
        element.send_keys(Keys.ENTER)
        print u'正在查询该关键字:',keyword

    except NoSuchElementException:
        print u'没有找到搜索框'

    # 3. 加载网页，根据CSS_SELECTOR = J_ItemList div.productImg-wrap来判断该页面是否加载完毕，返回页面源码
    try:
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_ItemList div.productImg-wrap"))
        )
    except TimeoutException:
        print u'查询失败'

    html = driver.page_source
    return html

#根据页面源码，提取每一个商品的信息，将商品的链接写入URL中
def parse_html(html):
    doc = pq(html)
    #得到所有商品的集合数组
    products = doc('#J_ItemList .product').items()
    
    for product in products:
        #提取每一个商品的店铺名称和商品图片
        shop = product.find('.productShop-name').text()
        href = product.find('.productImg').attr('href')
        if shop and href:
            #是否筛选相同店铺的商品,如果筛选，则只有当没有相同店铺时才写入商品详情链接，否则不进行判断，直接写入
            if config.FILTER_SHOP:
                if not shop in shop_list:
                    href = 'https:' + href
                    print shop, href
                    shop_list.append(shop)
                    link_list.append(href)
                    write_file(href)
                    print u'当前已采集', len(shop_list), u'个链接'
                else:
                    print u'店铺', shop, u'已经存在,该商品不会写入文件当中'
            else:
                shop_list.append(shop)
                href = 'https:' + href
                link_list.append(href)
                write_file(href)
                print u'当前已采集', len(shop_list), u'个链接'

#模拟翻页操作,根据页面源码，提取每一个商品的信息，将商品的链接写入URL中
def get_more_link():
    print u'正在采集下一页的宝贝链接'
    driver = config.DRIVER
    
    #使用JS动效模拟页面下拉的操作
    try:
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
    except WebDriverException:
        print u'页面下拉失败'
    

    #获取翻页的控件，模拟点击
    try:
        next = driver.find_element_by_css_selector('#content b.ui-page-num > a.ui-page-next')
        next.click()

    except NoSuchElementException:
        print u'未找到翻页按钮'

    except:
        print  u'未能成功点击翻页按钮'


    #隐式等待，等待5秒钟
    driver.implicitly_wait(5)

    #显式等待，和之前加载的一样，等待商品数据加载完成出来
    try:
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_ItemList div.productImg-wrap"))
        )
    except TimeoutException:
        print u'查询失败'

    #获取该页的网页源码
    html = driver.page_source

    #根据搜索出来的页面源码，提取每一个商品的信息，将商品的链接写入URL中
    parse_html(html)

#将商品详情的链接写入文件中
def write_file(href):
    try:
        with open(config.URLS_FILE, 'a') as f:
            f.write(href + '\n')
            f.close()
    except Exception:
        print u'写入失败'

#清空记录商品详情页链接的文件
def clear_file():
    try:
        with open(config.URLS_FILE, 'r') as f:
            print u'正在清空爬取链接，等待重新爬取新链接……'
            config.CONTENT = f.read()
            print u'已经将上次保存的数据设置为配置文件中的内容作为备份'
            f.close()
        with open(config.URLS_FILE, 'w') as f:
            f.write('')
            f.close()
            print u'已经将旧链接清空掉，现在可以爬取新链接'
    except Exception:
        print u'清空链接失败'


find_urls()