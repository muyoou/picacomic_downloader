import threading
import time

class myThread (threading.Thread): 
    def __init__(self,tree_date,mypica,event):
        threading.Thread.__init__(self)
        self.tree_date=tree_date
        self.mpica=mypica
        self.page=event.getNowPage()
        self.event=event

    def run(self):
        self.event.threadaState=1
        if self.mpica.login() == 1:
            input("error")
        '''
        delList=self.tree_date.get_children()
        for item in delList:
            self.tree_date.delete(item)
            '''
        #tmp=0
        #tmp2=1
        self.event.printl("获取收藏夹信息中...")
        #while True:
        self.mpica.getPage(self.page)
        #self.mpica.allInfo.extend(self.mpica.allComicInfo)
        self.event.insertList(self.mpica.allComicInfo)
        '''
        for item in self.mpica.allComicInfo:
            self.tree_date.insert('',tmp,values=(item.get('_id',''),item.get('title',''),item.get('author',''),item.get('likesCount',''),item.get('pagesCount',''),item.get('epsCount',''),''))
            tmp+=1
        '''
        #if tmp2==self.mpica.pageNum:break
        #else:tmp2+=1
        #    break
        self.event.refresh()
        self.event.threadaState=0
        self.event.printl("收藏夹加载完成！")
        
class downThread (threading.Thread):
    def __init__(self,mypica,event):
        threading.Thread.__init__(self)
        self.mpica=mypica
        self.event=event
        self._stop_event = threading.Event()
    def run(self):
        while True:
            time.sleep(1)
            if self.event.isStartDownload==1:
                if len(self.mpica.dolwnloadList)!=0:
                    self.mpica.downloadFirstComic()
            if self.stopped():
                break

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
        
'''
class refreshThread(threading.Thread):
    def __init__(self,tree,event,downing='',downed=[]):
        threading.Thread.__init__(self)
        self.tree_date=tree
        self.event=event
        self.downing=downing
        self.downed=downed
    def run(self):
'''