from tkinter import *           # 导入 Tkinter 库
from tkinter import ttk
import tkinter.messagebox
import webbrowser as web

class about():
    def __init__(self,root,event):
        self.root=root
        self.event=event
        self.event.aboutState=1
        x = root.winfo_x()
        y = root.winfo_y()
        t2 = Toplevel(self.root)
        t2.geometry("270x180+%d+%d"%(x+150,y+100))
        t2.title("关于") 
        t2.resizable(0,0)
        photo = PhotoImage(file=".\\icon\\temp.gif")
        imgLabel = Label(t2,image=photo)
        imgLabel.image=photo
        imgLabel.place(x=20,y=20,width=50,height=50)
        Label(t2,text='muyoo',font=('Microsoft YaHei UI',20),fg="RoyalBlue").place(x=80,y=13)
        Label(t2,text='一个摸鱼的伪技术宅',font=('Microsoft YaHei UI',10),fg="RoyalBlue").place(x=80,y=52)
        Label(t2,text="v 1.0 测试版").place(x=180,y=90)
        Button(t2,text="查看更多...",borderwidth=0,bg="RoyalBlue",fg="white",command=self.goto).place(x=0,y=120,relw=1,height=50)
    def goto(self):
        web.open("https://www.muyoo.top")