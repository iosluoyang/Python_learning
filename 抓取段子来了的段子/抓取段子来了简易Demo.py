# encoding: utf-8

import re
import sys
sys.path.append("..")
from publicTools.public import GetHtmlDataClass

gethtml = GetHtmlDataClass()
html = gethtml.gethtml('http://www.qiushibaike.com/')

pattern = re.compile('<div\s*?class="content">.*?<span>(.*?)</span>',re.S)   #使用点匹配模式 re.S
match = re.findall(pattern,html) #获取段子集合
for result in match:
    result = re.sub("<br/>","",result) #使用re.sub方法将字符串中的空格替换为空字符串,即删除空格
    result = result.strip()

    print result + "\n\n\n\n" + "-----------------------------\n"






