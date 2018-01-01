# encoding: utf-8
# 摩拜单车位置信息抓取  原文参考 https://www.zhihu.com/question/53141781
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import os
import sys
sys.path.append("/usr/pythonprojects/publicTools")
import time
import requests

'''
header:wxcode:微信openID(写个假的也可以)
header:time:请求的时间戳(精确到毫秒)
header:cityCode:城市编码 等同于座机号
body:longitude:经度
body:latitude:维度
body:altitude:海拔
body:citycode:城市编码(同header:cityCode)
'''

session = requests.Session()
session.headers['host'] = 'mwx.mobike.com'
session.headers['content-type'] = 'application/x-www-form-urlencoded'
session.headers['opensrc'] = 'list'
session.headers['mobileNo'] = ''
session.headers['wxcode'] = 'fake wxcode'
session.headers['platform'] = '3'
session.headers['accept-language'] = 'zh-cn'
session.headers['subsource'] = ''
session.headers['lang'] = 'zh'
session.headers['user-agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.22 NetType/WIFI Language/zh_CN'
session.headers['referer'] = 'https://servicewechat.com/wx80f809371ae33eda/141/page-frame.html'

def getmobikemsg():
    session.headers["time"] = str(long(time.time()*1000)) #精确到秒的时间戳
    session.headers["citycode"] = '010'

    body = {
        'verticalAccuracy':10,
        'speed':-1,
        'horizontalAccuracy':65,
        'accuracy':65,
        'errMsg':'getLocation:ok',
        'citycode':'010',
        'wxcode':'fake wxcode',
        'longitude':'116.7186',
        'latitude':'39.94749',
        'altitude':'18.81986236572266',
    }

    data = session.post(url='https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do',data=body).json()
    titledic = {"num":"车辆编号","locationX":"车辆坐标X值","locationY":"车辆坐标Y值","distance":"车子当前距离","type":"车子类型"}
    title = '{num}\t{locationX}\t{locationY}\t{distance}\t{type}'.format(**titledic)
    print title
    for bike in data['object']:
        location = '{distId}\t{distX}\t{distY}\t{distance}\t{biketype}'.format(**bike)
        print location

getmobikemsg()
