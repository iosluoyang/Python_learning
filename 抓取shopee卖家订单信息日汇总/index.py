#coding:utf8

from selenium import  webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

import json

shopeeaccount = '0955511464'
shopeepwd = 'N3184520eung'


# 添加谷歌浏览器的启动配置

# 启动谷歌浏览器
driver = webdriver.Chrome()

# 再增加cookies前要先进行一次访问
# 访问shopee卖家中心登录页 https://seller.th.shopee.cn/account/signin
driver.get('https://seller.th.shopee.cn')

# 然后再增加cookies
driver.delete_all_cookies()
dict_cookies = {}
with open('/Users/HelloWorld/Desktop/login-shopeecookies.json','r') as f:
    list_cookies = json.loads(f.read())

for i in list_cookies:
    driver.add_cookie(i)

driver.get('https://seller.th.shopee.cn')

try:
    myorderlinkitem = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.app-container .sidebar-container .sidebar-fixed .sidebar-menu .sidebar-menu-box:nth-child(2) .sidebar-submenu .sidebar-submenu-item:nth-child(1) a'))
    )
except ValueError as e:
    print ('定位我的订单元素失败' + e)

finally:
    print (myorderlinkitem)

# 点击我的订单区域
myorderlinkitem.click()

# 选择要发货的tab并点击
try:
    readytodeliveryitem = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.app-main-panel .order-list .shopee-fixed-top-card .fixed-container .portal-panel .shopee-tabs .shopee-tabs__nav .shopee-tabs__nav-warp .shopee-tabs__nav-tabs .shopee-tabs__nav-tab:nth-child(4)'))
    )
except ValueError as e:
    print ('定位即将发货元素失败' + e)

finally:
    print (readytodeliveryitem)

readytodeliveryitem.click()

# 休眠3秒钟
sleep(10)

# # 选择订单过滤时间选择器 设置为当前时间
# try:
#     dateselector = WebDriverWait(driver, 100).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.order-search-panel .order-export .shopee-date-picker'))
#     )
# except ValueError as e:
#     print ('定位日期选择器元素失败' + e)
#
# finally:
#     print (dateselector)
#
# dateselector.click()
#
# # 选择当前的日期进行点击
# try:
#     currentdateitem = WebDriverWait(driver, 100).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.shopee-daterange-picker-panel .shopee-daterange-picker-panel__body-right .shopee-date-table__cell.current'))
#     )
# except ValueError as e:
#     print ('定位当前日期元素失败' + e)
#
# finally:
#     print (currentdateitem)
#
# # 双击当前日期两次选择当前的日期
# ActionChains(driver).move_to_element(currentdateitem).double_click(currentdateitem).perform()
#
# # 点击确定按钮进行筛选
# searchbtn = driver.find_element_by_css_selector('.order-search-panel .order-export .report-export .latest button.export')
# print (searchbtn)
#
# searchbtn.click()

# 获取当前页面的订单列表信息
try:
    orderlistels = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.new-order-list .order-list-pannel .order-list-section .order-list-body a.order-item'))
    )
except ValueError as e:
    print ('获取订单信息元素失败' + e)

finally:
    print (orderlistels)

# 遍历订单列表 获取订单相关信息
for eachorderitemel in orderlistels:
    print eachorderitemel
    print eachorderitemel.get_attribute('href')



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





# 选择日期组件
# pickerelement = driver.find_element_by_css_selector('.order-search-pannel .order-export .shopee-date-picker')
# pickerelement.click()

