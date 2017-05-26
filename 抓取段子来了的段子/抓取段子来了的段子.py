# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

TotalPage = 3#如果抓取的页面多的话会造成网页限流，访问失败的情况，所以暂时抓取前3页

#糗事百科爬虫类
class QSBK:
	#初始化方法，定义一些变量
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#初始化headers
		self.headers = {'User-Agent':self.user_agent}
		#存放段子的变量，每一个元素是每一页的段子们
		self.stories = []
		#存放程序是否继续运行的变量
		self.enable = False
		#全局file变量，文件写入操作对象
		self.file = None
		#序列标号，初始为1
		self.floor = 1

	#传入某一页的索引获取页面代码
	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			#构建请求的request
			request = urllib2.Request(url,headers = self.headers)
			#利用urlopen获取页面代码
			response = urllib2.urlopen(request)
			#将页面转化为UTF-8编码
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print u"连接糗事百科失败，错误原因为:",e.reason
				return None

	#传入某一页代码，返回本页所有的段子列表
	def getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "页面加载失败……"
			return None
		pattern = re.compile('<div class="article.*?title="(.*?)".*?<div class="content">.*?<span>(.*?)</span>.*?</div>.*?<span class="stats-vote">.*?<i class="number">(.*?)</i>.*?<span class="stats-comments">.*?<i class="number">(.*?)</i>.*?</a>.*?</div>'
							,re.S)
		items = re.findall(pattern,pageCode)
		#用来存储每页的段子们
		pageStories = []
		#遍历正则表达式匹配的信息
		index = 1;
		for item in items:
			#将段子内容中的回车标识符<br/>去除掉
			replaceBR = re.compile('<br/>')
			text = re.sub(replaceBR,'\n',item[1])
			#item[0]是作者名称，item[1]是段子内容，item[2]是点赞个数，item[3]是评论个数
			content = u'第%d个段子:\n发布人:%s\n段子内容:\n%s\n%s个人觉得很赞\n%s个人进行了评论\n\n\n' %(index,item[0].strip(),text.strip(),item[2].strip(),item[3].strip())
			if content:
				pageStories.append(content)
				index += 1
			else:
				pass
			
			

		return pageStories


	#开始方法
	def start(self):
		print u'正在抓取糗事百科的段子……'

		try:
			for i in range(1,TotalPage+1):
				print '正在写入第' + str(i) + '页的段子'
				#文件名称
				f = open('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/抓取段子来了的段子/抓取的段子来了的段子集合/第' + str(i) + '页段子.txt','w+')
				#获取每一页的段子集合
				contents = self.getPageItems(i)
				#遍历段子集合，将每一个段子写入文件当中
				for content in contents:
					f.write(content)
						
				
		#出现写入异常
		except IOError, e:
			print '写入异常，原因为:'+ e.message
		finally:
			print '写入任务完成!🍻'


spider = QSBK()
spider.start()

