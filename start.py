from tkinter import *           # 导入 Tkinter 库
from tkinter import ttk
import pica
import threading
import setbox
import fileManager
import d

root = Tk()                     # 创建窗口对象的背景色
root.iconbitmap(".\\icon\\favicon.ico")
root.resizable(0,0)

class myThread (threading.Thread): 
    def __init__(self,tree_date,logT):
        threading.Thread.__init__(self)
        self.tree_date=tree_date
        self.log=logT
    def run(self):
        mpica=pica.pica(self.log)
        if mpica.login() is 1:
            mpica.printl("用户名或密码错误！请重新输入")
        tmp=0
        tmp2=1
        mpica.printl("获取收藏夹信息中...")
        '''
        while True:
            mpica.getPage(tmp2)
            mpica.allInfo.extend(mpica.allComicInfo)
            for item in mpica.allComicInfo:
                self.tree_date.insert('',tmp,values=(item.get('title',''),item.get('author',''),item.get('likesCount',''),item.get('pagesCount',''),item.get('epsCount','')))
                tmp+=1
            if tmp2==mpica.pageNum:break
            else:tmp2+=1
        mpica.printl("收藏夹加载完成！")
        '''
        
def openFile2():
    fileManager.openFile(".\\comic")

def huoqu():
    thread1=myThread(tree_date,logT)
    thread1.start()

root.title("哔咔收藏夹下载") 
root.geometry("800x560")
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New")
filemenu.add_command(label="Open...")
filemenu.add_command(label="Exit")
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...")
 
toolBar = Frame(root).place(relwidth=1,x=0,y=0)
Button(toolBar,text="获取",borderwidth=0,activeforeground="SkyBlue",command=huoqu).place(x=0,y=0,height=35,width=50)
Button(toolBar,text="开始下载",borderwidth=0,activeforeground="SkyBlue").place(x=55,y=0,height=35,width=50)
Button(toolBar,text="打开文件夹",borderwidth=0,activeforeground="SkyBlue",command=openFile2).place(x=120,y=0,height=35,width=60)
Button(toolBar,text="设置",borderwidth=0,activeforeground="SkyBlue").place(x=190,y=0,height=35,width=50)
Button(toolBar,text="关于",borderwidth=0,activeforeground="SkyBlue").place(relx=1,y=0,height=35,width=50,anchor="ne")
sb = Scrollbar(root)
table=Frame(root).place(relwidth=1,x=0,y=35)

tree_date = ttk.Treeview(table,show="headings",yscrollcommand= sb.set)
sb.config(command=tree_date.yview)
sb.place(relx=1,y=35,anchor="ne",width=20,height=340)
# 定义列
tree_date['columns'] = ['name','creater','likesCount','pagesCount','epsCount',"download"]
tree_date.place(x=0,y=35,width=780,height=340)


# 设置列宽度
tree_date.column('name',width=200)
tree_date.column('creater',width=100)
tree_date.column('pagesCount',width=30)
tree_date.column('epsCount',width=30)
tree_date.column('likesCount',width=30)
tree_date.column('download',width=50)
# 添加列名
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

if fileManager.isExist(".\\data\\config.json"):
    data=fileManager.readConfig()
    d.Email=data['user']
    d.Password=data['password']
    d.Proxy=data['proxy']
    d.Image_quality=data['quality']
else:
    setbox=setbox.setbox(root)

root.mainloop()