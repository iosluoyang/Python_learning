#coding:utf8

# 考生学籍号: 120524081  考生姓名: 吕由    编写日期:2018/06/23
originalnum = input("请输入要转换进制的数值:")#得到用户输入的原始数据信息
remainArr = []#记录每次余数的数组

while(originalnum != 0):#开始while循环
    remainArr.append(str(originalnum%2))#用户原始数据取余2的结果存放在数组中
    originalnum = originalnum/2#将原始数据整除2得到新一轮循环的初始数据

remainArr.reverse()#反转记录数据
resultnum = "".join(remainArr)#拼接为字符串
print ("该数字转换为二进制后是:"+resultnum)#打印出来结果



