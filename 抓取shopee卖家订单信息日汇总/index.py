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
import collections
from collections import Iterable
from datetime import datetime

shopeeaccount = '0955511464'
shopeepwd = 'N3184520eung'

stopOrderNum = ''
# 'orderNum','customerName','shippingWay','productList','totalShippingFee','totalCommissionFee','totalOrderPrice','totalCost'
excelFileKeyArr = ['orderNum','customerName','productList','totalCommissionFee']
# 'productName','productImg','productSpec','productUnitPrice','productQuantity','productTotalPrice'
excelProFileKeyArr = ['productName','productSpec','productUnitPrice','productQuantity']

driver = None
logincookiesPath = 'shopeelogincookies.json'
testlogincookiesPath = 'testshopeelogincookies.json'
# targetUrl = 'https://seller.th.shopee.cn'
targetUrl = 'https://seller.th.shopee.cn/portal/sale?type=shipping'

# 打开浏览器
def opendriver():

    global driver  # 注意这里的driver要进行全局变量的声明
    driver = webdriver.Chrome()

# 打开链接
def opentargetUrl():

    # 添加谷歌浏览器的启动配置

    # 在增加cookies前要先进行一次get访问
    # 访问shopee卖家中心登录页 https://seller.th.shopee.cn/account/signin
    driver.get(targetUrl)

    # 然后删除当前driver的所有cookies
    driver.delete_all_cookies()

    # 从本地文件中读取cookies写入 注意该cookies文件必须是一个list 且每一项含有必须的两个key: name和value
    with open(logincookiesPath, 'r') as f:
        cookies_list = json.loads(f.read())


    for eachcookie in cookies_list:
        driver.add_cookie(eachcookie)

    # 加完cookies之后再次进行一次get访问
    # driver.get(targetUrl)

    # 加完cookies之后刷新当前页面
    driver.refresh()

    # 如果有登录页面元素出现则说明需要重新登录获取cookies
    try:
        signinform = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            '.app-container .account-container .signin-panel .signin .signin-form'))
        )
        # 有登录表单元素出现说明需要重新登录获取cookies
    except:

        # 找不到说明无需登录 直接进行下面的操作即可
        print '没有定位到登录页面元素,本次无需登录,直接开始获取订单数据'
        allOrderList = getallorderList()  # 获取所有的订单列表数据
        allOrderInfoList = getOrderInfoListbyOrderList(allOrderList)  # 根据传入的订单列表获取对应的订单详情列表数据
        writetoExcelbyOrderInfoList(allOrderInfoList) # 将订单详情列表数据写入excel中

    else:
        # 找到说明需要登录
        print '获取登录表单元素成功,本次操作需要先登录'
        starttologin() # 开始登录操作

# 开始登录操作
def starttologin():

    # 定位登录输入框
    inputelements = driver.find_elements_by_css_selector(
        '.signin .signin-form .shopee-form-item .shopee-form-item__control .shopee-input input')

    # 账号输入框
    accountel = inputelements[0]
    pwdel = inputelements[1]

    # 键入账号密码
    accountel.send_keys(shopeeaccount)
    pwdel.send_keys(shopeepwd)

    # 点击记住密码
    driver.find_element_by_css_selector('.signin-form .remember .shopee-checkbox').click()

    # 点击登录按钮进行登录 此处改为手动登录
    # driver.find_element_by_css_selector('.signin-form button.shopee-button').click()

    # 等待直到页面进入主页面然后获取cookies
    try:
        sidebarelement = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.sidebar-container'))
        )
    except:
        print('登录失败,重新进行登录')
    else:
        print ('登录成功,开始获取cookies')

    # 获取cookies
    cookies = driver.get_cookies()
    # 将获取到的cookies序列化保存到本地
    cookiesdict = json.dumps(cookies)

    with open(logincookiesPath, 'w') as f:
        f.write(cookiesdict)

    # 写入完cookies之后重新访问目标链接
    opentargetUrl()

