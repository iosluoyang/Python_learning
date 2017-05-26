#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#encoding=utf-8

#****************简单输入输出**************#
# a = input ("请输入你的名字:")
# print ("很高兴认识你:",a)

#****************简单输入输出**************#




#****************汉诺塔（递归函数）**************#

#写在前面:
# 要理解递归首先你得理解递归。
# 递归题就是找感觉，要有要把大象装冰箱总共分几步？这样的思维方式，
# 一但去抠细节你就中计了。

# 汉诺塔问题有三根柱子，我给它们分别命名为起始柱start，临时柱temp，目的柱end
# 盘子一共分两种情况：
# 1.只有1个盘子
# 这种情况下，直接从起始柱src 移动到 目的柱dst ,完成任务。

# 2.有1个以上的盘子
# 假如有n个盘子在起始柱，

# 首先把第n个盘子上方的n-1个盘子搬到临时柱。
# 然后把第n个盘子从起始柱移动到目的柱
# 最后把n-1个盘子从临时柱搬到目的柱 任务完成
# 知道这些就够了，千万别XJB去想细节！！！
# 知道这些就够了，千万别XJB去想细节！！！
# 知道这些就够了，千万别XJB去想细节！！！

# def move(A,B):#将盘子从A 移动到 B ,轻松愉快的移动一下就OK
# 	print(A,'->',B)


# def hanoi(n,start,temp,end):#将n个盘子从from 移动到 to
#  if n==1 :#只有一个盘子，
#  	move(start,end)
#  else:#有一个以上盘子的情况
#     hanoi(n-1,start,end,temp)#将最底下的那个盘子上面的n-1个盘子从start搬到temp
#     move(start,end)#将最底下的那个盘子轻轻的从start搬到end 
#     hanoi(n-1,temp,start,end)#完成最后一个动作，将temp上面的n-1个盘子搬到end上


# number = int(input('请输入第一个柱子上的金盘数量:'))
# a = input('想给第一个柱子起什么名字？')
# b = input('想给第二个柱子起什么名字？')
# c = input('想给第三个柱子起什么名字？')

# if number > 0:
# 	#进行数量计算
# 	hanoi(number,a,b,c)
	
# else:
# 	print('请输入一个正整数')



#****************汉诺塔（递归函数）**************#



#******************map和reduce**************#

#利用map和reduce编写一个str2float函数，把字符串转换成浮点数
# import re
# def strtofloat(s):
# 	def chartonum(s):
# 		 return {'-' : 0, '+' : 0, '0': 0, '1': 1, 
# 		 '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
# 		 '7': 7, '8': 8, '9': 9}[s]
# 	def fn(x,y):
# 		  return x * 10 + y
# 	#参数验证，包含字母字符串抛出异常
# 	if re.search(r'[a-zA-Z]+',s) != 'None':
# 		raise TypeError('Error type of your para!')


# 	#浮点数去小数点，标记调整位数tuneDigit
# 	tmp = s.split('.')
# 	tuneDigit = len(tmp[1])
# 	if tuneDigit > 0:
# 		s = tmp[0]+tmp[1]
# 	else:
# 		s = tmp[0]
# 	#处理正负数
# 	if s.find('-') == -1:
# 		flag = 1
# 	else:
# 		flag = -1
# 	#map/reduce操作，最后根据tuneDigit调整
# 	return flag *reduce(fn,map(chartonum,s))/(10 ** tuneDigit)
# 	# Examples
# print(strtofloat('12.09'))
# print(strtofloat('-12.09'))
# print(strtofloat('+12.09'))
# print(strtofloat('-.09'))
# print(strtofloat('+.09'))
# print(strtofloat('-12.'))
# print(strtofloat('-a12.'))

#******************map和reduce**************#


#******************@log的使用**************#

# def log(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper

# @log
# def now():
# 	print('2015-3-25')
# now()
#******************@log的使用**************#



#******************测试模块的代码**************#

# __author__ = 'Phil Liu'

# import sys

# def test():
#     args = sys.argv
#     if len(args)==1:
#             print('Hello, world!')
#     elif len(args)==2:
#         print('Hello, %s!' % args[1])
#     else:
#         print('Too many arguments!')

# if __name__=='__main__':
#     test()

#******************测试模块的代码**************#


#******************面向对象**************#

# class Student(object):
# 	"""学生类"""
# 	def __init__(self,name,score):
# 		super(Student, self).__init__()
# 		self.__name = name
# 		self.__score = score
# 	def print_score(self):
# 		print('%s: %s' %((self.__name,self.__score)))
# 	def get_grade(self):
# 		if self.__score >= 90:
# 			return self.__name + 'A'
# 		elif self.__score >= 60:
# 			return 'B'
# 		else:
# 			 return 'C'



