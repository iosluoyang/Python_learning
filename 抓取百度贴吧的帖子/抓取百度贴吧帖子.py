# -*- decoding:utf-8 -*-
import urllib
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#工具类，用于处理抓取的源码的标签和图片
class Tool(object):
	#去除img标签,7位长空格
	removeImg = re.compile('<img.*?>| {7}|')
	#删除超链接标签
	removeAddr = re.compile('<a.*?>|</a>')
	#把换行标签转换为\n
	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
	#将表格制表<td>替换为\t
	replaceTD = re.compile('<td>')
	#把段落开头换位\n加两空格
	replacePara = re.compile('<p.*?>')
	#将换行符或双换行符替换为\n
	replaceBR = re.compile('<br><br>|<br>')
	#将其余标签剔除
	removeExtraTag = re.compile('<.*?>')
	def replace(self,x):
			x = re.sub(self.removeImg,"",x)
			x = re.sub(self.removeAddr,"",x)
			x = re.sub(self.replaceLine,"\n",x)
			x = re.sub(self.replaceTD,"\t",x)
			x = re.sub(self.replacePara,"\n  ",x)
			x = re.sub(self.replaceBR,"\n",x)
			x = re.sub(self.removeExtraTag,"",x)
			#strip()将前后多余内容删除
			return x.strip()	


#百度贴吧爬虫类
class BDTB:
	#初始化，传入基地址，是否只看楼主的参数
	def __init__(self, baseUrl,seeLZ,floorTag):
		#base链接地址
		self.baseURL = baseUrl
		#是否只看楼主
		self.seeLZ = '?see_lz='+str(seeLZ)
		#HTML标签剔除工具类对象
		self.tool = Tool()
		#全局file变量，文件写入操作对象
		self.file = None
		#楼层标号，初始为1
		self.floor = 1
		#默认的标题，如果没有成功获取到标题的话则使用百度贴吧的标题
		self.defaultTitle = u'百度贴吧'
		#是否写入楼分隔符的标记
		self.floorTag = floorTag


	#传入页码，获取该页帖子的代码
	def getPageCode(self,pageNum):
		try:
			#构建URL
			url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			#返回源码编码内容
			return response.read()
		#无法连接，报错
		except urllib2.URLError,e:
			if  hasattr(e,'reason'):
				print u'连接百度贴吧失败，错误原因为:',e.reason
				return None
	#获取帖子标题
	def getTitle(self,pageCode):
		#得到帖子标题的正则表达式
		pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow  .*?>(.*?)</h3>',re.S)
		result = re.search(pattern,pageCode)
		if result:
			#如果存在，则返回标题
			return result.group(1).strip()
		else:
			print u'未匹配到标题，请检查正则是否正确'
			return None

	#获取帖子总页数
	def getPageNum(self,pageCode):
		#获取帖子页数的正则表达式
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,pageCode)
		if result:
			return result.group(1).strip()
		else:
			print u'未匹配到总页数，请检查正则是否正确'
			return None

	#获取每一个帖子的作者,传入页面内容:(暂未使用)
	def getPageAuthor(self,pageCode):
		pattern = re.compile('<div class="louzhubiaoshi  j_louzhubiaoshi" author="(.*?)">',re.S)
		authors = re.findall(pattern,pageCode)
		for author in authors:
			print u'该帖子作者是:%s' %(author)

		return authors

	#获取每一层楼的内容,传入页面内容
	def getContent(self,pageCode):
		#匹配所有楼层的内容
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items = re.findall(pattern,pageCode)
		contents = []
		for item in items:
			#将文本进行去标签处理，同时在前后加入换行符
			content = "\n" + self.tool.replace(item) + "\n"
			contents.append(content)

		return contents

	def setFileTitle(self,title):
		#如果标题不是为None,则说明成功获取到标题
		if title is not None:
			self.file = open('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/抓取百度贴吧的帖子/抓取的帖子集合/' + title + '.txt','w+')
		else:
			self.file = open('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python_learning/抓取百度贴吧的帖子/抓取的帖子集合/' + self.defaultTitle + '.txt','w+')

	def writeData(self,contents):
		#向文件写入每一楼的信息
		for item in contents:
			if self.floorTag == '1':
				#楼之间的分隔符
				floorLine = '\n' + str(self.floor) + u'楼-----------------------------------------------------------------------------------------\n'
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexPageCode = self.getPageCode(1)
		pageNum = self.getPageNum(indexPageCode)
		title = self.getTitle(indexPageCode)
		self.setFileTitle(title)
		if pageNum == None:
			print 'URL已失效，请重试'
		try:
			print '该帖子共有' + str(pageNum) + '页'
			for i in range(1,int(pageNum)+1):
				print '正在写入第' + str(i) + '页数据'
				pageCode = self.getPageCode(i)
				contents = self.getContent(pageCode)
				self.writeData(contents)
		#出现写入异常
		except IOError, e:
			print '写入异常，原因为:'+ e.message
		finally:
			print '写入任务完成!🍻'


print u'请输入帖子代号'
baseURL = 'http://tieba.baidu.com/p/'+str(raw_input(u'http://tieba.baidu.com/p/'))		 
seeLZ = raw_input('是否只获取楼主发言，是输入1，否输入0\n')
floorTag = raw_input('是否写入楼层信息，是输入1，否输入0\n')
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()







		


