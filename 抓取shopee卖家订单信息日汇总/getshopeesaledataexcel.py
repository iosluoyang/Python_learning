#coding=utf8

import xlrd
import xlwt
from datetime import datetime

excelpath = r'/Users/HelloWorld/Desktop/Order.all.20200918_20201018 2.xls'
sheetname = 'orders'
allDataArr = []
needkeyarr = ['orderNum', 'buyerName','deliveryWay','sellPrice','amount','totalPrice']

def readExcel():
    # 打开文件
    workbook = xlrd.open_workbook(excelpath)
    # 获取所有的sheet
    allsheets = workbook.sheet_names()
    print ('所有的sheet表为:{sheet_names}'.format(sheet_names=allsheets))

    # 读取特定sheet的内容
    orderssheet = workbook.sheet_by_name(sheetname)
    # 检查sheet数据导入完毕
    if(workbook.sheet_loaded(sheetname)):
        print ('ordersheet的行数为:{rownum},列数为:{colnum}'.format(rownum=orderssheet.nrows, colnum=orderssheet.ncols))

        # 循环遍历每一行数据
        for rowindex in range(1,orderssheet.nrows):
            eachrowdatalist = orderssheet.row_values(rowindex)
            eachdatadic = {}
            # 遍历每一列 设置对应的数据
            for colindex in range(orderssheet.ncols):
                colname = orderssheet.col_values(colindex)[0]
                colvalue = eachrowdatalist[colindex]
                eachdatadic[colname] = colvalue

            allDataArr.append(eachdatadic)

        print ('数据读取完毕,共有{rownum}条数据被导入'.format(rownum=len(allDataArr)))

def writeExcel():
    # 创建工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建sheet 取当前的日期为sheet名称
    sheetname = 'LAL' + datetime.now().strftime('%Y-%m-%d %H%M%S')
    myordersheet = workbook.add_sheet(sheetname,cell_overwrite_ok=True)

    # 遍历数据写入要存储的数据
    for (rowindex,eachdatadic) in enumerate(allDataArr):

        newcolindex = 0
        for (colindex,datakey) in enumerate(eachdatadic.keys()):

            try:
                datavalue = eachdatadic[datakey]
                if(datakey in needkeyarr):
                    myordersheet.write(rowindex + 1, newcolindex, datavalue)
                    newcolindex = newcolindex + 1

            except ValueError as e:
                print ('写入数据失败{error}'.format(error=e))



    workbook.save('formatdataexcel.xls')




if __name__ == '__main__':
    readExcel()
    writeExcel()