# student1 = Student('student1',59)
# student2 = Student('student2',69)
# student3 = Student('student3',99)
# # print(student1.__name)//私有属性，不能得到，会报错

# print (student1.get_grade())

# print (student2.get_grade())
# print (student3.get_grade())


#******************面向对象**************#





#******************@property**************#
# class Student(object):
# 	"""docstring for Student"""
# 	@property
# 	def score(self):
# 		return self._score
# 	@score.setter
# 	def score(self,value):
# 		if not isinstance(value,int):
# 			raise ValueError('输入的必须为整型')
# 		if value < 0 or value > 100:
# 			raise ValueError('分数必须在0到100之间')
# 		self._score = value;
	
# s = Student()
# s.score = 60

# print(s.score)


# class Student(object):
# 	"""学生类"""
# 	@property
# 	def birth(self):
# 		return self._birth
# 	@birth.setter
# 	def birth(self,value):
# 		self._birth = value
# 	@property
# 	def age(self):
# 		return 2016 - self._birth

# s = Student()
# s.birth = 1990
# print(s.age)

# class Screen(object):

# 	@property   
# 	def width(self):
# 	    return self._width
# 	@width.setter
# 	def width(self,value):
# 	    self._width = value

# 	@property
# 	def height(self):
# 	    return self._height
# 	@height.setter
# 	def height(self,value):
# 	    self._height = value

# 	@property 
# 	def resolution(self):
# 	    return self._width * self._height

#     # test:
# s = Screen()
# s.width = 1024
# s.height = 768
# print(s.resolution)
# assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution

#******************@property**************#



#******************定制类**************#

# class Fib(object):
# 	"""斐波那契数列"""
# 	def __init__(self):
# 		super(Fib, self).__init__()
# 		self.a ,self.b = 0,1
# 	def __iter__(self):
# 		return self
# 	def __next__(self):
# 		self.a,self.b = self.b, self.a + self.b
# 		if self.a > 100000:
# 			raise StopIteration();
# 		return self.a
# 	def __getitem__(self,n):
# 		if isinstance(n, int): # n是索引	
# 			a,b = 1,1
# 			for x in range(n):
# 				a,b = b ,a+ b
# 			return a
# 		if isinstance(n,slice):
# 			start = n.start
# 			stop = n.stop
# 			if start is None:
# 				start = 0
# 			a,b = 1,1
# 			L = []
# 			for x in range(stop):
# 				if x >= start:
# 					L.append(a)
# 				a,b = b,a+b
# 			return L
# for n in Fib():
# 	print(n)

# f = Fib()
# print(f[5])

# f = Fib()
# print(f[0:5])

# class Chain(object):
# 	"""链式调用"""
# 	def __init__(self, path = ''):
# 		self.path = path
# 	def __getattr__(self,path):
# 		return Chain('%s/%s' % (self._path, path))
# 	def __str__(self):
# 		return self._path
# 	__repr__ = __str__

# print(Chain().status.user.timeline.list)

#******************定制类**************#


#******************枚举类**************#
# from enum import Enum
# Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
# for name , member in Month.__members__.items():
# 	print(name,'=>',member,',',member.value)

# from enum import Enum,unique
# @unique
# class Weekday(Enum):
# 	Sun = 0 #Sun的value被设定为0
# 	Mon = 1
# 	Tue = 2
# 	Wed = 3
# 	Thu = 4
# 	Fri = 5
# 	Sat = 6
# print(Weekday.Mon)

#******************枚举类**************#

#******************元类**************#
# def fn(self,name = 'World'):
# 	print('Hello,%s.'%name)
# Hello  = type('Hello',(object,),dict(hello = fn)) #创建Hello class
# h = Hello();
# print(h.hello)
#******************元类**************#


#******************错误调试，调用堆栈**************#
# def foo(s):
# 	return 10/int(s)
# def bar(s):
# 	return foo(s) * 2
# def main():
# 	try:
# 		bar('2')
# 	except Exception as e:
# 		print('Error:',e)
# 	else:
# 		print('No Error')
# 	finally:
# 		print('finally')
# main()
#******************错误调试，调用堆栈**************#

#******************调试方法**************#

# def foo(s):
# 	n = int(s)
# 	assert n != 0, 'n is zero!'
# 	return 10 / n

# def main():
# 	foo('0')
# main()

# import logging
# logging.basicConfig(level=logging.INFO)
# s = '0'
# n = int(s)
# logging.info('n = %d' %n)
# print(10/n)

# s = '0'
# n = int(s)
# print(10 / n)



