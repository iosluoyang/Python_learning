# encoding: UTF-8
#需要首先声明编码解码方式才能在之后添加注释
# 正则表达式部分参考  http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html

import re

print ("——————————————————实验1(match方法)开始————————————————————\n")

# 将正则表达式编译成Pattern对象
pattern = re.compile(r'hello')
# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
result1 = re.match(pattern,'hello')
result2 = re.match(pattern,'helloo LHY')
result3 = re.match(pattern,'helo LHY')
result4 = re.match(pattern,'hello LHY')

if result1:
	print result1.group()
else:
	print '1匹配失败'

if result2:
	print result2.group()
else:
	print '2匹配失败'


if result3:
	print result3.group()
else:
	print '3匹配失败'


if result4:
	print result4.group()
else:
	print '4匹配失败'

# Tips:
#match必须是从一开始就匹配成功，否则均为匹配失败
# match方法只能匹配一个结果，如果没有结果则直接返回none

print ("——————————————————实验1(match方法)结束————————————————————\n\n\n\n")








print ("——————————————————实验2(search方法)开始————————————————————\n")

pattern = re.compile(r'world')

match = re.search(pattern,'hello1 world lhy2 world!')
if match:
	print match.group()
else:
    print ('没有匹配到任意一项')

#Tips:
# search()方法可以在任意位置进行匹配，如果满足条件则直接返回匹配的结果，但是只能匹配第一项，其他的无法通过group获得

print ("——————————————————实验2(search方法)结束————————————————————\n\n\n\n")






print ("——————————————————实验3(split方法)开始————————————————————\n")

pattern = re.compile(r'\d+')
match = re.split(pattern,'one12two23three34four45')
print match

#Tips:
#split(string[, maxsplit]) | re.split(pattern, string[, maxsplit]):
#按照能够匹配的子串将string分割后返回列表。maxsplit用于指定最大分割次数，不指定将全部分割。
print ("——————————————————实验3(split方法)结束————————————————————\n\n\n\n")



print ("——————————————————实验4(findall方法)开始————————————————————\n")

pattern = re.compile(r'\d+')
match =  re.findall(pattern,'hello2ttt34world789!llala')
print match

#Tips:一般这个用的比较多，是在整体字符串中搜索出来符合条件的字符串，然后以列表的形式进行展现，一般用于字符串的提取

print ("——————————————————实验4(findall方法)结束————————————————————\n\n\n\n")



print ("——————————————————实验5(finditer方法)开始————————————————————\n")

pattern = re.compile(r'\d+')
for m in re.finditer(pattern,'one156two289three334four422'):
	print m.group()

#Tips:
#finditer(string[, pos[, endpos]]) | re.finditer(pattern, string[, flags]):
#搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器。
print ("——————————————————实验5(finditer方法)结束————————————————————\n\n\n\n")




print ("——————————————————实验6(sub方法)开始————————————————————\n")

pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'

print re.sub(pattern,r'\2 \1',s)#交换每一组匹配出来的字符串的顺序

def func(m):
	return m.group(1).title() + '' + m.group(2).title()

print re.sub(pattern,func,s)

#Tips:
# sub(repl, string[, count]) | re.sub(pattern, repl, string[, count]):
# 使用repl替换string中每一个匹配的子串后返回替换后的字符串。
# 当repl是一个字符串时，可以使用\id或\g<id>、\g<name>引用分组，但不能使用编号0。
# 当repl是一个方法时，这个方法应当只接受一个参数（Match对象），并返回一个字符串用于替换（返回的字符串中不能再引用分组）。
# count用于指定最多替换次数，不指定时全部替换

print ("——————————————————实验6(sub方法)结束————————————————————\n\n\n\n")





print ("——————————————————实验7(subn方法)开始————————————————————\n")

pattern = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'

print re.subn(pattern,r'\2 \1',s)

def func(m):
	return m.group(1).title() + '' + m.group(2).title()

print re.subn(pattern,func,s)

#Tips:
#返回 (sub(repl, string[, count]), 替换次数)。

print ("——————————————————实验7(subn方法)结束————————————————————\n\n\n\n")
























