# 获取所有的订单列表
def getallorderList():

    # 直到页面有分页器则说明数据加载完毕了

    ifhaspagination = False # 是否有分页元素 默认为否

    try:
        paginationel =  WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
            '.new-order-list .order-list-pannel .order-list-section .pagination-bottom'))
        )
        ifhaspagination = True # 获取到了分页元素
    except:
        # 获取分页元素失败 尝试直接获取当前页的订单数据
        print ('未获取到分页元素')


    # 所有的订单元素集合
    allorderListArr = []

    # 根据是否有分页元素选择是否进行遍历分页获取订单数据
    if(ifhaspagination):

        # 获取总共有几页
        totalPages = paginationel.find_elements_by_css_selector('ul.shopee-pager__pages li.shopee-pager__page')
        print ('总共获取到{totalPage}页的订单'.format(totalPage=len(totalPages)))

        for (pageindex, eachpageel) in enumerate(totalPages):

            print ( '开始采集第{pageindex}/{totalPage}页'.format(pageindex=pageindex + 1, totalPage=len(totalPages)) )

            # 将该页面从上滑到下
            driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
            # 停留1秒钟
            sleep(1)

            if (pageindex > 0):

                # 点击自己当前的分页元素 以防止点击事情失效
                try:
                    owneachpageel = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,
                                                        'ul.shopee-pager__pages li.shopee-pager__page:nth-child(' + str(
                                                            pageindex + 1) + ')'))
                    )
                    print ('点击了当前页的分页元素:第{pageindex}页，元素为{el}'.format(pageindex=pageindex + 1, el=owneachpageel))
                    owneachpageel.click()
                except:
                    print ('点击第{pageindex}个的分页元素失败,开始重新获取该分页元素'.format(pageindex=pageindex + 1))

                # sleep(3)  # 休眠3秒


                # 直到页面有该页码的分页器被激活则说明数据加载完毕了
                try:
                    activepageel = WebDriverWait(driver, 20).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                                                          'ul.shopee-pager__pages li.shopee-pager__page.active'),
                                                         str(pageindex + 1))
                    )
                except:
                    print ('获取该页码的分页元素失败')

                else:
                    print ('获取该页码的分页元素成功:')
                    print (activepageel)

            # 获取当前页面的订单列表信息
            try:
                pageorderlist = getorderlistbypage()
                allorderListArr += pageorderlist

                print ('获取第{page}/{totalPage}页订单列表信息元素成功'.format(page=pageindex + 1, totalPage=len(totalPages)))


            except:
                print ('获取第{page}/{totalPage}页订单列表信息元素失败'.format(page=pageindex + 1, totalPage=len(totalPages)))

    # 没有分页元素 则默认为仅有一页数据 获取当前订单数据
    else:
        allorderListArr = getorderlistbypage()


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
    # print filterAllOrderListArr
    return  filterAllOrderListArr

# 获取当前页的订单数据
def getorderlistbypage():
    # 获取当前页面的订单列表信息
    try:

        orderlistels = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
            '.new-order-list .order-list-pannel .order-list-section .order-list-body a.order-item'))
        )

        # 在此将该页数据需要的信息提取出来 否则在后面针对该元素无法进行数据获取
        pageOrderList = []
        # 遍历订单列表 获取订单相关信息
        for (index, eachorderitemel) in enumerate(orderlistels):
            # 获取元素对应的订单相关信息

            # 订单号
            orderNum = eachorderitemel.find_element_by_css_selector(
                '.order-title .orderid'
            ).get_attribute('innerHTML').split(';')[1].encode("utf-8")
            # print ('该订单的订单号为:{orderNum}'.format(orderNum=orderNum))

            # 买家名称
            customerName = eachorderitemel.find_element_by_css_selector(
                '.order-title .title-prefix .user-header .username'
            ).text.encode("utf-8")
            # print ('该订单的买家名称为:{customerName}'.format(customerName=customerName))

            # 物流方式
            shippingWay = eachorderitemel.find_element_by_css_selector(
                '.order-list-item .actual-carrier-name'
            ).text.encode("utf-8")
            # print ('该订单的运送方式为:{shippingWay}'.format(shippingWay=shippingWay))

            # 订单详情链接
            orderLink = eachorderitemel.get_attribute('href').encode("utf-8")
            # print ('该订单的详情链接为:{orderLink}'.format(orderLink=orderLink))

            orderdata = {
                "orderNum": orderNum,
                "customerName": customerName,
                "shippingWay": shippingWay,
                "orderLink": orderLink
            }

            pageOrderList.append(orderdata)

        return pageOrderList

    except:
        print ('未获取当前页的订单数据')