#******************调试方法**************#

#******************单元测试**************#
# class Dict(dict):
# 	"""docstring for Dict"""
# 	def __init__(self, **kw):
# 		super().__init__(**kw)
# 	def __getattr__(self,key):
# 		try:
# 			return self[key]
# 		except KeyError:
# 			raise AttributeError(r"'Dict' 对象没有这个key:"%key)
# 	def __setattr__(self,key,value):
# 		self[key] = value


		
# import unittest
# from mydict import Dict
# class TestDict(unittest.TestCase):
# 	"""docstring for TestDict"""

# 	def test_init(self):
# 		d = Dict(a=1,b = 'test')
# 		self.assertEqual(d.a,1)
# 		self.assertEqual(d.b,'test')
# 		self.assertTrue(isinstance(d,dict))
# 	def test_key(self):
# 		d = Dict()
# 		d['key'] = 'value'
# 		self.assertEqual(d.key,'value')
# 	def test_attr(self):
# 		d = Dict()
# 		d.key = 'value'
# 		self.assertTrue('key' in d)
# 		self.assertEqual(d['key'],'value')
# 	def test_keyerror(self):
# 		d = Dict()
# 		with self.assertRaises(KeyError):
# 			value = d['empty']
# 	def test_attrerror(self):
# 		d = Dict()
# 		with self.assertRaises(AttributeError):
# 			value = d.empty
# if __name__ == '__main__':
# 	unittest.main()

#******************单元测试**************#


#******************读写文件**************#
# from io import StringIO
# f = StringIO()
# f.write('hello')
# print(f.getvalue())

# from io import BytesIO
# f = BytesIO()
# f.write('中文'.encode('utf-8'))
# print(f.getvalue())

# import os
# print(os.uname())
#******************读写文件**************#


#******************多进程**************#
# from multiprocessing import Process
# import os
# #子进程要执行的代码
# def run_proc(name):
# 	print('子进程跑的名字是:%s(%s)...'% (name,os.getpid())

# if __name__=='__main__':
# 	print('父进程跑的名字是:%s.'% os.getpid())
# 	p = Process(target =run_proc,args('测试进程名称',))
# 	print('子线程将要启动')
# 	p.start()
# 	p.join()
# 	print('子线程将要关闭')


# from multiprocessing import Pool
# import os, time, random

# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))

# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(4)
#     for i in range(5):
#         p.apply_async(long_time_task, args=(i,))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print('All subprocesses done.')

# import subprocess

# print('$ nslookup www.python.org')
# r = subprocess.call(['nslookup', 'www.python.org'])
# print('Exit code:', r)

# from multiprocessing import Process, Queue
# import os, time, random

# # 写数据进程执行的代码:
# def write(q):
#     print('Process to write: %s' % os.getpid())
#     for value in ['A', 'B', 'C']:
#         print('Put %s to queue...' % value)
#         q.put(value)
#         time.sleep(random.random())

# # 读数据进程执行的代码:
# def read(q):
#     print('Process to read: %s' % os.getpid())
#     while True:
#         value = q.get(True)
#         print('Get %s from queue.' % value)

# if __name__=='__main__':
#     # 父进程创建Queue，并传给各个子进程：
#     q = Queue()
#     pw = Process(target=write, args=(q,))
#     pr = Process(target=read, args=(q,))
#     # 启动子进程pw，写入:
#     pw.start()
#     # 启动子进程pr，读取:
#     pr.start()
#     # 等待pw结束:
#     pw.join()
#     # pr进程里是死循环，无法等待其结束，只能强行终止:
#     pr.terminate()
#******************多进程**************#

#******************多线程**************#
# import time,threading
# #新线程执行的代码
# def loop():
# 	print('线程%s 正在运行当中……'% threading.current_thread().name)
# 	n = 0
# 	while n<5:
# 		n = n + 1
# 		print('线程 %s >>> %s'%(threading.current_thread().name,n))
# 		time.sleep(1)
# 	print('线程 %s 结束了'% threading.current_thread().name)
# print('线程%s 正在运行当中……'% threading.current_thread().name)
# t = threading.Thread(target = loop ,name = 'LoopThread')
# t.start()
# t.join()
# print('线程%s结束了'%threading.current_thread().name)


#******************多线程**************#

#******************正则表达式**************#
# import re
# #编译:
# re_email = re.compile(r'([a-zA-Z][a-zA-Z0-9\.]*)@(\w+\.[a-zA-Z]+)$')
# #使用:
# email = input('请输入您的电子邮件')
# if re.match(re_email,email):
# 	print('校验成功，给予通过')
# else:
# 	print('校验失败，请重新输入')



