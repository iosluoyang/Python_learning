# -*- coding:UTF-8 -*-
# encoding: utf-8

#该demo基于廖雪峰老师的博客而写，参考网址: https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432005226355aadb8d4b2f3f42f6b1d6f2c5bd8d5263000

#此类默认为使用本人ioslhy@163.com这个邮箱进行作为发送人,须知163邮箱的smtp_server是smtp.163.com 端口默认为25


#构造邮件内容需要引入的库
from email import  encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage  #邮件图片类库
from email.mime.base import MIMEBase

import smtplib #发送邮件类库
from urllib import urlretrieve #自动下载网络图片到本地
import shutil
import os
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler #定时任务类库
from datetime import datetime




class SendMailClass():

    #发送邮件 注意此处必选参数必须在前，有默认值的参数在后
    def sendmail(self,toaddressarr,emailtextcontent,emailimgArr=[],emaillocalfiles=[],fromNickname='小海哥',toNickname='嗨我亲爱的你',emailsubject='这是一封你点了就会后悔的信'):
        fromaddress = 'ioslhy@163.com'#发件人地址
        frompwd = 'wyhhsh1993' #发件人密码
        fromsmtpserver = 'smtp.163.com' #SMTP服务器地址
        to_addrs = toaddressarr #收件人邮箱数组
        fromnickname = fromNickname #发件人昵称
        tonickname = toNickname #收件人昵称
        subject = emailsubject #邮件主题
        textcontent = emailtextcontent #邮件文本内容
        imgUrlArr = emailimgArr #邮件正文中要显示的图片链接或者本地图片路径
        localfiles = emaillocalfiles #邮件中的附件数组，每一个数组都是一个字典对象,包含了文件路径，附件类型，附件后缀以及附件的展示名称

        #注意，该工具类暂时使用html类型,如果需要根据情况更改直接更改类型即可

        #构建邮件内容
        msg = MIMEMultipart('related')
        msg['From'] = _format_addr('%s:%s' %(fromnickname,fromaddress))
        msg['To'] = _format_addr('%s' %(tonickname))
        msg['Subject'] = Header(subject,'utf-8').encode()

        contentimg = "" #后面需要增加到正文中的img字符串
        #遍历图片数组 因为不能直接将网络图片URL作为图片参数进行传输所以对于网络图片先下载再进行发送邮件
        for i,img in enumerate(imgUrlArr):
            global msgImage
            if ("http" in img):
                #说明是网络图片，先下载到本地进行保存
                Path = "EmailPic/"+datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')+'-'+str(i)+'.jpg'
                urlretrieve(img,Path)
                imgfile = open(Path,'rb').read()
                msgImage = MIMEImage(imgfile)
            else:
                #本地图片，直接读取即可
                imgfile = open(img,'rb').read()
                msgImage = MIMEImage(imgfile)

            # 这句代码是关键，遍历图片数组时将每个图片都增加一个特定的标识
            msgImage.add_header("Content-ID", '<image{count}>'.format(count=i))
            msg.attach(msgImage)
            contentimg += "<p><img src='cid:image{count}'></p>".format(count=i)  # 给后面的正文增加图片
        #遍历完成之后将EmailPic文件夹内的所有文件都清空
        shutil.rmtree('EmailPic')
        os.mkdir('EmailPic')


        #遍历附件数组
        for i,localfile in enumerate(localfiles):

            localfilePath = localfile["path"]  # 邮件中的附件文件路径
            localfiletype = localfile["type"]  # 邮件中附件类型 img还是doc还是其他的
            locafiesuffix = localfile["suffix"]  # 邮件中附件的后缀，如果是图片的话是img还是png，如果是其他类型的话的后缀描述
            localfilename = localfile["name"]  # 邮件中附件文件的名称

            with open(localfilePath, 'rb') as f:

                # 设置附件的MIME和文件名，以及后缀格式:

                mime = MIMEBase(localfiletype, locafiesuffix, filename=localfilename)
                # 加上必要的头信息:
                mime.add_header('Content-Disposition', 'attachment', filename=localfilename)
                mime.add_header('Content-ID', '<file{count}>'.format(count=i))
                mime.add_header('X-Attachment-ID', '<file{count}>'.format(count=i))

                # 把附件内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)



        #设置邮件正文
        contentheader = "<html><body>"
        contenttext = textcontent
        contentfooter = "</body></html>"

        totalcontent = contentheader + contenttext + contentimg + contentfooter
        msg.attach(MIMEText(totalcontent,'html','utf-8'))

        #发送邮件
        server = smtplib.SMTP(fromsmtpserver,25)
        server.login(fromaddress,frompwd)
        server.sendmail(fromaddress,to_addrs,msg.as_string())
        server.quit()


#格式化邮件地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))






sendmailclass = SendMailClass()
sendmailclass.sendmail(
                        ["891508172@qq.com","3029068348@qq.com"],
                        "<h1 style='color: red'>幸福就是:~~</h1><h3>看你<span style='color: orange'>闹</span>,看你<span style='color: orange'>笑</span></h3>",
                        ["http://cdn.iciba.com/news/word/big_20171014b.jpg","http://cdn.iciba.com/news/word/big_20171012b.jpg"],
                        [{"path":"/Users/HelloWorld/Desktop/sky.jpg","type":"image","suffix":"jpg","name":"flower.jpg"}]
                       )



