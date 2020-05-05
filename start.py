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

Button(toolBar,text="打开文件夹",borderwidth=0,activeforeground="SkyBlue",padx=5,height=2,command=event.openfolder).pack(side=LEFT)
Button(toolBar,text="设置",borderwidth=0,activeforeground="SkyBlue",padx=5,height=2,command=event.openMenu).pack(side=LEFT)
Button(toolBar,text="下载选中",borderwidth=0,activeforeground="SkyBlue",padx=5,height=2,command=event.downloadSelected).pack(side=LEFT)
Button(toolBar,text="关于",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.openAbout).pack(side=RIGHT)

'''
sb = Scrollbar(root)
table=Frame(root).place(relwidth=1,x=0,y=35)

tree_date = ttk.Treeview(table,show="headings",yscrollcommand= sb.set)
sb.config(command=tree_date.yview)
sb.place(relx=1,y=35,anchor="ne",width=20,height=320)
# 定义列
tree_date['columns'] = ['id','name','creater','likesCount','pagesCount','epsCount',"download"]
tree_date.place(x=30,y=35,width=750,height=320)

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
'''
tree_date=mTreeList.My_Tk(root)
pageSetBar=Frame(root)
pageSetBar.pack(fill=X)
Button(pageSetBar,text="上一页",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.previousPage).pack(side=LEFT)
PageT=StringVar()
PageT.set("第 页，共 页")
PageL=Label(pageSetBar,textvariable=PageT,padx=10)
PageL.pack(side=LEFT)
Button(pageSetBar,text="下一页",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.nextPage).pack(side=LEFT)
#Button(root,text='暂停')
Button(pageSetBar,text="暂停下载",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.nextPage).pack(side=RIGHT)
Button(pageSetBar,text="继续下载",borderwidth=0,activeforeground="SkyBlue",padx=10,height=2,command=event.nextPage).pack(side=RIGHT)
Label(pageSetBar,text="当前没有下载任务",fg='Gray').pack(side=RIGHT)

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
event.getPica()
event.checkConfig()
event.printl("配置完成")

event.download()

'''
heading_frame=Frame(root)
heading_frame.pack(fill='x')

#填充用
button_frame=Label(heading_frame,width=1)
button_frame.pack(side='left')
#全选按钮
all_buttonvar = IntVar()
all_button = Checkbutton(heading_frame, text='',variable=all_buttonvar)
all_button.pack(side=LEFT)
all_buttonvar.set(0)

columns = ['名称', '作者', '页数', '章节数', '点赞数','状态']
widths = [130, 100, 100, 100, 100, 100]

#重建tree的头
for i in range(len(columns)):
    Label(heading_frame,text=columns[i],width=int(widths[i]*0.16),anchor='center',relief=GROOVE).pack(side=LEFT)

#放置 canvas、滚动条的frame
canvas_frame=Frame(root,width=600,height=400,bg='red')
canvas_frame.pack(fill=X)

#只剩Canvas可以放置treeview和按钮，并且跟滚动条配合
canvas=Canvas(canvas_frame,width=500,height=400,bg='blue',scrollregion=(0,0,500,400))
canvas.pack(side=LEFT,fill=BOTH,expand=1)

#滚动条
ysb = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=ysb.set)
ysb.pack(side=RIGHT, fill=Y)
#!!!!=======重点：鼠标滚轮滚动时，改变的页面是canvas 而不是treeview
canvas.bind_all("<MouseWheel>",lambda event:canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))


#想要滚动条起效，得在canvas创建一个windows(frame)！！
tv_frame=Frame(canvas,bg='green')
tv_frame2=canvas.create_window(0, 0, window=tv_frame, anchor='nw',width=600,height=400)#anchor该窗口在左上方

#放置button的frame
button_frame=Frame(tv_frame,bg='plum')
button_frame.pack(side=LEFT, fill=Y)
Label(button_frame,width=3).pack()  #填充用

#创建treeview
tv = ttk.Treeview(tv_frame, height=10, columns=columns, show='headings')#height好像设定不了行数，实际由插入的行数决定
tv.pack(expand=1, side=LEFT, fill=BOTH)
#设定每一列的属性
for i in range(len(columns)):
    tv.column(columns[i], width=0, minwidth=widths[i], anchor='center', stretch=True)


#设定treeview格式
# import tkinter.font as tkFont
# ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
tv.tag_configure('oddrow', font='Arial 12')                    #设定treeview里字体格式font=ft
tv.tag_configure('select', background='SkyBlue',font='Arial 12')#当对应的按钮被打勾，那么对于的行背景颜色改变！
rowheight=27                                       #很蛋疼，好像tkinter里只能用整数！
ttk.Style().configure('Treeview', rowheight=rowheight)      #设定每一行的高度

# 设定选中的每一行字体颜色、背景颜色 (被选中时，没有变化)
ttk.Style().map("Treeview",
            foreground=[ ('focus', 'black'), ],
            background=[ ('active', 'white')]
            )
def select_tree(event):

    select_item=tv.focus()
    button = orm[select_item][0]
    button.invoke()  #改变对应按钮的状态，而且调用其函数
tv.bind('<<TreeviewSelect>>', select_tree) #绑定tree选中时的回调函数
'''
root.mainloop()