# import re
# Email = '<Tom Paris> tom@voyager.org'
# re_Email = re.compile(r'^(<[a-zA-Z\.\s]{1,19}>)\s+(([0-9a-zA-Z\.]{1,19})\@[0-9a-z]{2,9}\.(com|org))$')
# name = re_Email.match(Email).group(1)
# email = re_Email.match(Email).group(2)
# print('%s Email: %s' %(name,email))

#******************正则表达式**************#


#******************Python自带的一些常用库**************#
# timedate
# ……
# from collections import namedtuple
# Point = namedtuple('Point',['x','y'])
# p = Point(1,2)
# print(p.x)

# from collections import deque
# q = deque(['a','b','c'])
# q.append('x')
# q.appendleft('y')
# print(q)

# from collections import defaultdict
# dd = defaultdict(lambda:'N/A')
# dd['key1'] = 'abc'
# print(dd['key1'])
# print(dd['key2'])


# 注意，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：
# from collections import OrderedDict
# d = dict([('a',1),('b',2),('c',3)])
# print(d)
# od = OrderedDict([('a',1),('b',2),('c',3)])
# print(od)


# from collections import Counter
# c = Counter()
# for ch in 'programming':
# 	c[ch] = c[ch] + 1
# print(c)

# import base64
# print(base64.b64encode(b'binary\x00string'))

# import struct
# print(struct.pack('>I',10240099))

# import hashlib
# md5 = hashlib.md5()
# md5.update('我该如何使用'.encode('utf-8'))
# md5.update('MD5加密'.encode('utf-8'))
# print(md5.hexdigest())
# import hashlib
# sha1 = hashlib.sha1()
# sha1.update('该如何使用sha1加密'.encode('utf-8'))
# print(sha1.hexdigest())

# import itertools
# natuals = itertools.count(1)
# for n in natuals:
# 	print(n)
# import itertools
# natuals = itertools.count(1)
# ns = itertools.takewhile(lambda x: x<= 10,natuals)
# print(list(ns))
# import itertools
# for c in itertools.chain('ABC','XYZ'):
# 	print(c)
# import itertools
# for key,group in itertools.groupby('AaaBBbcCAaA', lambda c: c.upper()):
# 	print(key+'->',list(group))

# @closing
# from contextlib import closing
# from urllib.request import urlopen
# with closing(urlopen('https://www.baidu.com')) as page:
# 		for line in page:
# 			print(line)



# from html.parser import HTMLParser
# from html.entities import name2codepoint

# class MyHTMLParser(HTMLParser):
# 	"""HTML解析"""
# 	def handle_starttag(self,tag,attrs):
# 		print('<%s>' % tag)
# 	def handle_endtag(self,tag):
# 		print('</%s>'%tag)
# 	def handle_startendtag(self,tag,attrs):
# 		print('<%s/>'%tag)
# 	def handle_data(self,data):
# 		print(data)
# 	def handle_comment(self,data):
# 		print('<!--',data,'-->')
# 	def handle_entityref(self,name):
# 		print('&%s;'% name)
# 	def handle_charref(self,name):
# 		print('&#%s;'%name)
# parser = MyHTMLParser()
# parser.feed('''<html>
# <head></head>
# <body>
# <!-- test html parser -->
#     <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
# </body></html>''')


# import requests
# from bs4 import BeautifulSoup
# resp = requests.get('https://www.python.org/events/python-events/')
# soup = BeautifulSoup(resp.text,'html.parser')
# for li in soup.select('.list-recent-events > li'):
# 	print('title:',li.find('a').text)
# 	print('time:',li.find('time').text)
# 	print('location:',li.select_one('.event-location').text)
# 	print('*'*100)
		
# from urllib import request
# with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
# 	data = f.read()
# 	print('Status:',f.status,f.reason)
# 	for k,v in f.getheaders():
# 		print('%s: %s'%(k,v))
# 	print('Data:',data.decode('utf-8'))

#模拟iPhone6请求豆瓣首页(Get请求)
# from urllib import request
# req = request.Request('http://www.douban.com')
# req.add_header('User-Agent','Mozilla/6.0(iphone OS 8_0 like Mac OS X) AppleWebKit/536.26(KHTML,like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# with request.urlopen(req) as f:
# 	print('Status:',f.status,f.reason)
# 	for k,v in f.getheaders():
# 		print('%s:%s' %(k,v))
# 	print('Data:',f.read().decode('utf-8'))

