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
import re
import json
import xlwt
from datetime import datetime

shopeeaccount = '0955511464'
shopeepwd = 'N3184520eung'

stopOrderNum = ''
excelFileKeyArr = ['orderNum','buyerName','shippingWay','productList','totalCommissionFee','totalShippingFee','totalOrderPrice','totalCost']

driver = None
logincookiesPath = '/Users/HelloWorld/Desktop/login-shopeecookies.json'
# targetUrl = 'https://seller.th.shopee.cn'
targetUrl = 'https://seller.th.shopee.cn/portal/sale?type=shipping'


# 打开链接
def opentargetUrl():

    global driver #注意这里的driver要进行全局变量的声明
    driver = webdriver.Chrome()

    # 添加谷歌浏览器的启动配置

    # 再增加cookies前要先进行一次访问
    # 访问shopee卖家中心登录页 https://seller.th.shopee.cn/account/signin
    driver.get(targetUrl)

    # 然后再增加cookies
    driver.delete_all_cookies()
    with open(logincookiesPath, 'r') as f:
        list_cookies = json.loads(f.read())

    for i in list_cookies:
        driver.add_cookie(i)

    driver.get(targetUrl)


# 获取所有的订单列表
def getallorderList():

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
        print ('获取到分页元素:')
        print (paginationel)


    # 所有的订单元素集合
    allorderListArr = []

    # 获取总共有几页
    totalPages = paginationel.find_elements_by_css_selector('ul.shopee-pager__pages li.shopee-pager__page')
    for (pageindex, eachpageel) in enumerate(totalPages):

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
                ).get_attribute('innerHTML').split(';')[1].encode("utf-8")
                # print ('该订单的订单号为:{orderNum}'.format(orderNum=orderNum))

                # 买家名称
                buyerName = eachorderitemel.find_element_by_css_selector(
                    '.order-title .title-prefix .user-header .username'
                ).text.encode("utf-8")
                # print ('该订单的买家名称为:{buyerName}'.format(buyerName=buyerName))

                # 物流方式
                shippingWay = eachorderitemel.find_element_by_css_selector(
                    '.order-list-item .carrier-name'
                ).text.encode("utf-8")
                # print ('该订单的运送方式为:{shippingWay}'.format(shippingWay=shippingWay))

                # 订单详情链接
                orderLink = eachorderitemel.get_attribute('href').encode("utf-8")
                # print ('该订单的详情链接为:{orderLink}'.format(orderLink=orderLink))

                orderdata = {
                    "orderNum": orderNum,
                    "buyerName": buyerName,
                    "shippingWay": shippingWay,
                    "orderLink": orderLink
                }

                allorderListArr.append(orderdata)

            print ('获取第{page}/{totalPage}页所有订单信息元素成功'.format(page=pageindex+1,totalPage=len(totalPages)))


        except ValueError as e:
            print ('获取第{page}页订单信息元素失败'.format(page=pageindex+1))

    sleep(1)
    # 获取完之后点击回到第一页
    firstPaginationel = paginationel.find_elements_by_css_selector('ul.shopee-pager__pages li.shopee-pager__page')[0]
    firstPaginationel.click()
    # 然后滚动到最顶部
    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")


    # 获取所有的订单数据完毕
    print ('共计获取了{num}个订单数据'.format(num=len(allorderListArr)))
    # print allorderListArr

    # print json.dumps(allorderListArr, sort_keys=True, indent=2)

    # 等待用户输入即将截断的订单号
    global stopOrderNum
    stopOrderNum = raw_input('Please enter the Order Number you want to collect to:\n')

    # 如果对数据进行过滤筛选则在这里进行
    #------------------------------

    # 例如获取前3个订单集合或者获取第一个特定的物流公司的订单
    # 判断是否有停止采集的订单号 如果有的话则取该订单号之前的订单集合 否则不进行过滤 默认所有订单
    filterAllOrderListArr = []
    if stopOrderNum is not None:
        for eachorder in allorderListArr:
            filterAllOrderListArr.append(eachorder)
            if(stopOrderNum in eachorder['orderNum']):
                break

    else:
        filterAllOrderListArr = allorderListArr

    # 将过滤后的订单列表数据返回
    print ('开始查看{num}个订单数据'.format(num=len(filterAllOrderListArr)))
    return  filterAllOrderListArr


