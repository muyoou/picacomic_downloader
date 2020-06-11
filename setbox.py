from tkinter import *           # 导入 Tkinter 库
from tkinter import ttk
import tkinter.messagebox
import d
import fileManager
import thread

class setbox ():
    def __init__(self,root,event):
        self.event=event
        self.root=root
        self.event.setboxState=1
        x = root.winfo_x()
        y = root.winfo_y()
        t2 = Toplevel(self.root)
        t2.geometry("270x230+%d+%d"%(x+150,y+100))
        t2.title("设置") 
        t2.transient(self.root)
        t2.resizable(0,0)
        Label(t2, text='哔咔账号', width=8,height=1).place(x=10,y=10)
        Label(t2, text='密码', width=5, height=1).place(x=10,y=50)
        Label(t2, text='下载图片质量', width=10, height=1).place(x=10,y=90)
        ttk.Separator(t2,orient='horizontal').place(x=10,y=150,width=240)
        self.var = StringVar()
        self.var.set('high')
        self.useProxy = BooleanVar()
        self.useProxy.set(d.useProxy)
        self.e1=Entry(t2)
        self.e3=Entry(t2, show='*')
        Radiobutton(t2, text='原画', variable=self.var, value='original').place(x=30,y=120)
        Radiobutton(t2, text='高', variable=self.var, value='high').place(x=90,y=120)
        Radiobutton(t2, text='中等', variable=self.var, value='medium').place(x=140,y=120)
        Radiobutton(t2, text='低', variable=self.var, value='low').place(x=200,y=120)
        Checkbutton(t2, text='使用https代理', variable=self.useProxy,command=self.usedProxy).place(x=10,y=160)
        self.e2=Entry(t2)
        self.e1.insert(0, d.Email)
        self.e3.insert(0,d.Password)
        self.e2.insert(0,d.Proxy)
        self.e1.place(x=80,y=10)
        self.e2.place(x=10,y=190)
        self.e3.place(x=80,y=50)
        Button(t2, text='确定', width=10, height=1, command=self.minput).place(x=170,y=180)
        t2.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.usedProxy()
        self.t2=t2 

    def closeWindow(self):
        self.event.setboxState=0
        self.t2.destroy()

    def usedProxy(self):
        if self.useProxy.get() == False:
            self.e2.config(state=DISABLED)
        else:
            self.e2.config(state=NORMAL)

    def minput(self):
        data={'user':self.e1.get(),'password':self.e3.get(),'useProxy':self.useProxy.get(),'proxy':self.e2.get(),'quality':self.var.get()}
        if(data['user'] == '' or data['password'] == ''):
            tkinter.messagebox.showinfo(title='提示', message='请填写哔咔的用户名或密码')
        else:
            fileManager.mkdir(".\\comic")
            fileManager.createJsonFile(data,'config.json')
            d.Email=data['user']
            d.useProxy=data['useProxy']
            d.Password=data['password']
            d.Proxy=data['proxy']
            d.Image_quality=data['quality']
            self.event.setboxState=0
            self.event.huoqu(1)
            self.t2.destroy()