#模拟微博登录(Post请求)
# from urllib import request,parse
# print('正在登陆微博')
# username = input('请输入用户名')
# passwd = input('请输入密码')
# #参数数据:
# login_data = parse.urlencode([
# 	('username',username),
# 	('password',passwd),
# 	('entry','mweibo'),
# 	('client_id',''),
# 	('savestate','1'),
# 	('ec',''),
# 	('pagerefer','https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
# 	])
# req = request.Request('https://passport.weibo.cn/sso/login')
# req.add_header('Origin','https://passport.weibo.cn')
# req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

# with request.urlopen(req,data = login_data.encode('utf-8')) as f:
# 	print('Status:',f.status,f.reason)
# 	for k,v in f.getheaders():
# 		print('%s: %s'%(k,v))
# 	print('Data:',f.read().decode('utf-8'))

# from PIL import Image
#打开一个jpg图像文件路径:
# im = Image.open('/Users/HelloWorld/Desktop/kobe.jpg')
# #获得图像尺寸:
# w,h = im.size
# print('原始图片的尺寸为:%sx%s'%(w,h))
# #缩放到50%
# im.thumbnail((w//2,h//2))
# print('压缩之后的图片尺寸为:%sx%s',(w//2,h//2))
# #把缩放后的图像用jpeg格式保存
# im.save('/Users/HelloWorld/Desktop/kobefixed.jpg','jpeg')

#模糊图片
# from PIL import Image,ImageFilter
# #打开一个jpg图像文件路径:
# im = Image.open('/Users/HelloWorld/Desktop/kobe.jpg')
# #应用模糊滤镜
# im2 = im.filter(ImageFilter.BLUR)
# im2.save('/Users/HelloWorld/Desktop/kobeblur.jpg','jpeg')

#生成字母验证码图片:
# from PIL import Image,ImageFilter,ImageDraw,ImageFont
# import random
# #随机字母
# def rndchar():
# 	return chr(random.randint(65,90))
# #随机颜色1
# def rndcolor():
# 	return(random.randint(64,255),random.randint(64,255),random.randint(64,255))
# 	#随机颜色1
# def rndcolor2():
# 	return(random.randint(32,127),random.randint(32,127),random.randint(32,127))
# #240x60
# width = 60*4
# height = 60
# image = ImageFont.truetype('Arial.ttf',36)
# #创建Draw对象
# draw = ImageDraw.Draw(image)
# #填充每个像素
# for x in range(width):
# 	for y in range(height):
# 		draw.point((x,y), fill = rndcolor())
# #输出文字
# for t in range(4):
# 	draw.text((60*t + 10 ,10),rndchar(),font = font,fill = rndcolor2())
# #模糊：
# image = image.filter(ImageFilter.BLUR)
# image.save('/Users/HelloWorld/Desktop/随机验证码.jpg','jpeg')
#******************Python自带的一些常用库**************#



#******************第一个GUI程序**************#
# from tkinter import *
# import tkinter.messagebox as messagebox

# class Application(Frame):
# 	def __init__(self, master = None):
# 		Frame.__init__(self,master)
# 		self.pack()
# 		self.creatWidgets()
# 	def creatWidgets(self):
# 		self.nameInput = Entry(self)
# 		self.nameInput.pack()
# 		self.alertButton = Button(self,text= 'Hello',command = self.hello)
# 		self.alertButton.pack()

# 		self.helloLabel = Label(self,text='Hello,World!')
# 		self.helloLabel.pack()
# 		self.quitButton  = Button(self,text='Quit',command = self.quit)
# 		self.quitButton.pack()
# 	def hello(self):
# 		name = self.nameInput.get() or 'world'
# 		messagebox.showinfo('Message','Hello,%s'%name)
		
# app = Application()
# #设置窗口标题:
# app.master.title ('Hello,World')
# #主消息循环:
# app.mainloop()
	
#******************第一个GUI程序**************#


#******************发送邮件**************#
#SMTP是发送邮件的协议
# from email.mime.text import MIMEText
# msg = MIMEText('你好，今天下午有时间吗？','plain','utf-8')
# #通过SMTP协议发送出去
# #输入Email地址和口令:
# from_addr = input('您的邮件地址:')
# password = input('您的邮箱密码:')
# #输入收件人地址:
# to_addr = input('输入对方的邮件地址:')
# #必须要有from 和 to ，否则163邮箱不给予发送！！
# msg['from'] = from_addr
# msg['to'] = to_addr
# #输入SMTP服务器的地址:
# smtp_server = input('输入SMTP服务器的地址:')
# import smtplib
# server = smtplib.SMTP(smtp_server,25)#SMTP协议默认的端口是25
# server.set_debuglevel(1)
# server.login(from_addr,password)
# server.sendmail(from_addr,[to_addr],msg.as_string())
# server.quit()