# 根据订单列表数据获取对应的订单详情数据的集合
def getOrderInfoListbyOrderList(orderList):

    orderInfoList = []

    ifopennewwindow = True  # 是否打开新窗口 默认为true

    # 遍历订单列表
    for (orderindex, eachorderdata) in enumerate(orderList):


        try:
            # 获取订单详情页面内容
            orderDetailHtml = getOrderDetailPageContent(eachorderdata['orderLink'], ifopennewwindow)

            ifopennewwindow = False  # 将是否打开新的浏览器设置为false

            # 解析详情页面内容获取对应的数据
            orderInfo = getOrderInfo(orderDetailHtml)

            orderInfoList.append(orderInfo)

        except ValueError as e:
            print ('第{orderindex}/{totalnum}个订单查看失败'.format(orderindex=orderindex + 1, totalnum=len(orderList)))

        finally:
            print ('第{orderindex}/{totalnum}个订单查看完成'.format(orderindex=orderindex + 1, totalnum=len(orderList)))


    print '获取到的订单详情列表数据为:'
    print json.dumps(orderInfoList)

    return orderInfoList


# 获取订单详情页面内容
def getOrderDetailPageContent(link, ifopennewwindow):

    # 根据是否需要打开新窗口来做不同情况的处理
    global driver

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
    else:
        driver.get(link)

    # 开始获取订单详情页的内容
    try:
        productListel = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,''
                '.fulfillment-order .order-detail .product-list'
            ))
        )
    except ValueError as e:
        print ('获取订单详情商品列表元素失败' + e)

    finally:
        print ('获取到订单详情商品列表元素:')
        # print (productListel)
        # 将该页面从上滑到下
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        # 等待1秒
        sleep(1)


    # 获取订单详情数据的元素内容
    orderDetailel = driver.find_element_by_css_selector('.fulfillment-order .order-detail')
    detailHtml = orderDetailel.get_attribute('innerHTML')

    return detailHtml

    # driver.close()  # 关闭当前窗口（订单详情）

    # 切换回主页窗口
    # driver.switch_to.window(current_handle)


