import d
import json
import post
import os
import time

class pica():

    def __init__(S,log):
        S.log=log
        S.printl("下载程序启动")
        S.printl("v 1.0.0   BY MUYOO")
        S.mrp=post.mrequest()
        S.mytoken='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1YmE5ZmFjMjFkYzM3YTY1NDk2ZTZhN2IiLCJlbWFpbCI6Im11eW9vIiwicm9sZSI6Im1lbWJlciIsIm5hbWUiOiJtdXlvbyIsInZlcnNpb24iOiIyLjIuMS4zLjMuNCIsImJ1aWxkVmVyc2lvbiI6IjQ1IiwicGxhdGZvcm0iOiJhbmRyb2lkIiwiaWF0IjoxNTg3OTczOTc0LCJleHAiOjE1ODg1Nzg3NzR9.Y_82vsuXloxDgBubns6dWMk8VRs8nXjnrDg7_uJFy4c'
        S.printl("尝试使用保存token登录")
        #S.mytoken=str(S.mrp.sendPost("auth/sign-in",{"email":d.Email,"password":d.Password},"POST").json()['data']['token'])
        print(S.mytoken)
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
        S.printl("初始化完成")
        S.printl("登录用户:"+d.Email)
        S.printl("图片下载质量:"+d.Image_quality)
        S.printl("代理设置:"+d.Proxy)
        

    def mkdir(self,path):
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path) 
            return True
        else:
            return False

    def isNone(self,input,other):
        if(not input):return other
        else : return input

    def getPage(self,index=None):
        index=self.isNone(index,self.index)
        tmp=self.mrp.sendPost("users/favourite?s=dd&page="+str(index),None,"GET",self.mytoken).json()['data']['comics']
        if self.pageNum==-1:
            self.pageNum=int(tmp['pages'])
        self.allComicInfo = tmp['docs']
        self.printl("已完成%d/%d"%(index,self.pageNum))

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
        self.mkdir(self.saveRootPath)
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
                                        if not (S.mkdir(savepath) or (temppage!=1)) : break
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

    def printl(self,text):
        self.log.insert('end',text+'\n')
        self.log.see('end')