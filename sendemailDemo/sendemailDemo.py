# -*- coding: UTF-8 -*-



#发送附件邮件

#邮件对象
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))

def sendemail():

	from_addr = 'ioslhy@163.com'  # input('邮件发送自:')
	password = 'wyhhsh1993'  # input('密码:')
	to_addr = '891508172@qq.com'  # input('邮件发送给:')
	smtp_server = 'smtp.163.com'  # input('SMTP 服务器地址是:')

	msg = MIMEMultipart()
	msg['From'] = _format_addr('我是邮件发送人:%s' % from_addr)
	msg['To'] = _format_addr('邮件接收人:%s' % to_addr)
	msg['Subject'] = Header('这封邮件的主题是看你开心看你闹', 'utf-8').encode()

	# 邮件正文是MIMEText:
	msg.attach(MIMEText('<html><body><h1>给你发送一张图片叫做sunrise</h1>' +
						'<p><img src="cid:0"></p>' +
						'</body></html>', 'html', 'utf-8'))
	# 添加附件就是加上一个MIMEBase,从本地读取一个图片:
	with open('/Users/HelloWorld/Desktop/sky.jpg', 'rb') as f:
		# 设置附件的MIME和文件名，这里是jpg格式:
		mime = MIMEBase('image', 'jpg', filename='sky.jpg')
		# 加上必要的头信息:
		mime.add_header('Content-Disposition', 'attachment', filename='sky.jpg')
		mime.add_header('Content-ID', '<0>')
		mime.add_header('X-Attachment-ID', '0')

		# 把附件内容读进来:
		mime.set_payload(f.read())
		# 用Base64编码:
		encoders.encode_base64(mime)
		# 添加到MIMEMultipart:
		msg.attach(mime)
	# 发送
	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()


# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(sendemail,  'cron', day_of_week='0-6', hour=19, minute=18)
scheduler.start()





