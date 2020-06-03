import d
import json
import post
import fileManager
import time

class pica():

    def __init__(S,event):
        #event类，在这里主要用于打印信息到窗口控制台
        S.event=event
        #mrequest类，用于发送请求
        S.mrp=post.mrequest()
        #记录曾获取到的所有的漫画信息
        S.allInfo = []
        #记录当前收藏页里的所有漫画信息
        S.allComicInfo = None
        #记录当前漫画的详细信息
        S.comicInfo= None
        #记录当前漫画分页里的所有图片详细信息
        S.allCPageInfo = None
        #已废除
        S.cPageInfo = None
        #记录当前漫画的所有章节
        S.allEpsInfo = None
        #记录当前章节的信息，是allEpsInfo的子类
        S.epsInfo = None
        #当前浏览的页数
        S.pageNum = -1
        #当前页中浏览的漫画是第几个
        S.index = 0
        #当前的章数
        S.epsID = 0
        #当前的图片分页数
        S.temID = 0
        #当前漫画的保存路径
        S.saveRootPath = None
        #当前图片的保存路径
        S.savePath = None
        #下载列表
        S.dolwnloadList=[]
        S.event.printl("初始化完成")

    #用于尝试使用token和密码登录
    def login(self):
        self.event.printl("验证登录")
        if self.loginByFile()!=0:
            self.loginByWeb()

    #使用保存的token文件登录
    def loginByFile(self):
        if fileManager.isExist(".\\data\\token.dat"):
            self.mytoken=fileManager.readToken()
            #return self.testConn()
            return 0
        else: return 1

    #使用密码登录，并保存token
    def loginByWeb(self):
        self.event.printl('尝试使用密码登录中...')
        output=self.mrp.sendPost("auth/sign-in",{"email":d.Email,"password":d.Password},"POST")
        if not self.event.checkError(output):
            self.event.printl("将在5秒后重试")
            time.sleep(5)
            self.loginByWeb()
        else:
            output=output.json()
        try:
            if output['message'] == 'invalid email or password':
                self.event.printl("-------------\n用户名或密码错误！请在设置中更改")
                return 1
            else:
                self.event.printl("登录成功！")
                self.mytoken=str(output['data']['token'])
                fileManager.creatTokenFile(self.mytoken)
                self.event.printl("token已保存")
                return 0
        except TypeError:
            self.login()

    #测试能否连接，-1为失败，0为成功
    def testConn(self):
        if self.mrp.sendPost("categories",None,"GET",self.mytoken) == -1:
            self.event.printl("登录超时！")
            return -1
        else:
            self.event.printl("登录成功！")
            return 0

    #用来检测input值是否为空，是则返回other值
    def isNone(self,input,other):
        if(not input):return other
        else : return input

    #用来检测漫画名中是否有非法字符，是则替换
    def haveIllegalChar(self,input):
        return input.replace("\\", "").replace("/","").replace(":", "").replace("*", "").replace("?", "").replace("\"","").replace("<","").replace(">","").replace("|","").replace(" ","")

    #获取这一页的收藏夹里的所有漫画信息，并导出到allComicInfo
    def getPage(self,index=None):
        index=self.isNone(index,self.index)
        tmp=self.mrp.sendPost("users/favourite?s=dd&page="+str(index),None,"GET",self.mytoken)
        if not self.event.checkError(tmp):
            self.event.printl("将在5秒后重试")
            time.sleep(5)
            self.getPage(index)
        else:
            tmp=tmp.json()['data']['comics']
        if self.pageNum==-1:
            self.pageNum=int(tmp['pages'])
        try:
            self.allComicInfo = tmp['docs']
        except TypeError:
            self.getPage(index)
        for item in self.allComicInfo:
            if self.event.isDownloaded(item['_id']):
                item['download']=True
            else:
                item['download']=False
        self.event.setPage(index,self.pageNum)
        self.event.printl("第%d页加载完成"%(index))

    #获取一个漫画的章节列表
    #可以通过comicid获取，也可以直接使用当前的漫画号
    def getComicEps(self,comicid=None):
        comicid=self.isNone(comicid,self.comicInfo['_id'])
        firstEps=self.mrp.sendPost("comics/"+str(comicid)+"/eps?page=1",None,"GET",self.mytoken).json()['data']['eps']
        epsNum=firstEps["total"]
        firstEps=firstEps['docs']
        pageItem=2
        while True:
            if epsNum>40:
                firstEps+=self.mrp.sendPost("comics/"+str(comicid)+"/eps?page="+str(pageItem),None,"GET",self.mytoken).json()['data']['eps']['docs']
                pageItem+=1
                epsNum-=40
            else:break
        return firstEps

    #获取comicid所示漫画的epsid章节的temppage分页中的所有图片信息
    def getCPage(self,temppage=None,comicid=None,epsid=None):
        comicid=self.isNone(comicid,self.comicInfo['_id'])
        epsid=self.isNone(epsid,self.epsID)
        temppage=self.isNone(temppage,self.temID)
        return self.mrp.sendPost("comics/"+str(comicid)+"/order/"+str(epsid)+"/pages?page="+str(temppage),None,"GET",self.mytoken).json()['data']['pages']

    #通过图片信息下载图片
    def getPic(self,picture,savepath):
        if self.event.isStartDownload==0:
            self.event.printl('下载已暂停')
            while True:
                time.sleep(1)
                if self.event.isStartDownload==1:
                    break
        if not fileManager.isExist(savepath):
            return self.mrp.sendPost(str(picture['fileServer'])+"/static/"+str(picture['path']),savepath,"img",self.mytoken)
        else:
            return 1

    #获取一张图片的保存路径及文件名
    def getPicSavePath(self,root,id,info):
        return root+"/"+str(id)+"_"+str(info['originalName'])

    #直接下载一个分页中的所有图片
    def get40Pic(self):
        picnum=(self.temID-1)*40+1
        for picture in self.allCPageInfo['docs']:
            self.event.printl('- '+str(picnum)+'/'+str(self.allCPageInfo['total'])+' -- '+str(picture['media']['originalName']))
            self.getPic(picture['media'],self.getPicSavePath(self.saveRootPath,picnum,picture['media']))
            picnum+=1

    #直接下载一个章节中的所有图片
    def getEpsPic(self):
        self.saveRootPath=self.getComicSavePath()
        fileManager.mkdir(self.saveRootPath)
        self.temID=1
        while True:
            self.allCPageInfo=self.getCPage()
            self.get40Pic()
            if int(self.allCPageInfo['pages'])==self.temID:break
            else : self.temID+=1

    #获取这个漫画的保存路径
    def getComicSavePath(self,comic=None,eps=None,id=None):
        comic=self.isNone(comic,self.comicInfo)
        eps=self.isNone(eps,self.epsInfo)
        id=self.isNone(id,self.index)
        return "./comic/"+self.haveIllegalChar(str(comic['title']))+"/"+self.haveIllegalChar(str(eps['title']))

    #直接下载一个漫画中的所有图片
    def getComicPic(self):
        self.event.printl("开始下载："+self.comicInfo['title'])
        for self.epsInfo in self.allEpsInfo:
            self.epsID=self.epsInfo["order"]
            self.getEpsPic()
        self.event.addDownloadedList(self.comicInfo['_id'])
        self.event.printl("此漫画下载完成！")

    #将当前页的漫画添加到下载列表
    def putNowPagePicToList(self):
        for item in self.allComicInfo:
            if not self.event.isDownloaded(item['_id']) and not item in self.dolwnloadList:
                self.dolwnloadList.append(item)

    #将选中的添加到下载列表
    def putSelectPicToList(self,data):
        for item in data:
            selectComic=self.allComicInfo[item-1]
            if not self.event.isDownloaded(selectComic['_id']) and not selectComic in self.dolwnloadList and not selectComic == self.comicInfo:
                self.dolwnloadList.append(selectComic)
            else:
                self.event.printl('已存在或者正在下载：'+selectComic['title'])
        self.event.printl('已经添加到下载列表！')
                

    #下载列表中的第一个漫画
    def downloadFirstComic(self):
        self.comicInfo=self.dolwnloadList[0]
        self.event.fristStartDownload()
        d.Downloading=self.comicInfo['_id']
        self.event.refresh()
        self.allEpsInfo=self.getComicEps()
        self.getComicPic()
        d.Downloading=''
        self.dolwnloadList.pop(0)
        self.event.finishDownload()
        self.event.refresh()

'''
    #下载下载列表里的所有漫画
    def getListPic(self):
        for self.comicInfo in self.dolwnloadList:
            d.Downloading=self.comicInfo['_id']
            self.allEpsInfo=self.getComicEps()
            self.getComicPic()

    #示例：下载第一页的第一个漫画
    def start2(self):
        self.index=1
        self.getPage()
        self.comicInfo=S.allComicInfo[0]
        self.allEpsInfo=S.getComicEps()
        self.getComicPic()
'''