#发送带有主题、发件人和收件人的邮件
# from email import encoders
# from email.header import Header
# from email.mime.text import MIMEText
# from email.utils import parseaddr,formataddr

# import smtplib
# def _format_addr(s):
# 	name,addr = parseaddr(s)
# 	return formataddr((Header(name,'utf-8').encode(),addr))
# from_addr = 'ioslhy@163.com' #input('邮件发送自:')
# password = 'wyhhsh1993'#input('密码:')
# to_addr = '891508172@qq.com'#input('邮件发送给:')
# smtp_server = 'smtp.163.com'#input('SMTP 服务器地址是:')

# msg = MIMEText('<html><body><h1>Hello</h1>' +
#     '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
#     '</body></html>','html','utf-8')
# msg['From'] = _format_addr('我是邮件发送人:%s' %from_addr)
# msg['To'] = _format_addr('邮件接收人:%s'%to_addr)
# msg['Subject'] = Header('这封邮件的主题是看你开心看你闹','utf-8').encode()

# server = smtplib.SMTP(smtp_server,25)
# server.set_debuglevel(1)
# server.login(from_addr,password)
# server.sendmail(from_addr,[to_addr],msg.as_string())
# server.quit()



#发送附件邮件

#邮件对象
# from email import encoders
# from email.header import Header
# from email.mime.text import MIMEText
# from email.utils import parseaddr,formataddr
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase



# import smtplib
# def _format_addr(s):
# 	name,addr = parseaddr(s)
# 	return formataddr((Header(name,'utf-8').encode(),addr))
# from_addr = 'ioslhy@163.com' #input('邮件发送自:')
# password = 'wyhhsh1993'#input('密码:')
# to_addr = '891508172@qq.com'#input('邮件发送给:')
# smtp_server = 'smtp.163.com'#input('SMTP 服务器地址是:')

# msg = MIMEMultipart()
# msg['From'] = _format_addr('我是邮件发送人:%s' %from_addr)
# msg['To'] = _format_addr('邮件接收人:%s'%to_addr)
# msg['Subject'] = Header('这封邮件的主题是看你开心看你闹','utf-8').encode()

# #邮件正文是MIMEText:
# msg.attach(MIMEText('<html><body><h1>给你发送一张图片叫做sunrise</h1>' +
#     '<p><img src="cid:0"></p>' +
#     '</body></html>', 'html', 'utf-8'))
# #添加附件就是加上一个MIMEBase,从本地读取一个图片:
# with open('/Users/HelloWorld/Desktop/sunrise.jpg','rb') as f:
# 	#设置附件的MIME和文件名，这里是jpg格式:
# 	mime = MIMEBase('image', 'jpg', filename='sunrise.jpg')
# 	#加上必要的头信息:
# 	mime.add_header('Content-Disposition','attachment',filename = 'sunrise.jpg')
# 	mime.add_header('Content-ID','<0>')
# 	mime.add_header('X-Attachment-ID','0')

# 	#把附件内容读进来:
# 	mime.set_payload(f.read())
# 	#用Base64编码:
# 	encoders.encode_base64(mime)
# 	#添加到MIMEMultipart:
# 	msg.attach(mime)
# #发送
# server = smtplib.SMTP(smtp_server,25)
# server.set_debuglevel(1)
# server.login(from_addr,password)
# server.sendmail(from_addr,[to_addr],msg.as_string())
# server.quit()




#******************发送邮件**************#

#******************收取邮件**************#
# import poplib
# from email.parser import Parser
# #输入邮件地址，口令和pop3服务器地址:
# email = input('请输入邮件地址:')
# password = input('请输入密码:')
# pop3_server = input('POP3服务器地址为:')

# #连接到pop3服务器:
# #链接QQpop服务时需要增加SSL
# # server = poplib.POP3_SSL(pop3_server)
# #链接163的时候不需要增加SSL
# server = poplib.POP3(pop3_server)
# #可以打开或者关闭调试信息:
# server.set_debuglevel(1)
# #可选:打印pop3服务器的欢迎文字:
# print(server.getwelcome().decode('utf-8'))

# #身份认证:
# server.user(email)
# server.pass_(password)

# #stat()返回邮件数量和占用空间:
# print('Message: %s Size: %s' % server.stat() )
# #list()返回所有邮件编号:
# resp,mails,octets = server.list()
# #可以查看返回的列表类似[b'1 82923',b'2 2184',...]
# print(mails)

# #获取最新一封邮件，注意索引号从1开始:
# index = len(mails)
# resp,lines,octets = server.retr(index)

# #lines存储了邮件的原始文本的每一行,
# #可以获得整个邮件的原始文本:
# msg_content = b'\r\n'.join(lines).decode('utf-8')
# #稍后解析出邮件:
# msg = Parser().parsestr(msg_content)

