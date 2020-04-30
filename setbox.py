from tkinter import *           # 导入 Tkinter 库
from tkinter import ttk
import tkinter.messagebox
import d
import fileManager


class setbox ():
    def __init__(self,root):
        self.root=root
        t2 = Toplevel(self.root)
        t2.geometry("270x200")
        t2.title("设置") 
        t2.transient(self.root)
        Label(t2, text='哔咔账号', width=8,height=1).place(x=10,y=10)
        Label(t2, text='密码', width=5, height=1).place(x=10,y=50)
        Label(t2, text='代理设置(https)', width=12, height=1).place(x=10,y=130)
        Label(t2, text='下载图片质量', width=10, height=1).place(x=10,y=90)
        ttk.Separator(t2,orient='horizontal').place(x=10,y=120,width=240)
        self.var = StringVar()
        self.var.set('high')
        
        self.e1=Entry(t2)
        self.e3=Entry(t2, show='*')
        Radiobutton(t2, text='高', variable=self.var, value='high').place(x=90,y=90)
        Radiobutton(t2, text='中等', variable=self.var, value='B').place(x=140,y=90)
        Radiobutton(t2, text='低', variable=self.var, value='C').place(x=200,y=90)
        self.e2=Entry(t2)
        self.e1.insert(0, d.Email)
        self.e3.insert(0,d.Password)
        self.e2.insert(0,d.Proxy)
        self.e1.place(x=80,y=10)
        self.e2.place(x=10,y=160)
        self.e3.place(x=80,y=50) 
        Button(t2, text='确定', width=10, height=1, command=self.minput).place(x=170,y=150)
        self.t2=t2

    def minput(self):
        data={'user':self.e1.get(),'password':self.e3.get(),'proxy':self.e2.get(),'quality':self.var.get()}
        if(data['user'] is '' or data['password'] is ''):
            tkinter.messagebox.showinfo(title='提示', message='请填写哔咔的用户名或密码')
        else:
            fileManager.mkdir(".\\comic")
            fileManager.createJsonFile(data,'config.json')
            d.Email=data['user']
            d.Password=data['password']
            d.Proxy=data['proxy']
            d.Image_quality=data['quality']
            self.t2.destroy()
        
