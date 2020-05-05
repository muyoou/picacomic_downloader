import d
import fileManager
import setbox
import thread
import pica
import aboutme
import sys

log=None
root=None
page=None
tree=None
mself=None
mpica=None
threadaState=0
setboxState=0
aboutState=0
downloadThred=None

#获取pica类
def getPica():
    global mpica
    mpica=pica.pica(mself)

#-----日志交互-----

#打印信息到窗口日志
def printl(text):
    log.insert('end',text+'\n')
    log.see('end')

#-----列表控制-----
def insertList(data):
    tree.insert_tv(data)

#-----配置设置-----

#将配置导入全局设置
def setConfig(data):
    d.Email=data['user']
    d.Password=data['password']
    d.Proxy=data['proxy']
    d.Image_quality=data['quality']

#从配置文件中读取配置
def getConfigByFile():
    setConfig(fileManager.readConfig())

#打印所有配置到窗口日志
def printConfig():
    printl("----------------------")
    printl("用户名："+d.Email)
    printl("图片质量："+d.Image_quality)
    printl("代理设置："+d.Proxy)
    printl("----------------------")

#检查是否是初次启动，初始化配置文件
def checkConfig():
    if fileManager.isExist(".\\data\\config.json"):
        printl("加载配置文件")
        getConfigByFile()
        printConfig()
        huoqu(1)
    else:
        printl("初次配置")
        openMenu()
        printConfig()
    printl("加载日志")
    if fileManager.isExist('.\\data\\downloaded.json'):
        setDownloaded()
    else:
        fileManager.createJsonFile([],'downloaded.json')

#-----下载事务-----

#从下载记录中导入已下载的文件清单
def setDownloaded():
    d.Downloaded=fileManager.readDownloaded()

#从全局变量中上传到下载记录文件
def writeToDownFile():
    fileManager.updataDownloaded(d.Downloaded)

#添加已下载清单
def addDownloadedList(input):
    d.Downloaded.append(input)
    writeToDownFile()

#检查一个动漫id是否已经下载完成
def isDownloaded(input):
    if input in d.Downloaded:
        return True
    else: return False

#检查一个动漫是否在下载列表里
def isInDownloadList(input):
    for item in mpica.dolwnloadList:
        print("id信息："+item['_id'])
        if input==item['_id']:
            return True
    return False
    

#获取现在正在下载的漫画id
def getdowning():
    return d.Downloading

#-----页码交互-----

#设置窗口中的页码部分
def setPage(nowp,allp):
    d.nowPage=nowp
    d.AllPage=allp
    page.set("第%d页，共%d页"%(nowp,allp))

#获取当前的页码数
def getNowPage():
    return d.nowPage

#获取收藏夹的总页码数
def getAllPage():
    return d.AllPage

#更改当前页码数
def setNowPage(nowp):
    d.nowPage=nowp
    page.set("第%d页，共%d页"%(nowp,d.AllPage))

#-----错误处理-----
def checkError(input):
    if input==-1:
        printl("----------------\n连接超时！")
        return False
    elif input==-2:
        printl("----------------\n连接错误！请检查你的网络，是否能连接到哔咔服务器")
        printl("建议使用VPN或者在设置中配置代理")
        return False
    elif input==-3:
        printl("----------------\n代理错误！请检查设置中的代理设置。如不需要代理，请保持空值")
        return False
    else: return True

#-----事件方法-----

#打开下载文件夹
def openfolder():
    fileManager.openFile(".\\comic")

#打开设置窗口
def openMenu():
    if setboxState==0:
        setbox.setbox(root,mself)

#获取index页的漫画列表
def huoqu(index=0):
    if threadaState==1:
        printl('请等待页面加载完成...')
    else:
        if index!=0:
            setNowPage(index)
        thread1=thread.myThread(tree,mpica,mself)
        thread1.start()

#下一页
def nextPage():
    tem=getNowPage()
    if(tem<getAllPage()):
        huoqu(tem+1)

#上一页
def previousPage():
    tem=getNowPage()
    if(tem>1):
        huoqu(tem-1)

#打开关于窗口
def openAbout():
    if aboutState==0:
        aboutme.about(root,mself)


#启动下载线程
def download():
    global downloadThred
    thread1=thread.downThread(mpica,mself)
    thread1.start()
    downloadThred=thread1

#下载此页
def downloadPage():
    mpica.putNowPagePicToList()

#刷新列表下载状态
def refresh():
    for item in tree.getTree().get_children():
        tem=tree.getTree().set(item,'id')
        print(tem)
        print()
        if tem==getdowning(): 
            tree.getTree().set(item,'状态','下载中...')
        elif isDownloaded(tem):
            tree.getTree().set(item,'状态','已下载')
        elif isInDownloadList(tem):
            tree.getTree().set(item,'状态','等待下载')
        else:
            tree.getTree().set(item,'状态','未下载')

def close():
    downloadThred.stop()
    root.destroy()