# # #可以根据邮件索引号直接从服务器删除邮件:
# # # server.dele(index)
# # #关闭连接:
# # server.quit()


# #解析邮件:
# from email.header import decode_header
# from email.utils import parseaddr

# #这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
# #嵌套可能还不止一层,所以我们要递归地打印出Message对象的层次结构：

# #indent用于缩进显示:
# def print_info(msg,indent = 0):
# 	if indent == 0:
# 		for header in ['From','To','Subject']:
# 			value  = msg.get(header,'')
# 			if value:
# 				if header == 'Subject':
# 					value = decode_str(value)
# 				else:
# 					hdr,addr = parseaddr(value)
# 					name = decode_str(hdr)
# 					value = u'%s <%s>'%(name,addr)
# 			print('%s%s: %s'%(' '* indent,header,value))
# 	if (msg.is_multipart()):
# 		parts = msg.get_payload()
# 		for n,part in enumerate(parts):
# 			print('%s part %s'%('  '* indent,n))
# 			print('%s-------------------'%('  '* indent))
# 	else:
# 		content_type = msg.get_content_type()
# 		if content_type == 'text/plain' or content_type == 'text/html':
# 			content = msg.get_payload(decode = True)
# 			charset = guess_charset(msg)
# 			if charset:
# 				content = content.decode(charset)
# 				print('%s Text: %s'%('  '*indent,content + '...'))
# 			else:
# 				print('%s Attachment: %s'%('  '* indent,content_type))
# #邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode：

# def decode_str(s):
# 	value,charset = decode_header(s)[0]
# 	if charset:
# 		value = value.decode(charset)
# 	return value
# #文本邮件的内容也是str，还需要检测编码，否则，非UTF-8编码的邮件都无法正常显示：
# def guess_charset(msg):
# 	charset = msg.get_charset()
# 	if charset is None:
# 		content_type = msg.get('Content-Type','').lower()
# 		pos = content_type.find('charset=')
# 		if pos >= 0:
# 			charset = content_type[pos + 8:].strip()
# 	return charset


# #打印从邮箱中获得的邮件内容:
# print_info(msg,0)

#******************收取邮件**************#


#******************访问数据库**************#
# 导入SQLite驱动:
# import sqlite3
# #连接到SQLite数据库
# #数据库文件是test.db
# #如果文件不存在，会自动在当前目录创建:
# conn = sqlite3.connect('/Users/HelloWorld/Desktop/测试数据库/test.db')
# #创建一个Cursor:
# cursor = conn.cursor()
# #执行一条SQL语句，创建user表
# cursor.execute('create table user (id varchar(20) primary key,name varchar(20))')
# #继续执行一条SQL语句，插入一条记录:
# cursor.execute('insert into user (id,name) values (\'8\',\'Phil\')')
# cursor.execute('insert into user (id,name) values (\'18\',\'Kobe\')')

# #通过rowcount获得插入的行数:
# print('插入的行数为:%s' %cursor.rowcount)

# #关闭Cursor:
# cursor.close()
# #提交事务:
# conn.commit()
# #关闭Connection：
# conn.close()




# #查询记录:
# conn = sqlite3.connect('/Users/HelloWorld/Desktop/测试数据库/test.db')
# cursor = conn.cursor()
# #执行查询语句:
# cursor.execute('select * from user where id=?',('8',))
# #获取查询结果集合:
# values = cursor.fetchall()
# print('查询的结果是:%s' %values)
# cursor.close()
# conn.close()


#ORM 关系数据库表结构映射对象技术
#导入:
# from sqlalchemy import Column,String ,create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# #创建对象的基类:
# Base = declarative_base()

# #定义user对象
# class  User(Base):
# 	"""表的名字"""
# 	__tablename__ = 'studentsusertable'
# #表的结构:
# id = Column(String(20),primary_key = True)
# name = Column(String(20))

# #初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://root:wyhhsh1993@127.0.0.1:3306/students')
	
# #创建DBSession类型
# DBSession = sessionmaker(bind = engine)


#******************访问数据库**************#


#******************Web**************#

#先在另外一个文件中编写该python文件
# def application(environ,start_response):
# 	start_response('200 OK',[('Content-Type','text/html')])
# 	return [b'<h1>Hello,web!</h1>']

#再编写另外一个python文件，负责启动WSGI服务器，加载alllication()函数:
# from wsgiref.simple_server import make_server
# #导入我们自己编写的application函数:
# from  printname import application

