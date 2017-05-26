# -*- coding:utf-8 -*-
import xlrd
import xlwt
import config
from xlutils.copy import copy
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 将获取的内容写入到excel中:
def write_info(infos, file=config.OUT_FILE):
    if len(infos) >= 3:
        name = infos[0]
        print u'准备将', name, u'写入文件'
        comment = infos[1]
        url = infos[2]
        contents = (name, comment, url)
        write_to_excel(contents, file)
    else:
        print u'写入文件时发生错误，跳过写入'


def write_to_excel(contents, file=config.OUT_FILE):
    print u'正在写入到文本中', contents[0]
    try:
        rb = xlrd.open_workbook(file)
        sheet = rb.sheets()[0]
        row = sheet.nrows
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        count = 0
        name = contents[0]
        if not repeat_excel(name, file):
            for content in contents:
                sheet.write(row, count, content)
                count = count + 1
                wb.save(file)
                print u'已成功写入到文件', file, u'第', row + 1, u'行'
        else:
            print u'内容已存在, 跳过写入文件', file

    except IOError:
        print u'未找到该文件', file
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        book.add_sheet('sheet1', cell_overwrite_ok=True)
        book.save(file)
        print u'已成功创建该文件', file
        write_to_excel(contents, file)


# 检测某用户名是否已经存在在文件当中
def repeat_excel(word, file=config.OUT_FILE):
    #判断是否需要筛选用户，如果需要则过滤掉重复的用户，如果不需要则不进行过滤
    if FILTER_USER:
        print u'正在检测', word, u'是否存在于文件中'
        try:
            workbook = xlrd.open_workbook(file)
            sheet = workbook.sheet_by_index(0)
            # 拿到用户名那行的所有的值组成一个数组
            words = sheet.col_values(0)
            if word in words:
                print u'用户名在excel中已经存在', word, u'跳过该用户'
                return True
            else:
                print u'用户名在excel中不存在'
                return False
        except IOError, e:
            if 'No such file' in e.strerror:
                print u'匹配重复时未找到该文件', file
                new_excel(file)
                return False
            return False
    else:
        return False

# 创建新文件
def new_excel(file=config.OUT_FILE):
    print u'发现写入目标不存在，正在创建文件', file
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    book.add_sheet('sheet1', cell_overwrite_ok=True)
    book.save(file)
    print u'已成功创建文件', file








