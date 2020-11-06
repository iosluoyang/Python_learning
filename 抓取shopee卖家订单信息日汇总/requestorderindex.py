#coding:utf8

import requests
import json


logincookiesPath = 'shopeelogincookies.json'


gettokenurl = 'https://seller.th.shopee.cn/api/v2/login/'
getorderidsurl = 'https://seller.th.shopee.cn/api/v3/order/get_simple_order_ids/'




# 使用request访问shopee相应接口获取代发货订单列表
def getallshippingorders():

    s = requests.Session()

    # 获取用户token

    # 从本地文件中读取cookies写入 注意该cookies文件必须是一个list 且每一项含有必须的两个key: name和value
    with open(logincookiesPath, 'r') as f:
        cookies_list = json.loads(f.read())

    newcookiedict = {}
    for eachcookie in cookies_list:
        cookiename = eachcookie['name']
        cookievalue = eachcookie['value']
        newcookiedict[cookiename] = cookievalue


    print '获取本地cookies的对象'
    print newcookiedict
    print '----------------------------------\n\n\n\n\n'



    tokenr = s.get(gettokenurl, cookies=newcookiedict)
    print '获取token的接口'
    print tokenr.url
    print tokenr.status_code
    print tokenr.cookies
    print tokenr.json()
    print '----------------------------------\n\n\n\n\n'

    token= tokenr.json()['token']
    print '获取token:'
    print token
    print '----------------------------------\n\n\n\n\n'



    # 获取完token之后使用同一个session进行接下来的请求
    getorderidparams = {
        'SPC_CDS': newcookiedict['SPC_CDS'], 'SPC_CDS_VER': '2','source': 'shipping',
        'page_size': '40','page_number': '1','total': '0', 'is_massship': 'false'
    }

    # 进行for循环获取所有的订单列表数据 知道返回的数据为空数组则停止
    allorderidsArr = []
    ifcontinue = True
    page_number = 1
    while ifcontinue:

        # 更新页码
        getorderidparams['page_number'] = str(page_number)

        # 进行接口请求
        orderidr = s.get(getorderidsurl, params=getorderidparams, cookies=newcookiedict)
        print('获取到第{page_num}页的订单列表数据'.format(page_num=page_number))
        print orderidr.url
        print orderidr.status_code
        print orderidr.cookies
        print orderidr.json()
        orders = orderidr.json()['data']['orders']
        print('本页共获取到{orderlistnum}个订单数据'.format(orderlistnum=len(orders)))
        print ('本页订单列表数据为:')
        print orders
        allorderidsArr = allorderidsArr + orders
        print '\n\n\n'
        if len(orders) == 0:
            ifcontinue = False
        page_number = page_number+1

    print ('共获取到{allorderidnum}个订单数据'.format(allorderidnum=len(allorderidsArr)))
    print allorderidsArr
    print '----------------------------------\n\n\n\n\n'


if __name__ == "__main__":

    getallshippingorders()