# 获取订单详情数据
def getOrderInfo(htmlcontent):

    soup = BeautifulSoup(htmlcontent, 'lxml')

    # 订单编号
    orderNum = soup.select('.od-shippin .id .detail')[0].text.strip().encode("utf-8")
    # print orderNum

    # 物流方式
    shippingWay = soup.select('.od-shippin .logistic-history-log .carrier')[0].text.strip().encode("utf-8")
    # print shippingWay

    # 买家名称
    buyerName = soup.select('.user-view-item .username')[0].text.strip().encode("utf-8")
    # print buyerName

    # 商品数组对象
    productList = []
    productelList = soup.select('.product-list')[0].select('[class=product-list-item]')
    for eachproduct in productelList:

        # 商品图片
        productImgStr = eachproduct.select('.product-item .product-image')[0].attrs['style']
        productImg = re.findall(r'"(.*?)"', productImgStr)[0]
        # print productImg

        # 商品名称
        productName = eachproduct.select('.product-item .product-detail .product-name')[0].text.strip().encode("utf-8")
        # print productName

        # 商品规格 可能会不存在规格元素
        productSpec = ""

        productSpecEl = eachproduct.select('.product-item .product-detail .product-meta div')
        if productSpecEl is None:
            productSpec = productSpecEl[0].text.strip().split(':')[1].encode("utf-8")
        # print productSpec

        # 商品单价
        productPrice = eachproduct.select('.price')[0].text.strip().encode("utf-8")
        # print productPrice

        # 商品数量
        productAmount = eachproduct.select('.qty')[0].text.strip().encode("utf-8")
        # print productAmount

        # 商品总价
        productTotalPrice = eachproduct.select('.subtotal')[0].text.strip().encode("utf-8")
        # print productTotalPrice

        productInfo = {
            "productImg": productImg,
            "productName": productName,
            "productSpec": productSpec,
            "productPrice": productPrice,
            "productAmount": productAmount,
            "productTotalPrice": productTotalPrice
        }

        productList.append(productInfo)

    # print productList

    # 订单费用相关
    orderPaymentEl = soup.select('.payment-info-details')[0]

    # 订单总成本
    totalCost = orderPaymentEl.select('.income-item.income-subtotal .income-value')[0].text.strip().encode("utf-8")
    totalCost = filter(str.isdigit,totalCost)
    # print totalCost

    # 总运输费用
    totalShippingFee = orderPaymentEl.select('.income-item.income-subtotal .income-value')[1].text.strip().encode("utf-8")
    totalShippingFee = filter(str.isdigit, totalShippingFee)
    # print totalShippingFee

    # 总平台补贴
    totalCommissionFee = orderPaymentEl.select('.income-item.income-subtotal .income-value')[2].text.strip().encode("utf-8")
    totalCommissionFee = filter(str.isdigit, totalCommissionFee)
    # print totalCommissionFee

    # 总实付金额
    totalOrderPrice = orderPaymentEl.select('.income-item.income-subtotal.total .income-value')[0].text.strip().encode("utf-8")
    totalOrderPrice = filter(str.isdigit, totalOrderPrice)
    # print totalOrderPrice

    # 结束订单信息的搜集
    # 开始组装数据

    orderInfo = {

        "orderNum":orderNum, # 订单编号
        "shippingWay": shippingWay, # 物流方式
        "buyerName": buyerName, # 买家名称
        "productList": productList, #订单商品列表
        "totalCost": totalCost, # 订单总成本
        "totalShippingFee": totalShippingFee, # 订单总物流费用
        "totalCommissionFee": totalCommissionFee, # 订单总平台服务费
        "totalOrderPrice": totalOrderPrice, # 订单实付金额

    }

    # print orderInfo

    return orderInfo


# 开始将订单详情列表数据写入excel表格中
def writetoExcelbyOrderInfoList(orderinfolist):

    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet 取当前的日期为sheet名称
    sheetname = 'LAL' + datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    myordersheet = workbook.add_sheet(sheetname, cell_overwrite_ok=True)

    # 表格样式
    headerfont = xlwt.Font()  # 为样式创建字体
    headerfont.name = 'Times New Roman'
    headerfont.bold = True  # 黑体
    headerfont.height = 22 * 11 # 字体大小
    headerfont.underline = False  # 下划线
    headerfont.italic = False  # 斜体字

    headeralignment = xlwt.Alignment()  # Create Alignment
    headeralignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    headeralignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED

    headerstyle = xlwt.XFStyle()  # 初始化样式
    headerstyle.font = headerfont  # 设定样式
    headerstyle.alignment = headeralignment
    # 遍历数据写入要存储的数据

    startrowindex = 1
    headerkeyArr = []

    for rowindex,eachdatadic in enumerate(orderinfolist):

        # 根据筛选数组过滤对应的写入数据
        for colindex, datakey in enumerate(eachdatadic.keys()):
            if not datakey in excelFileKeyArr:
                del eachdatadic[datakey]
            elif rowindex == 0:
                headerkeyArr.append(datakey)


        # 开始写入数据
        for colindex,datakey in enumerate(eachdatadic.keys()):

            # 设置列宽 字数 * 256
            myordersheet.col(colindex).width = 30 * 256

            datavalue = eachdatadic[datakey]

            try:
                # 写入数据
                # 看是否是字符串
                # 如果是字符串则直接写入
                if isinstance(datavalue, str):
                    myordersheet.write(startrowindex, colindex, datavalue)

                # 如果是数组则遍历数组进行写入
                if isinstance(datavalue, list):
                    for (productindex, eachproduct) in enumerate(datavalue):

                        productName = eachproduct['productName']

                        myordersheet.write(startrowindex, colindex, productName)

                        # # 合并单元格，合并第2行到第4行的第4列到第5列
                        # myordersheet.write_merge(2, 4, 4, 5, u'合并')

                        # 如果不是最后一个商品则行索引+1 如果是最后一个商品则不用+1 因为最后会加
                        if not len(datavalue) == 1 and not productindex == len(datavalue) - 1:
                            startrowindex = startrowindex + 1

                # 打印
                print ('写入第{num}/{totalnum}条数据成功'.format(num=rowindex,totalnum=len(orderinfolist)))
            except ValueError as e:
                print ('写入数据失败{error}'.format(error=e))

        startrowindex = startrowindex + 1


    # 最后写入表头
    try:
        for headerindex, headername in enumerate(headerkeyArr):
            myordersheet.write(0, headerindex, headername, headerstyle)
        print ('写入表头成功')
    except ValueError as e:
        print ('写入表头失败{error}'.format(error=e))


    workbookname = 'LAL' + datetime.now().strftime('%Y-%m-%d')
    workbook.save(workbookname+'.xls')
    print ('文件保存成功')

