from lxml import etree

# text = '''
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a>
#      </ul>
#  </div>
# '''
#
# html = etree.HTML(text)
# result = etree.tostring(html)
# print(result)







# <?xml version="1.0" encoding="ISO-8859-1"?>
#
# <bookstore>
#
# <book category="COOKING">
#   <title lang="en">Everyday Italian</title>
#   <author>Giada De Laurentiis</author>
#   <year>2005</year>
#   <price>30.00</price>
# </book>
#
# <book category="CHILDREN">
#   <title lang="en">Harry Potter</title>
#   <author>J K. Rowling</author>
#   <year>2005</year>
#   <price>29.99</price>
# </book>
#
# <book category="WEB">
#   <title lang="en">XQuery Kick Start</title>
#   <author>James McGovern</author>
#   <author>Per Bothner</author>
#   <author>Kurt Cagle</author>
#   <author>James Linn</author>
#   <author>Vaidyanathan Nagarajan</author>
#   <year>2003</year>
#   <price>49.99</price>
# </book>
#
# <book category="WEB">
#   <title lang="en">Learning XML</title>
#   <author>Erik T. Ray</author>
#   <year>2003</year>
#   <price>39.95</price>
# </book>
#
# </bookstore>

html = etree.parse('hello2.html')
# print html


result = html.xpath('/bookstore/book[price>35]/title/text()')
print result
