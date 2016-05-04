import os
Const_Image_Format = [".jpg",".jpeg",".bmp",".png",".gif",".GIF",".JPG",".json"]
Const_File_Format = [".json",".py",".idea",".pyc",".iml",".xml",".name"]
rootDir = "./"

limit_size = 1*1024  #图片大小限制，30K


class FileFilt:
    deleted = 0
    def __init__(self):
        pass
    def FilterFile(self, dirr):
        for parent,dirnames,filenames in os.walk(rootDir):
            for filename in filenames :
                fileDir = os.path.join(parent,filename)
                if fileDir and (os.path.splitext(fileDir)[1] in Const_Image_Format ):
                    filesize = os.path.getsize(fileDir)
                    if (filesize <= limit_size):
                        print("删除太小的文件"+fileDir+"文件大小"+str(os.path.getsize(fileDir)))
                        os.remove(fileDir)
                        self.deleted+=1
                    else:
                        pass
                else:
                    if fileDir and (os.path.splitext(fileDir)[1] not in Const_File_Format ):
                        print("删除格式不对的文件" + fileDir)
                        os.remove(fileDir)
                        self.deleted+=1
                    else:
                        pass



# 删除空文件夹
def delete_null_dir(dirr):
    if os.path.isdir(dirr):
        for p in os.listdir(dirr):
            d  = os.path.join(dirr,p)
            if (os.path.isdir(d) == True):
                delete_null_dir(d)
    if not os.listdir(dirr):
        os.rmdir(dirr)
        print('移除空目录: ', dirr)

if __name__ == "__main__":

    b = FileFilt()
    b.FilterFile(dirr = rootDir)
    print("===开始删除文件===")
    print ('删除个数 : ',b.deleted)
    print("===结束删除文件===")

    print ("===开始删除空文件夹===")
    delete_null_dir(rootDir)
    print ("===结束删除空文件夹===")