# 根据订单列表数据获取对应的订单详情数据的集合
def getOrderInfoListbyOrderList(orderList):

    orderInfoList = []

    ifopennewwindow = True  # 是否打开新窗口 默认为true

    # 遍历订单列表
    for (orderindex, eachorderdata) in enumerate(orderList):


        try:
            # 获取订单详情页面内容
            orderDetailHtml = getOrderDetailPageContent(eachorderdata['orderLink'], ifopennewwindow)
            # print '获取网页内容---------开始'
            # print orderDetailHtml
            # print '获取网页内容---------结束'

            ifopennewwindow = False  # 将是否打开新的浏览器设置为false

            # 解析详情页面内容获取对应的数据
            orderInfo = getOrderInfo(orderDetailHtml)

            print ('获取到的该订单数据为')
            print orderInfo
            if(orderInfo == None) :
                print ('该订单出错')
                break

            orderInfoList.append(orderInfo)

        except Exception as e:

            print ('获取第{orderindex}/{totalnum}个订单详情数据发生错误,错误为:'.format(orderindex=orderindex + 1, totalnum=len(orderList)))
            print e
            print ('发生错误的订单html为:')
            print orderDetailHtml
            print ('第{orderindex}/{totalnum}个订单详情数据获取失败'.format(orderindex=orderindex + 1, totalnum=len(orderList)))

        else:
            print ('第{orderindex}/{totalnum}个订单详情数据获取成功'.format(orderindex=orderindex + 1, totalnum=len(orderList)))


    # print '获取到的订单详情列表数据为:'
    print json.dumps(orderInfoList)

    return orderInfoList


# 获取订单详情页面内容
def getOrderDetailPageContent(link, ifopennewwindow):

    # 根据是否需要打开新窗口来做不同情况的处理
    # global driver

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
    except:
        print ('获取订单详情商品列表元素失败')

    else:
        print ('获取订单详情商品列表元素成功')
        # 将该页面从上滑到下
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        # 等待1秒
        sleep(1)


    # 获取订单详情数据的元素内容
    orderDetailel = driver.find_element_by_css_selector('.fulfillment-order')
    detailHtml = orderDetailel.get_attribute('innerHTML')

    return detailHtml

    # driver.close()  # 关闭当前窗口（订单详情）

    # 切换回主页窗口
    # driver.switch_to.window(current_handle)


