# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import sys
sys.path.append("/var/www/html/python_projects/publicTools")
reload(sys)
sys.setdefaultencoding('utf8')


import itchat
import math
import PIL.Image as Image
import os

itchat.auto_login(enableCmdQR=2, hotReload=True)
friends = itchat.get_friends(update=True)[0:]
user = friends[0]["UserName"]

num = 0
for i in friends:
    img = itchat.get_head_img(userName=i["UserName"])
    RemarkName = i["RemarkName"]
    fileImage1 = open('文件夹' + "/" + str(num) + ".jpg",'wb')
    fileImage2 = open('所有微信好友的头像集合' + '/' + RemarkName + '_'+ str(num)+ '.jpg','wb')
    fileImage1.write(img)
    fileImage2.write(img)
    fileImage1.close()
    fileImage2.close()
    num += 1

ls = os.listdir("文件夹")
each_size = int(math.sqrt(float(640*640)/len(ls)))
lines = int(640/each_size)
image = Image.new('RGBA',(640,640))
x = 0
y = 0
for i in range(0,len(ls)+1):
    try:
        img = Image.open('文件夹'+'/'+str(i)+'.jpg')
    except IOError:
        print "读取第"+str(i)+"图片失败"
    else:
        img = img.resize((each_size,each_size),Image.ANTIALIAS)
        image.paste(img,(x*each_size,y*each_size))
        x += 1
        if x == lines:
            x = 0
            y += 1
image.save('文件夹'+'/'+'all.jpg')
itchat.send_image('文件夹' + "/" + "all.jpg", 'filehelper')