# 测试写入excel文件
def testwritetoExcel():

    allorderInfoList = [
    {
        "orderNum":"2010233WC6BE7Q",
        "totalCost":"40",
        "buyerName":"gtozakung",
        "productList":[
            {
                "productTotalPrice":"40",
                "productAmount":"1",
                "productName":"เบิร์ดแม็ก ยาถ่ายพยาธินก ใช้ได้ในนกและสัตว์ปีกสายพันธุ์ต่างๆ",
                "productImg":"https://s-cf-th.shopeesz.com/file/d61c8dcd8be2038dd862c9756cbfe56a_tn",
                "productSpec":"",
                "productPrice":"40"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"1",
        "totalShippingFee":"29",
        "totalOrderPrice":"68"
    },
    {
        "orderNum":"2010234902CY7S",
        "totalCost":"35",
        "buyerName":"39shi",
        "productList":[
            {
                "productTotalPrice":"35",
                "productAmount":"1",
                "productName":"กรรไกรตัดเล็บแมว กรรไกรตัดเล็บสุนัข กรรไกรตัดเล็บกระต่าย กรรไกรตัดเล็บสำหรับสัตว์",
                "productImg":"https://s-cf-th.shopeesz.com/file/192db7900533787b16231835992e6796_tn",
                "productSpec":"",
                "productPrice":"35"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"1",
        "totalShippingFee":"26",
        "totalOrderPrice":"60"
    },
    {
        "orderNum":"20102464EGHM4N",
        "totalCost":"60",
        "buyerName":"thebnatwara",
        "productList":[
            {
                "productTotalPrice":"60",
                "productAmount":"3",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productSpec":"",
                "productPrice":"20"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"2",
        "totalShippingFee":"29",
        "totalOrderPrice":"87"
    },
    {
        "orderNum":"2010245WMWAFR0",
        "totalCost":"30",
        "buyerName":"plengmie",
        "productList":[
            {
                "productTotalPrice":"15",
                "productAmount":"1",
                "productName":"商品1",
                "productImg":"https://s-cf-th.shopeesz.com/file/609f91da34a6a6495d370ec35abe9536_tn",
                "productSpec":"",
                "productPrice":"15"
            },
            {
                "productTotalPrice":"15",
                "productAmount":"1",
                "productName":"商品2",
                "productImg":"https://s-cf-th.shopeesz.com/file/609f91da34a6a6495d370ec35abe9536_tn",
                "productSpec":"",
                "productPrice":"15"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"1",
        "totalShippingFee":"0",
        "totalOrderPrice":"29"
    },
    {
        "orderNum":"20102466KE8B32",
        "totalCost":"100",
        "buyerName":"chantabu",
        "productList":[
            {
                "productTotalPrice":"100",
                "productAmount":"5",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productSpec":"",
                "productPrice":"20"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"1",
        "totalShippingFee":"0",
        "totalOrderPrice":"99"
    }
]

    writetoExcelbyOrderInfoList(allorderInfoList)


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
   opentargetUrl() # 打开目标页面
   allOrderList = getallorderList() # 获取所有的订单列表数据
   allOrderInfoList = getOrderInfoListbyOrderList(allOrderList) # 根据传入的订单列表获取对应的订单详情列表数据
   writetoExcelbyOrderInfoList(allOrderInfoList)

