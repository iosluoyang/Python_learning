# encoding: utf-8

import itchat
import time
import sys

#避免python2.7中输出中文的报错问题
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import json

from collections import OrderedDict

from xlwt import *




#获取微信登录所需要的uuid
def getwxuuid():

    uuid = None
    while uuid is None :
        uuid = itchat.get_QRuuid()
        return uuid
        time.sleep(1)

#判断是否已经登录了微信
def checkiflogin():

    uuid = getwxuuid()
    print "获取的uuid为:" + uuid

    status = itchat.check_login(uuid)
    print status

    if status == '200':
        #登录成功 返回true
        return  True
    else:
        return False


#登录微信
def loginwx():

    #首先检查是否已经登录
    if checkiflogin():
        #已经登录
        return
    else:
        #未登录 执行登录操作
        itchat.auto_login(hotReload=False, statusStorageDir='登录记录', enableCmdQR=2)


#将相关数据保存起来
def writetosave(friends_list):


    print json.dumps(friends_list)

    #创建一个workbook对象 相当于是创建了一个excel文件
    book = Workbook(encoding='utf-8',style_compression=0)
    '''
    Workbook类初始化时有encoding和style_compression参数
    encoding:设置字符编码
    style_compression:表示是否压缩，不常用。
    '''

    #创建一个sheet对象  一个sheet对象对应Excel中的一个表格
    # 其中的wx_frienddata是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False
    sheet = book.add_sheet(mynickname + "的好友数据",cell_overwrite_ok=True)

    #遍历friends数组 将数据写入到sheet表中

    #注意此处使用有序字典
    sheettitledic = OrderedDict()

    sheettitledic["RemarkName"] = "备注名"
    sheettitledic["Sex"] = "性别"
    sheettitledic["Province"] = "省份"
    sheettitledic["City"] = "城市"
    sheettitledic["Signature"] = "签名"
    sheettitledic["NickName"] = "昵称"


    #表格样式相关

    #设置表格的列宽
    sheet.col(0).width = 256 * 20
    sheet.col(1).width = 256 * 5
    sheet.col(2).width = 256 * 10
    sheet.col(3).width = 256 * 10
    sheet.col(4).width = 256 * 30
    sheet.col(5).width = 256 * 20




    #将表头写入sheet中
    for index , key in enumerate(sheettitledic):

        #表头样式

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
        titlefont.height = 300  #15号字体



        #表头的边框
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


        #对齐方式
        titlealign = Alignment()
        titlealign.horz = Alignment.HORZ_CENTER #设置水平居中
        titlealign.vert = Alignment.VERT_CENTER #设置垂直居中



        titlestyle = XFStyle()
        titlestyle.pattern = titlepattern
        titlestyle.font = titlefont
        titlestyle.borders = titleborder
        titlestyle.alignment = titlealign


        #依次写入表头数据
        sheet.write(0, index, sheettitledic[key],titlestyle)


    #从第一行开始按照表头的值写入对应的数据
    for index1,friend  in enumerate(friends_list):

        # friend = json.dumps(friend)

        #遍历表头值的数组,将对应的数据取出来写入sheet中
        for index2 , key in enumerate(sheettitledic):
            #获取key对应的值value
            datavalue = friend[key]

            #如果是Sex的话则如果为1为男 2为女
            if key == 'Sex':

                datavalue = '男' if str(datavalue) == '1' else '女'

            #将获得的值写入对应的位置  注意这里行数要从1开始
            currentindex = index1 + 1
            sheet.write(currentindex, index2, datavalue)


    #写入数据完毕之后保存该文件
    book.save('wx_frienddata.xls')



#获取头像图片
def getheadImg(friend):


    # itchat.get_head_img() 获取到头像二进制，并写入文件，保存每张头像

    # 根据userName获取头像二进制文件
    img = itchat.get_head_img(userName=friend.UserName)

    #返回相关数据
    return img



#主程序
def startrun():

    #登录微信
    loginwx()

    '''
        关于itchat中用户的信息字典含义:
        UserName  微信的唯一id，一般用于判断是否是某个人的标准
        Signature   微信签名
        NickName    昵称
        HeadImgUrl  头像地址
        Sex         性别 1是男
        '''

    #个人信息：

    my = itchat.get_friends(update=True)[0]
    global myUserName
    myUserName = my.UserName
    global mynickname
    mynickname = my.NickName
    mysex = "男" if my.Sex == 1 else "女"
    mysign = my.Signature

    print '嗨,%s,您的微信用户名为: %s ,您的性别是%s,您的微信签名是:%s' % (mynickname ,myUserName, mysex, mysign)


    friends_list = itchat.get_friends()

    writetosave(friends_list)






#执行主程序
startrun()





