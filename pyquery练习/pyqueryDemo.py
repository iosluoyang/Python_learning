# from pyquery import PyQuery as pq
#
#
# from lxml import etree
# doc = pq('http://www.baidu.com')
# print doc




# from pyquery import PyQuery as pq
# doc = pq(filename='hello.html')
# print doc.html()
# print type(doc)
# li = doc('li')
# print type(li)
# print li.text()



#
# from pyquery import PyQuery as pq
#
# p = pq('<p id="hello" class="hello"></p>')('p')
# print p.attr("id")
# print p.attr("id", "plop")
# print p.attr("id", "hello")



from pyquery import PyQuery as pq

p = pq('<p id="hello" class="hello"></p>')('p')
print p.addClass('beauty')
print p.removeClass('hello')
print p.css('font-size', '16px')
print p.css({'background-color': 'yellow'})