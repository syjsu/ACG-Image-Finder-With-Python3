# -* - coding: UTF-8 -* -
import urllib.request
import os
import threading
import json
import socket
import time
import re
import ssl
from  threading import Timer
import enum
import tkinter as tk


# #建立线程池，并启动线程直到结束
def parallel(infos, downloadFile):
    startTime = time.time()
    threads = []
    counts = range(len(infos))
    for i in counts:
        t = MyThread(downloadImage, (infos[i], downloadFile,), downloadImage.__name__)
        threads.append(t)
    for i in counts:
        threads[i].start()
    for i in counts:
        threads[i].join()
    print('花费时间:%s' % (time.time() - startTime))


# #自定义线程类
class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.res = self.func(*self.args)


# # #单线程测试
# def parallel(infos,downloadFile):
#     counts = range(len(infos))
#     for i in counts:
#         downloadImage(infos[i],downloadFile)
#     print("OK")

# 根绝imageUrl下载图片到本地
def downloadImage(info, downloadFile):
    imageUrl = info["url"]
    imagePName = str(info["pname"])
    imageCName = str(info["cname"])
    dir = "./" + downloadFile + "/" + imagePName + "/"

    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            print("创建目录成功 %s" % dir)
    except Exception as e:
        print("创建目录失败 %s" % dir, e)
        return

    imageType = imageUrl.split('.')[-1]
    path = dir + imageCName + "." + imageType
    if os.path.exists(path):
        print(imageCName + "文件已存在")
        return
    else:
        print(imageCName + "文件不存在")
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            data = urllib.request.urlopen(urllib.request.Request(url=imageUrl,headers=headers),context=gcontext).read()
        except Exception as e:
            print("下载失败", e)
            return
        try:
            f = open(path, "wb")
            f.write(data)
            f.close()
            print("保存成功" + path)
        except Exception as e:
            print("保存失败", e)
            return


# 下载整个相册
def downloadAlbum(albumName, albumIndex, downloadUrl, downloadFile):
    reqs = []
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        res = urllib.request.urlopen(url = urllib.request.Request(downloadUrl +"/list.json?cat="+ albumIndex +"&no-sexy=no&pro=yes&user=yes&version=a.1.2", headers=headers))
        res = res.read().decode("utf-8",'ignore')
        res = str(res)
        resAlbum = json.loads(res)
    except Exception as e:
        print("获取专辑信息失败", e)
        return
    for Album in resAlbum['data']:
        print(" 文件ID：" + str(Album['id']) + " 下载地址：" + Album['tid'])
        a = {}
        a['pname'] = albumName
        a['cname'] = str(Album['id'])
        a['url'] = "https://t750.antendan.in/"+str(Album['tid'])
        reqs.append(a)
    parallel(reqs, downloadFile)
    save("./" + downloadFile + "/" + albumName + "/" + "info.json", resAlbum)


# 获取专辑信息
def downloadIndex(downloadUrl, downloadFile):
    fileFolder = "./" + downloadFile + "/"
    if not os.path.exists(fileFolder):
        os.mkdir(fileFolder)
    timeout = 10
    socket.setdefaulttimeout(timeout)

    try:
        print(downloadUrl + "/tags.json?no-sexy=no&pro=yes&user=yes&version=a.1.2")
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        res = urllib.request.urlopen(urllib.request.Request(url=downloadUrl + "/tags.json?no-sexy=no&pro=yes&user=yes&version=a.1.2", headers=headers))
        res =  res.read().decode("utf-8",'ignore')
        res = str(res)
        resAlbum = json.loads(res)
        print(resAlbum)
    except Exception as e:
        print("获取索引失败", e)
        exit(404)
        return

    for Album in resAlbum['tags']:
        print("开始下载专辑" + Album['name'] + " 索引是：" + str(Album['id']) + "数量是: "+ str(Album['count']))
        # 专辑名
        AlbumName = re.sub("[\s+\.\!\/_,$%^*+\"\']+|[+——！，。？、~@#￥%……&*（）:：]+", "-", Album['name'])
        # 下载专辑
        downloadAlbum(AlbumName, str(Album['id']), downloadUrl, downloadFile)

    save("./" + downloadFile + "/" + "info.json", resAlbum)
    print("结束任务")


# 保存文件到本地
def save(filename, contents):
    try:
        r =json.dumps(contents, sort_keys=True, indent=2, ensure_ascii=False)
        fh=open(filename, 'w')
        fh.write(r)
        fh.close()
    except Exception as e:
        print(e)

# 主程序
if __name__ == "__main__":
    # 下载地址
    downloadUrl = "http://hezi.antendan.in"
    # 下载文件夹
    downloadFile = "Hezi"
    # 线程任务
    downloadIndex(downloadUrl, downloadFile)

    print("结束")
