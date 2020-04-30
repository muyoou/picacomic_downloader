import threading

class myThread (threading.Thread): 
    def __init__(self,tree_date,mypica,event):
        threading.Thread.__init__(self)
        self.tree_date=tree_date
        self.mpica=mypica
        self.page=event.getNowPage()
        self.event=event

    def run(self):
        if self.mpica.login() is 1:
            input("error")
        delList=self.tree_date.get_children()
        for item in delList:
            self.tree_date.delete(item)
        tmp=0
        #tmp2=1
        self.event.printl("获取收藏夹信息中...")
        #while True:
        self.mpica.getPage(self.page)
        #self.mpica.allInfo.extend(self.mpica.allComicInfo)
        for item in self.mpica.allComicInfo:
            self.tree_date.insert('',tmp,values=(item.get('title',''),item.get('author',''),item.get('likesCount',''),item.get('pagesCount',''),item.get('epsCount',''),'已下载'if item['download']else '未下载'))
            tmp+=1
        #if tmp2==self.mpica.pageNum:break
        #else:tmp2+=1
        #    break
        self.event.printl("收藏夹加载完成！")
        
class downThread (threading.Thread):
    def __init__(self,tree_date,mypica,event):
        threading.Thread.__init__(self)
        self.tree_date=tree_date
        self.mpica=mypica
        self.event=event
    def run(self):
        self.event.printl("开始下载")
        for item in self.tree_date.get_children():
            self.mpica.getNowPagePic()
            print(self.tree_date.item(item,"values"))