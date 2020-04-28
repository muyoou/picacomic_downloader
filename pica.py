import d
import json
import post
import fileManager
import time

class pica():

    def __init__(S,event):
        S.event=event
        S.mrp=post.mrequest()
        S.allInfo = []
        S.allComicInfo = None
        S.comicInfo= None
        S.allCPageInfo = None
        S.cPageInfo = None
        S.allEpsInfo = None
        S.epsInfo = None
        S.pageNum = -1
        S.index = 0
        S.epsID = 0
        S.temID = 0
        S.saveRootPath = None
        S.savePath = None
        S.event.printl("初始化完成")

    def login(self):
        self.event.printl("开始登录")
        if self.loginByFile()!=0:
            self.loginByWeb()

    def loginByFile(self):
        if fileManager.isExist(".\\data\\token.dat"):
            self.event.printl('使用token登录')
            self.mytoken=fileManager.readToken()
            self.event.printl("已获取token，尝试登陆中...")
            print (self.mytoken)
            return self.testConn()
        else: return 1


    def loginByWeb(self):
        self.event.printl('尝试使用密码登录中...')
        output=self.mrp.sendPost("auth/sign-in",{"email":d.Email,"password":d.Password},"POST").json()
        print(output)
        if output['message'] == 'invalid email or password':
            self.event.printl("用户名或密码错误！请在设置中更改")
            return 1
        else:
            self.event.printl("登录成功！")
            self.mytoken=str(output['data']['token'])
            fileManager.creatTokenFile(self.mytoken)
            self.event.printl("token已保存")
            return 0

    def testConn(self):
        if self.mrp.sendPost("categories",None,"GET",self.mytoken) == -1:
            self.event.printl("登录超时！")
            return -1
        else:
            self.event.printl("登录成功！")
            return 0

    def isNone(self,input,other):
        if(not input):return other
        else : return input

    def getPage(self,index=None):
        index=self.isNone(index,self.index)
        tmp=self.mrp.sendPost("users/favourite?s=dd&page="+str(index),None,"GET",self.mytoken).json()['data']['comics']
        if self.pageNum==-1:
            self.pageNum=int(tmp['pages'])
        self.allComicInfo = tmp['docs']
        self.event.printl("已完成%d/%d"%(index,self.pageNum))

    def getComicEps(self,comicid=None):
        comicid=self.isNone(comicid,self.comicInfo['_id'])
        return self.mrp.sendPost("comics/"+str(comicid)+"/eps?page=1",None,"GET",self.mytoken).json()['data']['eps']['docs']

    def getCPage(self,temppage=None,comicid=None,epsid=None):
        comicid=self.isNone(comicid,self.comicInfo['_id'])
        epsid=self.isNone(epsid,self.epsID)
        temppage=self.isNone(temppage,self.temID)
        return self.mrp.sendPost("comics/"+str(comicid)+"/order/"+str(epsid)+"/pages?page="+str(temppage),None,"GET",self.mytoken).json()['data']['pages']

    def getPic(self,picture,savepath):
        print(str(picture['fileServer'])+"/static/"+str(picture['path']))
        return self.mrp.sendPost(str(picture['fileServer'])+"/static/"+str(picture['path']),savepath,"img",self.mytoken)

    def getPicSavePath(self,root,id,info):
        return root+"/"+str(id)+"_"+str(info['originalName'])

    def get40Pic(self):
        picnum=(self.temID-1)*40+1
        for picture in self.allCPageInfo['docs']:
            print('-下载 '+str(picnum)+'/'+str(self.allCPageInfo['total'])+' -- '+str(picture['media']['originalName']))
            #pic=self.getPic(picture['media'],self.getPicSavePath(self.saveRootPath,picnum,picture['media']))
            picnum+=1

    def getEpsPic(self):
        self.saveRootPath=self.getComicSavePath()
        fileManager.mkdir(self.saveRootPath)
        self.temID=1
        while True:
            self.allCPageInfo=self.getCPage()
            self.get40Pic()
            if int(self.allCPageInfo['pages'])==self.temID:break
            else : self.temID+=1

    def getComicSavePath(self,comic=None,eps=None,id=None):
        comic=self.isNone(comic,self.comicInfo)
        eps=self.isNone(eps,self.epsInfo)
        id=self.isNone(id,self.index)
        return "./comic/"+str(id)+'_'+str(comic['title'])+"/"+str(eps['title']);

    def getComicPic(self):
        for self.epsInfo in self.allEpsInfo:
            self.epsID=self.epsInfo["order"]
            self.getEpsPic()


    def start2(S):
        S.index=1
        S.getPage()
        S.comicInfo=S.allComicInfo[0]
        S.allEpsInfo=S.getComicEps()
        S.getComicPic()
        
        


    def start(S):
        for S.index in range(1,2):
                print('\n')
                print('开始下载收藏夹第'+str(S.index)+'页的内容。。。')
                for S.comicInfo in S.getPage():
                       print('～正在下载第'+str(S.index)+'页本子：'+str(S.comicInfo['title']))
                       epsnum=1
                       for S.epsInfo in S.getComicEps():
                                print('章节:'+str(S.epsInfo['title'])+"\n---------------------------------------\n")
                                temppage=1
                                while True:
                                        S.cPageInfo=S.getCPage(temppage)
                                        total=S.cPageInfo['total']
                                        savepath=S.getComicSavePath(S.comicInfo,S.epsInfo,S.index);
                                        if not (fileManager.mkdir(savepath) or (temppage!=1)) : break
                                        picnum=(temppage-1)*40+1
                                        for picture in S.cPageInfo['docs']:
                                                print('-下载 '+str(picnum)+'/'+str(total)+' -- '+str(picture['media']['originalName']))
                                                pic=S.getPic(picture['media'],S.getPicSavePath(savepath,picnum,picture['media']))
                                                picnum+=1
                                        if int(S.cPageInfo['pages'])==temppage:break
                                        else : temppage+=1
                                print('此章节下载完成\n---------------------------------------\n')
                                if epsnum>=5 :break
                                epsnum+=1
                       print("～此本子下载完成")
                       time.sleep(3)
                print('\n\n这一页下载完成\n\n')
                time.sleep(3)