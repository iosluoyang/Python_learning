# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  #伪装模块
from bs4 import BeautifulSoup

def defaultPhantomJS():
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1','--webdriver-loglevel=ERROR'])
    driver.get('http://service.spiritsoft.cn/ua.html')
    source = driver.page_source
    soup = BeautifulSoup(source,'lxml')
    user_agent = soup.find_all('td',attrs={'style':'height:40px;text-align:center;font-size:16px;font-weight:bolder;color:red;'})
    for u in user_agent:
        print( "伪装之前为:" + u.get_text().replace('\n','').replace(' ',''))
    driver.close()



def afterPhantomJS():

    #首先将DesiredCapabilities转换为一个字典，方便添加键值对
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    #然后添加一个浏览器标识的键值对：
    dcap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')

    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1','--webdriver-loglevel=ERROR'])
    driver.get('http://service.spiritsoft.cn/ua.html')
    source = driver.page_source
    soup = BeautifulSoup(source,'lxml')
    user_agent = soup.find_all('td',attrs={'style':'height:40px;text-align:center;font-size:16px;font-weight:bolder;color:red;'})
    for u in user_agent:
        print( "伪装之后为:" + u.get_text().replace('\n','').replace(' ',''))
    driver.close()





defaultPhantomJS()

afterPhantomJS()