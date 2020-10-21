#coding:utf8

from selenium import  webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


from time import sleep

import json

shopeeaccount = '0955511464'
shopeepwd = 'N3184520eung'

driver = None
logincookiesPath = '/Users/HelloWorld/Desktop/login-shopeecookies.json'
# targetUrl = 'https://seller.th.shopee.cn'
targetUrl = 'https://seller.th.shopee.cn/portal/sale?type=shipping'


# 打开链接
def opentargetUrl():

    driver = webdriver.Chrome()

    # 添加谷歌浏览器的启动配置

    # 再增加cookies前要先进行一次访问
    # 访问shopee卖家中心登录页 https://seller.th.shopee.cn/account/signin
    driver.get(targetUrl)

    # 然后再增加cookies
    driver.delete_all_cookies()
    dict_cookies = {}
    with open(logincookiesPath, 'r') as f:
        list_cookies = json.loads(f.read())

    for i in list_cookies:
        driver.add_cookie(i)

    driver.get(targetUrl)

# 操作跳转目标页面
def getallOrders():

    # # 获取我的订单元素并点击
    # try:
    #     myorderlinkitem = WebDriverWait(driver, 100).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR,
    #         '.app-container .sidebar-container .sidebar-fixed .sidebar-menu .sidebar-menu-box:nth-child(2) .sidebar-submenu .sidebar-submenu-item:nth-child(1) a'))
    #     )
    #     myorderlinkitem.click()
    # except ValueError as e:
    #     print ('定位我的订单元素失败' + e)
    #
    # finally:
    #     print ('获取我的订单元素:')
    #     print (myorderlinkitem)
    #
    # # 获取即将发货的tab并点击
    # try:
    #     readytodeliveryitem = WebDriverWait(driver, 100).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR,
    #         '.app-main-panel .order-list .shopee-fixed-top-card .fixed-container .portal-panel .shopee-tabs .shopee-tabs__nav .shopee-tabs__nav-warp .shopee-tabs__nav-tabs .shopee-tabs__nav-tab:nth-child(4)'))
    #     )
    #     readytodeliveryitem.click()
    # except ValueError as e:
    #     print ('定位即将发货元素失败' + e)
    #
    # finally:
    #     print ('获取即将发货元素:')
    #     print (readytodeliveryitem)
    #
    #
    #

    # 直到页面有分页器则说明数据加载完毕了

    try:
        paginationel =  WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            '.new-order-list .order-list-pannel .order-list-section .pagination-bottom'))
        )
    except ValueError as e:
        print ('获取分页元素失败' + e)

    finally:
        print ('获取分页元素:')
        print (paginationel)

    # 所有的订单元素集合
    allorderArr = []

    # 获取总共有几页
    totalPages = paginationel.find_elements_by_css_selector('ul.shopee-pager__pages li.shopee-pager__page')
    for (pageindex, eachpageel) in enumerate(totalPages):

        # 每一页的订单列表数据
        orderlistels = []

        # 超过一页的情况下将页面滑到底部
        if(pageindex > 0):

            # 将该页面从上滑到下
            driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
            # 停留1秒钟
            sleep(1)

            # 点击该页的分页元素
            eachpageel.click()

            # 再将页面从下滑到上
            # driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")

            # 直到页面有分页器则说明数据加载完毕了
            try:
                paginationel = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                    '.new-order-list .order-list-pannel .order-list-section .pagination-bottom'))
                )
            except ValueError as e:
                print ('获取分页元素失败' + e)

            finally:
                print ('获取分页元素:')
                print (paginationel)


        # 获取当前页面的订单列表信息
        try:
            orderlistels = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                '.new-order-list .order-list-pannel .order-list-section .order-list-body a.order-item'))
            )

            # 在此将该页数据需要的信息提取出来 否则在后面针对该元素无法进行数据获取

            # 遍历订单列表 获取订单相关信息
            for (index, eachorderitemel) in enumerate(orderlistels):
                # 获取元素对应的订单相关信息

                # 订单号
                orderNum = eachorderitemel.find_element_by_css_selector(
                    '.order-title .orderid'
                ).get_attribute('innerHTML').split(';')[1]

                # print ('该订单的订单号为:{orderNum}'.format(orderNum=orderNum))

                # 物流方式
                shippingWay = eachorderitemel.find_element_by_css_selector(
                    '.order-list-item .carrier-name').text
                # print ('该订单的运送方式为:{shippingWay}'.format(shippingWay=shippingWay))

                # 订单详情链接
                orderLink = eachorderitemel.get_attribute('href')
                # print ('该订单的详情链接为:{orderLink}'.format(orderLink=orderLink))

                orderdata = {
                    "orderNum": orderNum,
                    "shippingWay": shippingWay,
                    "orderLink": orderLink
                }

                allorderArr.append(orderdata)

            print ('获取第{page}/{totalPage}页所有订单信息元素成功'.format(page=pageindex,totalPage=len(totalPages)))


        except ValueError as e:
            print ('获取第{page}页订单信息元素失败'.format(page=pageindex))

    # 获取所有的订单数据完毕
    print ('共计获取了{num}个订单数据'.format(num=len(allorderArr)))
    # print allorderArr

    # 如果对数据进行过滤筛选则在这里进行
    #------------------------------

    # 遍历过滤后的订单数据
    for(orderindex, eachorderdata) in enumerate(allorderArr):
        print ('正在查看第{orderindex}/{totalnum}'.format(orderindex=orderindex+1,totalnum=len(allorderArr)))
        ifopennewwindow = orderindex == 0 # 是否打开新窗口 只有第一个订单才打开

        # 模拟只获取第一个订单数据
        if orderindex == 0:
            gotoorderdetailPage(eachorderdata['orderLink'], ifopennewwindow)

