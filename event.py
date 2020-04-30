import d
import fileManager
import setbox
import thread
import pica

class event():
    def __init__(self,log,root,page,tree):
        self.log=log
        self.root=root
        self.page=page
        self.tree=tree
        self.pica=pica.pica(self)

    #打印信息到窗口日志
    def printl(self,text):
        self.log.insert('end',text+'\n')
        self.log.see('end')

    #将配置导入全局设置
    def setConfig(self,data):
        d.Email=data['user']
        d.Password=data['password']
        d.Proxy=data['proxy']
        d.Image_quality=data['quality']

    #从配置文件中读取配置
    def getConfigByFile(self):
        self.setConfig(fileManager.readConfig())

    #从下载记录中导入已下载的文件清单
    def setDownloaded(self):
        d.Downloaded=fileManager.readDownloaded()

    #打印所有配置到窗口日志
    def printConfig(self):
        self.printl("----------------------")
        self.printl("用户名："+d.Email)
        self.printl("图片质量："+d.Image_quality)
        self.printl("代理设置："+d.Proxy)
        self.printl("----------------------")

    #打开设置窗口
    def openMenu(self):
        setbox.setbox(self.root)

    #检查是否是初次启动，初始化配置文件
    def checkConfig(self):
        if fileManager.isExist(".\\data\\config.json"):
            self.printl("加载配置文件")
            self.getConfigByFile()
            self.printConfig()
        else:
            self.printl("初次配置")
            self.openMenu()
            self.printConfig()
        self.printl("加载日志")
        if fileManager.isExist('.\\data\\downloaded.json'):
            self.setDownloaded()
        else:
            fileManager.createJsonFile([],'downloaded.json')

    #检查一个动漫id是否已经下载完成
    def isDownloaded(self,input):
        if input in d.Downloaded:
            return True
        else: return False

    #设置窗口中的页码部分
    def setPage(self,nowp,allp):
        d.nowPage=nowp
        d.AllPage=allp
        self.page.set("第%d页，共%d页"%(nowp,allp))

    #获取当前的页码数
    def getNowPage(self):
        return d.nowPage

    #获取收藏夹的总页码数
    def getAllPage(self):
        return d.AllPage

    #更改当前页码数(形式更改)
    def setNowPage(self,nowp):
        d.nowPage=nowp
        self.page.set("第%d页，共%d页"%(nowp,d.AllPage))

    #打开下载文件夹
    def openfolder(self):
        fileManager.openFile(".\\comic")

    def huoqu(self,index=0):
        if index!=0:
            self.setNowPage(index)
        thread1=thread.myThread(self.tree,self.pica,self)
        thread1.start()

    def nextPage(self):
        tem=self.getNowPage()
        if(tem<self.getAllPage()):
            self.huoqu(tem+1)

    def previousPage(self):
        tem=self.getNowPage()
        if(tem>1):
            self.huoqu(tem-1)

    def download(self):
        thread1=thread.downThread(self.tree,self.pica,self)
        thread1.start()