# encoding: utf-8
#特别注意,下面两行代码是专门为了Linux服务器上在不同目录文件中找到publicTool中的文件而写的,即在Linux环境下增加系统变量,不要忘记！！！
import json
import sys
sys.path.append("/var/www/html/python_projects/publicTools")
reload(sys)
sys.setdefaultencoding('utf8')


import itchat
import math
import PIL.Image as Image
import os
import shutil
import time

#用于检查登录状态时获取到的uuid 没有保存二维码图片的操作
def getuuid():
    uuid = itchat.get_QRuuid()
    while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
    return uuid

# 首先获取uuid
uuid = getuuid()
# 根据uuid获取到最新的二维码并打开
itchat.get_QR(uuid=uuid,picDir='QR.jpg')
#循环检查是否已经登录微信
while 1:

    # 首先先判断是否已经登录了微信,如果是已经登录了则直接break掉继续后面的操作即可
    status = itchat.check_login(uuid)  # 注意此处如果未登录,每次检查是否登录都需要32秒钟的时间
    print status

    if status == '200':
        # 登录成功
        userInfo = itchat.web_init()  # 切记如果使用二维码图片进行登录需要初始化该参数才能登录成功
        print ("登录成功")
        break
    elif status == '201':
        # 已经扫描二维码等待确认
        print ('已经扫描二维码,等待确认中……')
    elif status == '408':
        # 二维码已经失效 (如果是未登录,则经过32秒的检查时间会来到二维码失效的方法中)
        print "二维码失效,重新加载二维码"
        # 首先获取uuid
        uuid = getuuid()
        # 根据uuid获取到最新的二维码并打开
        itchat.get_QR(uuid=uuid, picDir='QR.jpg')


# itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='自动登录日志记录文件')

friends = itchat.get_friends(True)

user = friends[0].UserName
mynickname = friends[0].NickName

JsonStr = json.dumps(friends, ensure_ascii=False, encoding='UTF-8')
print "您的好友通讯录为:" + JsonStr

path1 = mynickname + '/所有微信好友的头像/'
path2 = mynickname + '/存储和读取头像集合/'
path3 = mynickname + '/头像大合照/'

try:
    # 删除存储和读取的文件夹
    shutil.rmtree(path1)

except:
    print '旧文件夹删除失败'

finally:
    os.makedirs(path1)

try:
    # 删除存储和读取的文件夹
    shutil.rmtree(path2)

except:
    print '旧文件夹删除失败'

finally:
    os.makedirs(path2)

try:
    # 删除存储和读取的文件夹
    shutil.rmtree(path3)
except:
    print '旧文件夹删除失败'

finally:
    os.makedirs(path3)






#下载所有好友的头像
for index,friend in enumerate(friends):
    img = itchat.get_head_img(userName=friend.UserName)
    RemarkName = friend.RemarkName if friend.RemarkName != '' else '无备注名称'
    NickName = friend.NickName

    print RemarkName +"   下载进度:"+ str(index+1) + "/" + str(len(friends))

    fileImage1 = open(path1 + str(index+1)+'-'+str(len(friends)) + ' ' + NickName +"("+ RemarkName + ")" + '.jpg','wb')
    fileImage1.write(img)
    fileImage1.close()

    fileImage2 = open(path2 + str(index) + '.jpg', 'wb')
    fileImage2.write(img)
    fileImage2.close()

#拿到下载的所有好友头像的文件目录
ls = os.listdir(path2)
each_size = int(math.sqrt(float(640*640)/len(ls)))#总共的面积除以图片个数等于一张图片的面积 开平方根为边长
lines = int(640/each_size)
image = Image.new('RGBA',(640,640))
x = 0
y = 0
#逐一拼接好友头像
for i in range(0,len(ls)+1):
    try:
        img = Image.open(path2 + str(i)+'.jpg')
    except IOError:
        print "读取第"+str(i)+"图片失败"
    else:
        img = img.resize((each_size,each_size),Image.ANTIALIAS)
        image.paste(img,(x*each_size,y*each_size))
        x += 1
        if x == lines:
            x = 0
            y += 1

#删除存储和读取的文件夹
shutil.rmtree(path1)
shutil.rmtree(path2)
image.save(path3 + 'all.jpg')
itchat.send_image(path3 + "all.jpg",'filehelper')

#退出登录
itchat.logout()
#退出程序
sys.exit()
