#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
import json
import time

from collections import OrderedDict
from xlwt import *


#获取所有的活动
def getAllActivityCodes():


    url = 'https://pt.morning-star.cn/pt-app/api/home/getAllActivityCodes'

    headers = {'token': 'kt7duxiewkea'}

    data = {'agentCode':'Agt180606620985892','latitude':'27.635109','longitude':'117.980629','columnCode':'all','searchValue':'','opc':'cs_cs'}

    r = requests.post(url=url,headers=headers,data=data)

    data = r.json()


    if r.status_code != 200:

        print "发生错误 " + str(r.status_code)

        return None

    else:

        try:

            print data['data']

            allActivityCodes = data['data']['activityCodes']

            return allActivityCodes

        except:

            print "未获取到数据"

            return None

        finally:

            print '活动数据获取完毕'

            print json.dumps(data)






#根据不同的活动ID获取活动详情 然后将其返回
def getActivityInfo(activityCode):


    url = 'https://pt.morning-star.cn/pt-app/api/activity/queryAct'

    headers = {'token': 'kt7duxiewkea'}

    data = {'activityCode':activityCode,'agentCode':'Agt180606620985892'}


    r = requests.post(url=url,headers=headers,data=data)

    data = r.json()


    if r.status_code != 200:

        print "获取详情发生错误 " + str(r.status_code)
        return None

    else:

        data = json.loads(json.dumps(data))

        return data['data']



#开始主程序
def startmission():

    #首先获取活动的所有编号数组
    allActivityCodes = getAllActivityCodes()

    if allActivityCodes != None:

        #创建Excel以及表头

        # 创建一个workbook对象 相当于是创建了一个excel文件
        book = Workbook(encoding='utf-8', style_compression=0)
        '''
        Workbook类初始化时有encoding和style_compression参数
        encoding:设置字符编码
        style_compression:表示是否压缩，不常用。
        '''

        # 创建一个sheet对象  一个sheet对象对应Excel中的一个表格
        # 其中的wx_frienddata是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False
        currentdatestr = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))

        booktitle = "你我您团购特卖商品爬取数据_" + currentdatestr


        sheet = book.add_sheet(booktitle, cell_overwrite_ok=True)

        # 注意此处使用有序字典
        sheettitledic = OrderedDict()


        sheettitledic["pCode"] = "商品编号"
        sheettitledic["title"] = "商品名称"
        sheettitledic["subtitle"] = "商品副标题"
        sheettitledic["realPrice"] = "真实售价"
        sheettitledic["originalPrice"] = "原价"
        sheettitledic["sellTotalCount"] = "销量"
        sheettitledic["supplierName"] = "供货商名称"




        # 表格样式相关

        # 设置表格的列宽
        sheet.col(0).width = 256 * 20
        sheet.col(1).width = 256 * 30
        sheet.col(2).width = 256 * 30
        sheet.col(3).width = 256 * 10
        sheet.col(4).width = 256 * 10
        sheet.col(5).width = 256 * 10
        sheet.col(6).width = 256 * 20

        # 将表头写入sheet中
        for index, key in enumerate(sheettitledic):
            # 表头样式

            # 表头背景颜色
            titlepattern = Pattern()
            titlepattern.pattern = Pattern.SOLID_PATTERN
            titlepattern.pattern_fore_colour = Style.colour_map['white']

            # 表头的字体
            titlefont = Font()
            titlefont.name = 'Times New Roman'
            # May be: 8 through 63.  0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,
            # 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown)
            # 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
            titlefont.colour_index = Style.colour_map['sky_blue']
            titlefont.bold = True
            titlefont.height = 300  # 15号字体

            # 表头的边框
            titleborder = Borders()

            '''
                May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE,
                HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED,
                THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED,
                or 0x00 through 0x0D.
            '''
            titleborder.left = Borders.MEDIUM  # 添加边框-虚线边框
            titleborder.right = Borders.MEDIUM  # 添加边框-虚线边框
            titleborder.top = Borders.MEDIUM  # 添加边框-虚线边框
            titleborder.bottom = Borders.MEDIUM  # 添加边框-虚线边框

            titleborder.left_colour = Style.colour_map['light_orange']  # 边框颜色
            titleborder.right_colour = Style.colour_map['light_orange']
            titleborder.top_colour = Style.colour_map['light_orange']
            titleborder.bottom_colour = Style.colour_map['light_orange']

            # 对齐方式
            titlealign = Alignment()
            titlealign.horz = Alignment.HORZ_CENTER  # 设置水平居中
            titlealign.vert = Alignment.VERT_CENTER  # 设置垂直居中

            titlestyle = XFStyle()
            titlestyle.pattern = titlepattern
            titlestyle.font = titlefont
            titlestyle.borders = titleborder
            titlestyle.alignment = titlealign

            # 依次写入表头数据
            sheet.write(0, index, sheettitledic[key], titlestyle)


        #从第一行开始按照表头的值写入对应的数据
        for index1, acticitycode in enumerate(allActivityCodes):

            #首先根据商品编号获取相对应的商品详情的信息数据
            infodata = getActivityInfo(acticitycode)

            if infodata != None:

                # 遍历表头值的数组,将对应的数据取出来写入sheet中
                for index2, key in enumerate(sheettitledic):

                    # 获取key对应的值value

                    datavalue = infodata[key]

                    # 将获得的值写入对应的位置  注意这里行数要从1开始
                    currentindex = index1 + 1
                    sheet.write(currentindex, index2, datavalue)

            print "数据采集进度为:  " + str(index1) + "/" + str(len(allActivityCodes)) + " " + "已经采集完毕"

            #休眠2秒
            time.sleep(2)

        #保存整个数据表格的数据
        book.save(booktitle + '.xls')




startmission()