# 打开每一个订单信息
def gotoorderdetailPage(link, ifopennewwindow):

    # 根据是否需要打开新窗口来做不同情况的处理

    # 需要打开新窗口
    if ifopennewwindow:

        js = 'window.open("' + link + '");'
        driver.execute_script(js)

        # 输出当前窗口句柄
        current_handle = driver.current_window_handle

        # 获取当前窗口句柄集合（列表类型）
        handles = driver.window_handles
        # print(handles)  # 输出句柄集合

        # 获取新窗口的句柄
        orderdetail_handle = None
        for handle in handles:
            if handle != current_handle:
                orderdetail_handle = handle
                break

        # 输出当前窗口句柄（订单详情窗口）
        # print('switch to ', orderdetail_handle)
        # 切换到订单详情页的窗口中
        driver.switch_to.window(orderdetail_handle)

    # 不需要打开新窗口
    driver.get(link)

    # 开始获取订单详情页的内容
    try:
        orderDetailel = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,''
                '.fulfillment-order .order-detail'
            ))
        )
    except ValueError as e:
        print ('获取订单详情元素失败' + e)

    finally:
        print ('获取到订单详情元素:')
        # print (orderDetailel)
        # 将该页面从上滑到下
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        # 等待1秒
        sleep(1)



    # 获取订单详情数据的元素内容
    detailHtml = orderDetailel.get_attribute('innerHTML')

    # 进行订单数据的获取
    ordertailsoup = BeautifulSoup(detailHtml,'lxml').prettify()
    print ordertailsoup

    # driver.close()  # 关闭当前窗口（订单详情）

    # 切换回主页窗口
    # driver.switch_to.window(current_handle)



# 获取订单详情数据
def getOrderDetailData(htmlcontent):

    # 加载模拟数据
    with open('/Users/HelloWorld/Desktop/htmlcontentDemo.html', 'r') as f:
        htmlcontent = f.read()





# try:
#     signinform = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.signin .signin-form'))
#     )
# except ValueError as e:
#     print ('错误原因为:' + e)
#
# # 定位登录输入框
# inputelements = driver.find_elements_by_css_selector('.signin .signin-form .shopee-form-item .shopee-form-item__control .shopee-input input')
#
# # 账号输入框
# accountel = inputelements[0]
# pwdel = inputelements[1]
#
# # 键入账号密码
# accountel.send_keys(shopeeaccount)
# pwdel.send_keys(shopeepwd)
#
# # 点击记住密码
# rememberel = driver.find_element_by_css_selector('.signin-form .remember .shopee-checkbox').click()

# 进行登录
# loginbtn = driver.find_element_by_css_selector('.signin-form button.shopee-button').click()

# # 等待直到页面进入主页面然后获取cookies
# sidebarelement = WebDriverWait(driver, 100).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.sidebar-container'))
# )
#
# # 获取cookies
# cookies = driver.get_cookies()
#
# # 将获取到的cookies序列化保存到本地
# cookiesdict = json.dumps(cookies)
#
# with open('/Users/HelloWorld/Desktop/login-shopeecookies.json', 'w') as f:
#     f.write(cookiesdict)


if __name__ == "__main__":
   # opentargetUrl() # 打开目标页面
   # getallOrders() # 获取所有订单数据

   # 获取订单详情的相关数据
   getOrderDetailData(None)