# 获取订单详情数据
def getOrderInfo(htmlcontent):

    soup = BeautifulSoup(htmlcontent, 'lxml')

    # 订单编号
    orderNum = soup.select('.order-detail .col-12 .shopee-card__content .grid.section .body div')[0].text.strip().encode("utf-8")
    # print orderNum

    # 物流方式
    # shopee规则有时会出现 .carrier 和.actual-carrier-name 此时.actual-carrier-name代表实际的物流方式
    try:
        shippingWay = soup.select('.actual-carrier-name')[0].text.strip().encode("utf-8")
    except:
        shippingWay = soup.select('.carrier')[0].text.strip().encode("utf-8");

    # print shippingWay

    # 买家名称
    customerName = soup.select('.user-view-item .username')[0].text.strip().encode("utf-8")
    # print customerName

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

        try:
            productSpecEl = eachproduct.select('.product-item .product-detail .product-meta div')
            if not productSpecEl is None:
                productSpec = productSpecEl[0].text.strip().split(':')[1].encode("utf-8")
                # print productSpec
        except:
            print('获取商品规格失败')


        # 商品单价
        productUnitPrice = eachproduct.select('.price')[0].text.strip().encode("utf-8")
        # print productUnitPrice

        # 商品数量
        productQuantity = eachproduct.select('.qty')[0].text.strip().encode("utf-8")
        # print productQuantity

        # 商品总价
        productTotalPrice = eachproduct.select('.subtotal')[0].text.strip().encode("utf-8")
        # print productTotalPrice

        # 构造商品数据collection有序字典
        productInfo = collections.OrderedDict()
        productInfo['productName'] = productName
        productInfo['productImg'] = productImg
        productInfo['productSpec'] = productSpec
        productInfo['productUnitPrice'] = productUnitPrice
        productInfo['productQuantity'] = productQuantity
        productInfo['productTotalPrice'] = productTotalPrice

        productList.append(productInfo)

    # print productList

    # 订单费用相关
    orderPaymentEl = soup.select('.payment-info-details')[0]

    # 订单总成本
    totalCost = ''
    totalCost = orderPaymentEl.select('.income-item.income-subtotal .income-value')[0].text.strip().encode("utf-8")
    totalCost = filter(str.isdigit,totalCost)
    print totalCost

    # 总运输费用
    totalShippingFee = ''
    totalShippingFee = orderPaymentEl.select('.income-item.income-subtotal .income-value')[1].text.strip().encode("utf-8")
    totalShippingFee = filter(str.isdigit, totalShippingFee)
    print totalShippingFee

    # 总平台服务费
    totalCommissionFee = ''
    totalCommissionFee = orderPaymentEl.select('.income-item.income-subtotal .income-value')[2].text.strip().encode("utf-8")
    totalCommissionFee = filter(str.isdigit, totalCommissionFee)
    print totalCommissionFee

    # 总实付金额
    totalOrderPrice = ''
    totalOrderPrice = orderPaymentEl.select('.income-item.income-subtotal.total .income-value')[0].text.strip().encode("utf-8")
    totalOrderPrice = filter(str.isdigit, totalOrderPrice)
    print totalOrderPrice

    # 结束订单信息的搜集
    # 开始组装数据

    orderInfo = {

        "orderNum":orderNum, # 订单编号
        "customerName": customerName,  # 买家名称
        "shippingWay": shippingWay, # 物流方式
        "productList": productList, #订单商品列表
        "totalCommissionFee": totalCommissionFee,  # 订单总平台服务费
        "totalShippingFee": totalShippingFee,  # 订单总物流费用
        "totalOrderPrice": totalOrderPrice,  # 订单实付金额
        "totalCost": totalCost, # 订单总成本

    }
    print json.dumps(orderInfo)
    return orderInfo


