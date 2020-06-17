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
screenWidth=root.winfo_screenwidth()
screenHeight=root.winfo_screenheight()
x=(screenWidth-800)/2
y=(screenHeight-560)/2
root.geometry("800x560+%d+%d"%(x,y))
root.protocol("WM_DELETE_WINDOW",event.close)

toolBar = Frame(root)
toolBar.pack(fill=X)
downloadIcon=PhotoImage(file=".\\icon\\download.gif")
refreshIcon=PhotoImage(file=".\\icon\\refresh.gif")
cancerIcon=PhotoImage(file=".\\icon\\close.gif")
infoIcon=PhotoImage(file=".\\icon\\info.gif")
filterIcon=PhotoImage(file=".\\icon\\filter.gif")
imageIcon=PhotoImage(file=".\\icon\\image.gif")
Button(toolBar,text="刷新",borderwidth=0,activeforeground="LightCoral",padx=5,height=40,command=event.huoqu,image=refreshIcon,compound=LEFT).pack(side=LEFT)
Button(toolBar,text="已下载",borderwidth=0,activeforeground="LightCoral",padx=9,height=10,command=event.openfolder,image=imageIcon,compound=LEFT).pack(side=RIGHT)
Button(toolBar,text="设置",borderwidth=0,activeforeground="LightCoral",padx=5,height=10,command=event.openMenu,image=filterIcon,compound=LEFT).pack(side=RIGHT)
Button(toolBar,text="下载",borderwidth=0,activeforeground="LightCoral",padx=5,height=10,command=event.downloadSelected,image=downloadIcon,compound=LEFT).pack(side=LEFT)
Button(toolBar,text="取消下载",borderwidth=0,activeforeground="LightCoral",padx=5,height=10,command=event.downloadSelected,image=cancerIcon,compound=LEFT).pack(side=LEFT)
Button(toolBar,text="关于",borderwidth=0,activeforeground="LightCoral",padx=10,height=10,command=event.openAbout,image=infoIcon,compound=LEFT).pack(side=RIGHT)
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