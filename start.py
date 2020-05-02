from tkinter import * 
from tkinter import ttk

import event

root = Tk()
root.iconbitmap(".\\icon\\favicon.ico")
root.resizable(0,0)



root.title("哔咔收藏夹下载") 
root.geometry("800x560")
 
toolBar = Frame(root).place(relwidth=1,x=0,y=0)
Button(toolBar,text="刷新",borderwidth=0,activeforeground="SkyBlue",command=event.huoqu).place(x=0,y=0,height=35,width=50)
Button(toolBar,text="下载此页",borderwidth=0,activeforeground="SkyBlue",command=event.downloadPage).place(x=55,y=0,height=35,width=50)
Button(toolBar,text="打开文件夹",borderwidth=0,activeforeground="SkyBlue",command=event.openfolder).place(x=120,y=0,height=35,width=60)
Button(toolBar,text="设置",borderwidth=0,activeforeground="SkyBlue",command=event.openMenu).place(x=190,y=0,height=35,width=50)
Button(toolBar,text="关于",borderwidth=0,activeforeground="SkyBlue").place(relx=1,y=0,height=35,width=50,anchor="ne")
Button(root,text="上一页",borderwidth=0,activeforeground="SkyBlue",command=event.previousPage).place(x=20,y=355)
Button(root,text="下一页",borderwidth=0,activeforeground="SkyBlue",command=event.nextPage).place(x=180,y=355)
PageT=StringVar()
PageT.set("第 页，共 页")
PageL=Label(root,textvariable=PageT)
PageL.place(x=80,y=358)
sb = Scrollbar(root)
table=Frame(root).place(relwidth=1,x=0,y=35)

tree_date = ttk.Treeview(table,show="headings",yscrollcommand= sb.set)
sb.config(command=tree_date.yview)
sb.place(relx=1,y=35,anchor="ne",width=20,height=320)
# 定义列
tree_date['columns'] = ['id','name','creater','likesCount','pagesCount','epsCount',"download"]
tree_date.place(x=0,y=35,width=780,height=320)


# 设置列宽度
tree_date.column('id',width=0)
tree_date.column('name',width=200)
tree_date.column('creater',width=100)
tree_date.column('pagesCount',width=30)
tree_date.column('epsCount',width=30)
tree_date.column('likesCount',width=30)
tree_date.column('download',width=50)
# 添加列名
tree_date.heading('id',text='ID')
tree_date.heading('name',text='名称')
tree_date.heading('creater',text='作者')
tree_date.heading('pagesCount',text='页数')
tree_date.heading('epsCount',text='章节数')
tree_date.heading('likesCount',text='点赞数')
tree_date.heading('download',text='状态')
# 给表格中添加数据
pageBar=Frame(root)
pageBar.place(relwidth=1,height=160,relx=1,rely=1,anchor="se")
logT=Text(pageBar,bg="black",fg="white")
logT.place(relwidth=1,height=150,relx=1,rely=1,anchor="se")

event.tree=tree_date
event.log=logT
event.root=root
event.page=PageT
event.mself=event

event.printl("下载程序初始化")
event.printl("v 1.0.0   BY MUYOO")
event.checkConfig()
event.printl("配置完成")
event.getPica()
event.huoqu(1)
event.download()
root.mainloop()