# 开始将订单详情列表数据写入excel表格中
def writetoExcelbyOrderInfoList(orderinfolist):

    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet 取当前的日期为sheet名称
    sheetname = 'LAL-' + datetime.now().strftime('%Y%m%d') + '-' + str(len(orderinfolist)) + ' Orders'
    myordersheet = workbook.add_sheet(sheetname, cell_overwrite_ok=True)

    # 表头字体样式
    headerfont = xlwt.Font()  # 为样式创建字体
    headerfont.name = 'Times New Roman'
    headerfont.bold = True  # 黑体
    headerfont.height = 22 * 11 # 字体大小
    headerfont.underline = False  # 下划线
    headerfont.italic = False  # 斜体字

    # 正常数据类型字体样式
    normalfont = xlwt.Font()  # 为样式创建字体
    normalfont.name = 'Times New Roman'
    normalfont.bold = False  # 黑体
    normalfont.height = 18 * 11  # 字体大小
    normalfont.underline = False  # 下划线
    normalfont.italic = False  # 斜体字

    # 数字类型字体样式
    numberfont = xlwt.Font()  # 为样式创建字体
    numberfont.name = 'Times New Roman'
    numberfont.bold = True  # 黑体
    numberfont.height = 33 * 11  # 字体大小
    numberfont.underline = False  # 下划线
    numberfont.italic = False  # 斜体字

    # 表尾字体样式
    footerfont = xlwt.Font()  # 为样式创建字体
    footerfont.name = 'Times New Roman'
    footerfont.bold = True  # 黑体
    footerfont.height = 40 * 11  # 字体大小
    footerfont.colour_index = 10  # 设置其字体颜色
    footerfont.underline = False  # 下划线
    footerfont.italic = False  # 斜体字

    centeralignment = xlwt.Alignment()  # Create Alignment
    centeralignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    centeralignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED

    headerstyle = xlwt.XFStyle()  # 初始化样式
    headerstyle.font = headerfont  # 设定样式
    headerstyle.alignment = centeralignment

    normalstyle = xlwt.XFStyle()  # 初始化样式
    normalstyle.font = normalfont # 设定样式
    normalstyle.alignment = centeralignment

    numberstyle = xlwt.XFStyle() # 初始化样式
    numberstyle.font = numberfont # 设定样式
    numberstyle.alignment = centeralignment

    footerstyle = xlwt.XFStyle() # 初始化样式
    footerstyle.font = footerfont # 设定样式
    footerstyle.alignment = centeralignment # 设定对齐方式

    # 合并表格的样式
    mergestyle = xlwt.XFStyle()  # 初始化合并单元格样式
    mergealignment = xlwt.Alignment()  # Create Alignment
    mergealignment.horz = xlwt.Alignment.HORZ_LEFT  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    mergealignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    mergestyle.alignment = mergealignment


    headerkeyArr = []  # 表头的键值 根据实际写入excel中的数据得出


    # 遍历数据写入要存储的数据

    startrowindex = 1 # 开始写入的行数索引

    # 写入每一行订单数据
    for orderindex,eachorderdata in enumerate(orderinfolist):

        # 开始尝试遍历每一个订单
        try:

            startcolindex = 0  # 开始写入的列数索引 归零
            ifreadprolist = False  # 是否已经读取过商品列数据的标识
            mergeIndexArr = [] # 合并单元格的列索引

            # 开始根据键值数组写入每一列数据
            for headerkey in excelFileKeyArr:

                datavalue = eachorderdata[headerkey]

                writefontstyle = normalstyle # 默认写入的字体样式

                # 值存在的时候判断值的类型进行写入
                if datavalue is not None:

                    try:

                        # 写入数据
                        # 看是否是字符串
                        # 如果是字符串则直接写入
                        if isinstance(datavalue, str):

                            # 如果是服务费金额则将内容转为数字并且使用数字样式
                            if (headerkey == 'totalCommissionFee'):
                                datavalue = float(datavalue)
                                writefontstyle = numberstyle

                            # 这里增加一个物流公司快递的名称转换
                            # if(headerkey == 'shippingWay'):
                            #     if('Shopee' in datavalue):
                            #         datavalue = 'Shopee'
                            #     elif ('DHL' in datavalue):
                            #         datavalue = 'DHL'


                            # 写入数据 如果已经读取过商品的列数据则将数据写入的行数变更为当前行数-商品数组长度+1
                            writerowindex = startrowindex
                            if ifreadprolist:
                                writerowindex = startrowindex - len(eachorderdata['productList']) + 1

                            myordersheet.write(writerowindex, startcolindex, datavalue, writefontstyle)
                            print ('写入第{startcolindex}列数据成功'.format(startcolindex=startcolindex))
                            # 写入完成将当前的startrowindex和当前startcol存入数据中
                            mergedic = {
                                "mergerowindex": writerowindex,
                                "mergecolindex": startcolindex,
                                "mergevalue": datavalue
                            }
                            print mergedic
                            mergeIndexArr.append(mergedic)

                            # 如果是第一行的数据则将对应的键值放入表头数组中
                            if orderindex == 0:
                                headerkeyArr.append(headerkey)  # 将键值加入表头键值数组(仅在第一个订单数据遍历时加入)
                                # 设置列宽 只有在第一行的时候才进行统一设置  字数 * 256 默认均为30个字
                                myordersheet.col(startcolindex).width = 30 * 256

                            # 写入完成之后将列数+1
                            startcolindex = startcolindex + 1  # 列数索引+1

                        # 如果是数组则遍历数组进行写入
                        elif isinstance(datavalue, list):

                            begincolindex = startcolindex # 记录最开始的列数索引
                            for (productindex, eachproduct) in enumerate(datavalue):

                                startcolindex = begincolindex # 列数索引复位

                                # 遍历对象数组中的可迭代对象键值进行数据写入
                                for (productdickeyindex, productdickey) in enumerate(excelProFileKeyArr):

                                    productvalue = eachproduct[productdickey]
                                    writefontstyle = normalstyle # 重置样式为普通样式

                                    # 找到该键值对应的值  若存在则写入
                                    if productvalue is not None:

                                        # 如果是商品图片则写入图片
                                        if productdickey == 'productImg':
                                            # myordersheet.insert_image(startrowindex, startcolindex, 'pro.png', {'url':productvalue})
                                            # 暂时写入图片路径
                                            myordersheet.write(startrowindex, startcolindex, productvalue,writefontstyle)
                                        # 其他数据则正常写入
                                        else:
                                            # 如果是商品数量或者单价金额则将内容转为数字并且使用数字样式
                                            if (productdickey == 'productQuantity' or productdickey == 'productUnitPrice'):
                                                productvalue = float(productvalue)
                                                writefontstyle = numberstyle

                                            myordersheet.write(startrowindex, startcolindex, productvalue,writefontstyle)

                                        print ('写入第{startcolindex}列数据成功'.format(startcolindex=startcolindex))

                                        # 如果是第一行的订单数据且为第一个商品数据则将对应的键值放入表头数组中
                                        if orderindex == 0 and productindex == 0:
                                            headerkeyArr.append(productdickey)
                                            myordersheet.col(startcolindex).width = 30 * 256  # 设置该列列宽
                                            # 如果是商品名称则将列宽设置为60
                                            if productdickey == 'productName':
                                                myordersheet.col(startcolindex).width = 60 * 256  # 设置该列列宽

                                        # 写入完成之后将列数+1
                                        startcolindex = startcolindex + 1  # 列数索引+1


                                # 如果不是最后一个商品则行索引+1 如果是最后一个商品则不用+1 因为最后会+1  重要！！！
                                if len(datavalue) > 1 and not productindex == len(datavalue) - 1:
                                    startrowindex = startrowindex + 1

                            ifreadprolist = True # 写完商品数据之后将是否读取过商品数据的标识变为True

                    except:
                        print ('写入第{startcolindex}列数据失败'.format(startcolindex=startcolindex))

            # # 合并单元格 如果一个订单中的商品列表超过1个则进行单元格合并
            # proListNum = len(eachorderdata['productList'])
            # if proListNum > 1:
            #     # 遍历每一个列 将当前rowindex和前rowindex-proListNum+1进行合并  例如有三个商品 当前行为10 则合并第10-3+1 = 8 行到第10行数据
            #     for mergeindexdic in mergeIndexArr:
            #
            #         mergerowindex = mergeindexdic['mergerowindex']
            #         mergecolindex = mergeindexdic['mergecolindex']
            #         mergevalue = mergeindexdic['mergevalue']
            #
            #         myordersheet.write_merge(mergerowindex-proListNum+1, mergerowindex, mergecolindex, mergecolindex,mergevalue,mergestyle)


            # 写入一个订单数据之后将行数索引+1
            startrowindex = startrowindex + 1


        except:
            print ('写入第{orderindex}/{totalorderindex}个订单数据失败'.format(orderindex=orderindex + 1,
                                                                     totalorderindex=len(orderinfolist)))
        else:

            print ('写入第{orderindex}/{totalorderindex}个订单数据成功'.format(orderindex=orderindex + 1,

                                                                     totalorderindex=len(orderinfolist)))

    # 写入表头数据
    try:
        print ('开始写入表头数据')
        for (headerindex, headerkey) in enumerate(headerkeyArr):
            myordersheet.write(0,headerindex,headerkey,headerstyle)
    except:
        print ('写入表头失败')
    else:
        print ('写入表头成功')

    # 写入表尾数据
    try:
        print ('开始写入表尾数据')
        sheetfooterstr = 'in total there is   ' + str(len(orderinfolist)) + '  orders'
        myordersheet.write(startrowindex + 5 ,3,sheetfooterstr,footerstyle)
    except:
        print ('写入表尾失败')
    else:
        print ('写入表尾成功')


    workbookname = 'LAL-' + datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '—(' + str(len(orderinfolist)) + ' Orders)'
    workbook.save(workbookname+'.xls')
    print ('文件保存成功')

