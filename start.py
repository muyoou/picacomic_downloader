#from tkinter import Button,Label,Frame,StringVar,Scrollbar,Text,Tk,IntVar
from tkinter import *
from tkinter import ttk
import sys
import event
import mTreeList

root = Tk()
root.iconbitmap(".\\icon\\favicon.ico")
root.resizable(0,0)
root.title("哔咔收藏夹下载")
root.geometry("800x560")
root.protocol("WM_DELETE_WINDOW",event.close)

toolBar = Frame(root)
toolBar.pack(fill=X)
Button(toolBar,text="刷新",borderwidth=0,activeforeground="SkyBlue",padx=5,width=5,height=2,command=event.huoqu).pack(side=LEFT)
Button(toolBar,text="打开下载文件夹",borderwidth=0,activeforeground="SkyBlue",padx=5,height=2,command=event.openfolder).pack(side=LEFT)
Button(toolBar,text="设置",borderwidth=0,activeforeground="SkyBlue",padx=5,height=2,command=event.openMenu).pack(side=LEFT)
Button(toolBar,text="下载选中",borderwidth=0,activeforeground="SkyBlue",padx=5,height=2,command=event.downloadSelected).pack(side=LEFT)
Button(toolBar,text="关于",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.openAbout).pack(side=RIGHT)
tree_date=mTreeList.My_Tk(root)
pageSetBar=Frame(root)
pageSetBar.pack(fill=X)
Button(pageSetBar,text="上一页",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.previousPage).pack(side=LEFT)
PageT=StringVar()
PageT.set("第 页，共 页")
PageL=Label(pageSetBar,textvariable=PageT,padx=10)
PageL.pack(side=LEFT)
Button(pageSetBar,text="下一页",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.nextPage).pack(side=LEFT)
StopBtton=Button(pageSetBar,text="暂停下载",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.PauseDownload)
StartButton=Button(pageSetBar,text="继续下载",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.startDownload)
downloadNum=StringVar()
downloadNum.set("选中漫画后，点击[下载选中]开始下载")
Label(pageSetBar,textvariable=downloadNum,padx=100,fg='Gray').pack(side=LEFT)
DownloadStateList=(StopBtton,StartButton,downloadNum)

pageBar=Frame(root)
pageBar.place(relwidth=1,height=160,relx=1,rely=1,anchor="se")
logT=Text(pageBar,bg="black",fg="white")
logT.place(relwidth=1,height=150,relx=1,rely=1,anchor="se")
event.tree=tree_date
event.DownloadStateList=DownloadStateList
event.log=logT
event.root=root
event.page=PageT
event.mself=event

event.printl("下载程序初始化")
event.printl("v 1.0.0   BY MUYOO")
event.getPica()
event.checkConfig()
event.printl("配置完成")

event.download()
root.mainloop()