# #创建一个服务器，IP地址为空，端口是8000，处理函数是application:
# httpd = make_server('',8000,application)
# print('Serving HTTP on port 8000……')
# #开始监听HTTP请求:
# httpd.serve_forever()





#web框架实例

# from flask import Flask
# app = Flask(__name__)

# @app.route('/hello')
# def hello():
#     return '你好!'

# @app.route('/hi')
# def hi():
#     return '嗨!'

# if __name__ == '__main__':
#     app.run()


#web框架
# from flask import Flask
# from flask import request

# app = Flask(__name__)

# app.route("/",methods = ['GET','POST'])
# def home():
# 	return '<h1>Home</h1>'
# @app.route("/signin",methods = ['GET'])
# def signin_form():
# 	return '''<form action="/signin" method="post">
#               <p><input name="username"></p>
#               <p><input name="password" type="password"></p>
#               <p><button type="submit">Sign In</button></p>
#               </form>'''
# @app.route("/signin",methods = ['POST'])
# def signin():
# 	#需要从request对象读取表单内容:
# 	if request.form['username'] == 'liuhaiyang' and request.form['password'] == '123456':
# 		return '<h3>你好，老大</h3>'
# 	return '<h3>账号或密码错误,请检查</h3>'

# if __name__ == '__main__':
# 	app.run()



#用MVC模式
# from flask import Flask,request,render_template
# from flask import request

# app = Flask(__name__)

# app.route("/",methods = ['GET','POST'])
# def home():
# 	return render_template('home.html')

# @app.route("/signin",methods = ['GET'])
# def signin_form():
# 	return render_template('form.html')

# @app.route("/signin",methods = ['POST'])
# def signin():
# 	username = request.form['username']
# 	password = request.form['password']

# 	if username == 'liuhaiyang' and password == '123456':
# 		return render_template('signin-ok.html',username = username)
# 	return render_template('form.html',message = '账号或密码错误,请检查',username = username)
	

# if __name__ == '__main__':
# 	app.run()


#******************Web**************#


#******************	协程	**************#

# def consumer():
# 	r = ''
# 	while True:
# 		n = yield r
# 		if not n:
# 			return
# 		print('[CONSUMER] Consuming %s……' %n)
# 		r = '200 OK'

# def produce(c):
# 	c.send(None)
# 	n = 0
# 	while  n < 5:
# 		n = n + 1
# 		print('[PRODUCER] Producing %s……' %n)
# 		r = c.send(n)
# 		print('[PRODUCER] Consumer return: %s' %r)
# 	c.close()

# c = consumer()

# produce(c)
#******************	协程	**************#


#******************	异步IO	**************#
# import asyncio
# @asyncio.coroutine
# def hello():
# 	print('Hello World!')
# 	#异步调用asyncio.sleep(1):
# 	r = yield from asyncio.sleep(1)
# 	print('Hello again!')
# #获取EventLoop:
# loop = asyncio.get_event_loop()
# #执行coroutine
# loop.run_until_complete(hello())
# loop.close()




# import threading
# import asyncio

# @asyncio.coroutine
# def hello():
# 	print('Hello World!(%s)' %threading.currentThread())
# 	#异步调用asyncio.sleep(1):
# 	r = yield from asyncio.sleep(1)
# 	print('Hello again!(%s)' %threading.currentThread())

# #获取EventLoop:
# loop = asyncio.get_event_loop()
# tasks = [hello(),hello()]
# #执行coroutine
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()





# import asyncio
# @asyncio.coroutine
# def wget(host):
# 	print('wget %s……' %host)
# 	connect = asyncio.open_connection(host,80)
# 	reader,writer = yield from connect
# 	header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
# 	writer.write(header.encode('utf-8'))
# 	yield from writer.drain()
# 	while  True:
# 		line = yield from reader.readline()
# 		if line == b'\r\n':
# 			break
# 		print('%s header > %s' %(host,line.decode('utf-8').rstrip()))
# 	#Ignore the body ,close the socket
# 	writer.close()

# loop = asyncio.get_event_loop()
# tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()




# import asyncio

# from aiohttp import web

# async def index(request):
#     await asyncio.sleep(0.5)
#     return web.Response(body=b'<h1>Index</h1>')

# async def hello(request):
#     await asyncio.sleep(0.5)
#     text = '<h1>hello, %s!</h1>' % request.match_info['name']
#     return web.Response(body=text.encode('utf-8'))

# async def init(loop):
#     app = web.Application(loop=loop)
#     app.router.add_route('GET', '/', index)
#     app.router.add_route('GET', '/hello/{name}', hello)
#     srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
#     print('Server started at http://127.0.0.1:8000...')
#     return srv

# loop = asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()
#******************	异步IO	**************#


















