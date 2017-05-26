from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient
import datetime


class mzitu():

    def __init__(self):
        client = MongoClient() ##与MongDB建立连接（这是默认连接本地MongDB数据库）
        db = client['meinvxiezhenji'] ## 选择一个数据库
        self.meizitu_collection = db['meizitu'] ##在meizixiezhenji这个数据库中，选择一个集合
        self.title = '' ##用来保存页面主题
        self.url = '' ##用来保存页面地址
        self.img_urls = [] ##初始化一个 列表 用来保存图片地址

    def all_url(self, url):
        html = request.get(url, 3) ##这儿替换了，并加上timeout参数
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print(u'开始保存：', title) ##加点提示不然太枯燥了
            path = str(title).replace("?", '_') ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(path) ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            href = a['href']
            self.url = href  ##将页面地址保存到self.url中
            if self.meizitu_collection.find_one({'主题页面': href}):  ##判断这个主题是否已经在数据库中、不在就运行else下的内容，在则忽略。
                print(u'这个页面已经爬取过了')
            else:
                self.html(href) ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！


    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        html = request.get(href, 3)
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        page_num = 0  ##这个当作计数器用 （用来判断图片是否下载完毕）
        for page in range(1, int(max_span) + 1):
            page_num = page_num + 1  ##每for循环一次就+1  （当page_num等于max_span的时候，就证明我们的在下载最后一张图片了）
            page_url = href + '/' + str(page)
            self.img(page_url, max_span, page_num)  ##把上面我们我们需要的两个变量，传递给下一个函数。

    def img(self, page_url, max_span, page_num): ##添加上面传递的参数
        img_html = request.get(page_url, 3) ##这儿替换了
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)  ##每一次 for page in range(1, int(max_span) + 1)获取到的图片地址都会添加到 img_urls这个初始化的列表
        if int(max_span) == page_num:  ##我们传递下来的两个参数用上了 当max_span和Page_num相等时，就是最后一张图片了，最后一次下载图片并保存到数据库中。
            self.save(img_url)
            post = {  ##这是构造一个字典，里面有啥都是中文，很好理解吧！
                '标题': self.title,
                '主题页面': self.url,
                '图片地址': self.img_urls,
                '获取时间': datetime.datetime.now()
            }
            self.meizitu_collection.save(post)  ##将post中的内容写入数据库。
            print(u'插入数据库成功')
        else:  ##max_span 不等于 page_num执行这下面
            self.save(img_url)

    def save(self, img_url): ##这个函数保存图片
        name = img_url[-9:-4]
        img = request.get(img_url, 3) ##这儿替换了，并加上timeout参数
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path): ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/抓取妹子图(加入反爬虫)/抓取的图片/", path))
            os.chdir(os.path.join("/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/抓取妹子图(加入反爬虫)/抓取的图片/", path)) ##切换到目录
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url): ##这个函数获取网页的response 然后返回
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content

Mzitu = mzitu() ##实例化
Mzitu.all_url('http://www.mzitu.com/all') ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）





