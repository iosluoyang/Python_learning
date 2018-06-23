#coding:utf8
import os

def rename():

        path="/Users/HelloWorld/Desktop/Level6"
        filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）

        i = 0
        for files in filelist:#遍历所有文件

            i=i+1

            #分离文件名与扩展名 得到文件名
            originalfilename=os.path.splitext(files)[0]

            #如果文件名中有-空格的字符串的话则将其后面的名称拿出来  如果没有的话则直接忽略
            if "- " in originalfilename:

                #拿到要保留的名称
                filename = originalfilename.split("- ")[1]

                #文件扩展名
                filetype = os.path.splitext(files)[1]

                #新文件名称
                newName = path.split('/')[-1] + "_" + str(i) + "_" + filename + filetype

                Olddir = os.path.join(path, files)  # 链接目录与文件名 获取原来的文件路径

                Newdir = os.path.join(path, newName)  # 新的文件路径

                # 重命名
                os.rename(Olddir,Newdir)


rename()