# 测试写入excel文件
def testwritetoExcel():

    allorderInfoList = [
    {
        "orderNum":"201029KMGD0BVD",
        "totalShippingFee":"29",
        "customerName":"aukkara31",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/fdda562ade723d87ef6b007fd1355acf_tn",
                "productName":"Parrot Toy ที่แขวนมิลเล็ตสเปรย์ ของเล่นนก มิลเล็ต บันไดนก บันไดชูก้าร์ ที่แขวนอาหาร สำหรับนก หนู ชูก้าร์ กระรอก",
                "productSpec":"",
                "productUnitPrice":"44",
                "productQuantity":"1",
                "productTotalPrice":"44"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"1.25",
        "totalCost":"44",
        "totalOrderPrice":"72"
    },
    {
        "orderNum":"201030MS7P3JKX",
        "totalShippingFee":"0",
        "customerName":"pawanaaphongam",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productSpec":"",
                "productUnitPrice":"20",
                "productQuantity":"4",
                "productTotalPrice":"80"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"2",
        "totalCost":"80",
        "totalOrderPrice":"78"
    },
    {
        "orderNum":"201030MMK2YJ6F",
        "totalShippingFee":"0",
        "customerName":"hussayamonmeoy",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productSpec":"",
                "productUnitPrice":"20",
                "productQuantity":"1",
                "productTotalPrice":"20"
            }
        ],
        "shippingWay":"DHL Domestic",
        "totalCommissionFee":"20",
        "totalCost":"20",
        "totalOrderPrice":"20"
    },
    {
        "orderNum":"201029JXD58DFF",
        "totalShippingFee":"26",
        "customerName":"bangornkamasa",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productSpec":"",
                "productUnitPrice":"20",
                "productQuantity":"5",
                "productTotalPrice":"100"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"2",
        "totalCost":"100",
        "totalOrderPrice":"124"
    },
    {
        "orderNum":"201029K4N93JUU",
        "totalShippingFee":"29",
        "customerName":"yodkwan0604...",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/4fd05f2677676aacc6725dceb928ae4c_tn",
                "productName":"ปลอกคอสุนัข ปลอกคอเล็ก ปลอกคอ 3 หุน ปลอกคอแมว ปลอกคอสุนัขเล็ก ราคายกโหล",
                "productSpec":"",
                "productUnitPrice":"99",
                "productQuantity":"1",
                "productTotalPrice":"99"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"3",
        "totalCost":"99",
        "totalOrderPrice":"125"
    },
    {
        "orderNum":"201029KP41CDW8",
        "totalShippingFee":"0",
        "customerName":"opasza",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productSpec":"",
                "productUnitPrice":"20",
                "productQuantity":"7",
                "productTotalPrice":"140"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"3",
        "totalCost":"140",
        "totalOrderPrice":"137"
    },
    {
        "orderNum":"201030MWYW9DX3",
        "totalShippingFee":"29",
        "customerName":"usachuenarom",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productSpec":"",
                "productUnitPrice":"20",
                "productQuantity":"4",
                "productTotalPrice":"80"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"2",
        "totalCost":"80",
        "totalOrderPrice":"107"
    },
    {
        "orderNum":"201029K5Q4D935",
        "totalShippingFee":"0",
        "customerName":"anrkanatthawin",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/ce4d0f7210b70fdc8ad025cd934662e8_tn",
                "productName":"สปริงนกเขา สปริงสแตนเลส สปริงล็อคประตูกรง สปริงล็อคถาด สปริงสำหรับกรงนกเขา สปริงสำหรับกรงนกกางเขน",
                "productSpec":"789",
                "productUnitPrice":"45",
                "productQuantity":"1",
                "productTotalPrice":"45"
            },
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/6ba107083a104ab2e50f5477b55126a2_tn",
                "productName":"วิตามินนก วิตามินรวมสำหรับนก สินค้าคุณภาพ",
                "productSpec":"456",
                "productUnitPrice":"25",
                "productQuantity":"1",
                "productTotalPrice":"25"
            },
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/d61c8dcd8be2038dd862c9756cbfe56a_tn",
                "productName":"เบิร์ดแม็ก ยาถ่ายพยาธินก ใช้ได้ในนกและสัตว์ปีกสายพันธุ์ต่างๆ",
                "productSpec":"123",
                "productUnitPrice":"40",
                "productQuantity":"1",
                "productTotalPrice":"40"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"3",
        "totalCost":"110",
        "totalOrderPrice":"107"
    },
    {
        "orderNum":"201029KP3YNSE3",
        "totalShippingFee":"28",
        "customerName":"aibbetty",
        "productList":[
            {
                "productImg":"https://s-cf-th.shopeesz.com/file/9b854f5eb41f35fcc732830b63a93cad_tn",
                "productName":"เหยื่อกำจัดหนู สูตรตายแห้ง ยาฆ่าหนู ยาเบื่อหนู บรรจุ 4 เม็ด",
                "productSpec":"",
                "productUnitPrice":"20",
                "productQuantity":"10",
                "productTotalPrice":"200"
            }
        ],
        "shippingWay":"Shopee Express",
        "totalCommissionFee":"5",
        "totalCost":"200",
        "totalOrderPrice":"223"
    }
]

    writetoExcelbyOrderInfoList(allorderInfoList)

