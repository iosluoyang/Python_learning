# encoding: utf-8
import re
import sys
sys.path.append("..")
from publicTools.public import GetHtmlDataClass

gethtml = GetHtmlDataClass()
html = gethtml.gethtml('http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/2017-10-16',None,False,'utf-8')
print html
