

# import urllib2

# request = urllib2.Request('http://www.baidu.com')
# response = urllib2.urlopen(request)
# print response.read()



#POST
# import urllib
# import urllib2

# values = {'username':'ioslhy@163.com','password':'wyhhsh1993'}
# data = urllib.urlencode(values)
# url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
# request = urllib2.Request(url,data)
# response = urllib2.urlopen(request)
# print response.read()


#GET
# import urllib
# import urllib2

# values = {}
# values['username'] = 'ioslhy@163.com'
# values['password'] = 'wyhhsh1993'
# data = urllib.urlencode(values)
# url = 'http://passport.csdn.net/account/login'
# geturl = url + '?' + data
# request = urllib2.Request(geturl)
# response = urllib2.urlopen(request)
# print response.read()




# import urllib
# import urllib2

# url = 'https://www.douban.com/login'
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
# values = {'username':'ioslhy@163.com','password':'wyhhsh1993'}
# headers = {'User-Agent':user_agent,'Referer':'http://www.douban.com'}
# data = urllib.urlencode(values)
# request = urllib2.Request(url,data,headers,10)
# response = urllib2.urlopen(request)
# page = response.read()
# print page




# import urllib2
# request = urllib2.Request('http://blog.csdn.net/cqcre')
# try:
# 	urllib2.urlopen(request)
# except urllib2.HTTPError, e:
# 	print e.code
# except urllib2.URLError,e:
# 	print e.reason
# else:
# 	print 'OK'


# import urllib2
# request = urllib2.Request('http://blog.csdn.net/cqcre')
# try:
# 	urllib2.urlopen(request)

# except urllib2.URLError,e:
# 	if hasattr(e,'code'):
# 		print e.code
# 	if hasattr(e,'reason'):
# 		print e.reason
# else:
# 	print 'OK'



# import urllib2
# import cookielib
# cookie = cookielib.CookieJar()
# handler = urllib2.HTTPCookieProcessor(cookie)
# opener = urllib2.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
# 	print 'Name = ' + item.name
# 	print 'Value = ' + item.value





# import cookielib
# import urllib2

# filename = 'cookie.txt'
# cookie = cookielib.MozillaCookieJar(filename)
# handler = urllib2.HTTPCookieProcessor(cookie)
# opener = urllib2.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard = True,ignore_expires = True)




import cookielib
import urllib2

cookie = cookielib.MozillaCookieJar()
cookie.load('/Users/HelloWorld/Desktop/cookie.txt',ignore_discard = True ,ignore_expires = True)
req = urllib2.Request('http://www.baidu.com')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
print response.read()
