# 测试写入cookies文件
def testwritecookies():
    writeContent = [{
        "name": "name1",
        "value": "value1"
    }]
    # 将获取到的cookies序列化保存到本地
    testcookiesdict = json.dumps(writeContent)

    with open(testlogincookiesPath, 'w') as f:
        f.write(testcookiesdict)

# 测试读取cookies文件
def testreadcookies():
    with open(logincookiesPath, 'r') as f:
        testlist_cookies = json.loads(f.read())
    print testlist_cookies

# 测试构造有序字典
def testinitorderdict():

    productInfo = collections.OrderedDict()
    productInfo.productImg = 'imgurlxxx'
    productInfo['productName'] = 'productnamexxx'
    productInfo['productSpec'] = 'productspecxxx'
    productInfo['productUnitPrice'] = 'productUnitPricexxx'
    productInfo['productTotalPrice'] = 'producttotalpricexxx'
    productInfo['productQuantity'] = 'productQuantityxxx'

    print productInfo
    print isinstance(productInfo, Iterable)
    print productInfo['productName']

    for eachkey,eachvalue in productInfo.items():
        print ('key:{key}---value:{value}'.format(key=eachkey,value=eachvalue))

if __name__ == "__main__":

    opendriver() # 打开浏览器
    opentargetUrl() # 打开目标页面 开始进行操作


    # testwritetoExcel() # 测试写入订单数据到excel中

    # testwritecookies() # 测试写入cookies
    # testreadcookies() # 测试读取cookies
    # testinitorderdict() # 测试构造字典

    # 测试beautifulsoup提取网页内容
    # with open('htmlcontent.text', 'r') as f:
    #     htmlcontent = f.read()
    #
    # testOrderInfo = getOrderInfo(htmlcontent)
    # print json.dumps(testOrderInfo)

