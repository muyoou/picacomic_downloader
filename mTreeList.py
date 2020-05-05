
from tkinter import *
from tkinter.ttk import *
class My_Tk():
    def __init__(self,mytk):
        self.tk=mytk
        self.orm={}
        #self.create_button()
        self.create_heading()
        self.create_tv()
 
    def create_button(self):
        Button(self.tk,text='增加数据',command=self.insert_tv).pack()
 
    def create_heading(self,):
        '''重新做一个treeview的头，不然滚动滚动条，看不到原先的头！！！'''
        heading_frame=Frame(self.tk)
        heading_frame.pack(fill=X)
 
        #填充用
        button_frame=Label(heading_frame,width=0.5)
        button_frame.pack(side=LEFT,)
        #全选按钮
        self.all_buttonvar = IntVar()
        self.all_button = Checkbutton(heading_frame, text='',variable=self.all_buttonvar, command=self.select_all)
        self.all_button.pack(side=LEFT)
        self.all_buttonvar.set(0)
 
        self.columns = ['id','名称', '作者', '页数', '章节数', '点赞数','状态']
        self.widths = [0,260, 150, 65, 65, 65,65]
 
        #重建tree的头
        for i in range(len(self.columns)):
            Label(heading_frame,text=self.columns[i],width=int(self.widths[i]*0.156),anchor='center',relief=GROOVE).pack(side=LEFT)
 
 
    def create_tv(self):
        #放置 canvas、滚动条的frame
        canvas_frame=Frame(self.tk,width=400,height=400)
        canvas_frame.pack(fill=X)
 
        #只剩Canvas可以放置treeview和按钮，并且跟滚动条配合
        self.canvas=Canvas(canvas_frame,width=400,height=300,scrollregion=(0,0,500,300),bg='red')
        self.canvas.pack(side=LEFT,fill=BOTH,expand=1)
        #滚动条
        ysb = Scrollbar(canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=ysb.set)
        ysb.pack(side=RIGHT, fill=Y)
        #!!!!=======重点：鼠标滚轮滚动时，改变的页面是canvas 而不是treeview
        self.canvas.bind_all("<MouseWheel>",lambda event:self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
 
 
        #想要滚动条起效，得在canvas创建一个windows(frame)！！
        tv_frame=Frame(self.canvas)
        self.tv_frame=self.canvas.create_window(0, 0, window=tv_frame, anchor='nw',width=780,height=400)#anchor该窗口在左上方
 
        #放置button的frame
        self.button_frame=Frame(tv_frame)
        self.button_frame.pack(side=LEFT, fill=Y)
        Label(self.button_frame,width=3).pack()  #填充用
 
 
        #创建treeview
        self.tv = Treeview(tv_frame, height=10, columns=self.columns, show='headings')#height好像设定不了行数，实际由插入的行数决定
        self.tv.pack(expand=1, side=LEFT, fill=BOTH)
        #设定每一列的属性
        for i in range(len(self.columns)):
            self.tv.column(self.columns[i], width=self.widths[i], anchor='n', stretch=True)
 
 
        #设定treeview格式
        # import tkinter.font as tkFont
        # ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
        self.tv.tag_configure('oddrow')                    #设定treeview里字体格式font=ft
        self.tv.tag_configure('select', background='SkyBlue')#当对应的按钮被打勾，那么对于的行背景颜色改变！
        self.rowheight=27                                       #很蛋疼，好像tkinter里只能用整数！
        Style().configure('Treeview', rowheight=self.rowheight)      #设定每一行的高度
 
        # 设定选中的每一行字体颜色、背景颜色 (被选中时，没有变化)
        Style().map("Treeview",
                  foreground=[ ('focus', 'black'), ],
                  background=[ ('active', 'white')]
                  )
        self.tv.bind('<<TreeviewSelect>>', self.select_tree) #绑定tree选中时的回调函数
 
    def getTree(self):
        return self.tv
 
    def delALl(self):
        #清空tree、checkbutton
        items = self.tv.get_children()
        [self.tv.delete(item) for item in items]
        self.tv.update()
        for child in self.button_frame.winfo_children()[1:]: #第一个构件是label，所以忽略
            child.destroy()

    def insert_tv(self,data):
        #清空tree、checkbutton
        items = self.tv.get_children()
        [self.tv.delete(item) for item in items]
        self.tv.update()
        for child in self.button_frame.winfo_children()[1:]: #第一个构件是label，所以忽略
            child.destroy()
        #重设tree、button对应关系
        self.orm={}
        for item in data:
            tv_item=self.tv.insert('','end',values=(item.get('_id',''),item.get('title',''),item.get('author',''),item.get('likesCount',''),item.get('pagesCount',''),item.get('epsCount',''),''))
            import tkinter
            ck_button = tkinter.Checkbutton(self.button_frame,variable=IntVar())
            ck_button['command']=lambda item=tv_item:self.select_button(item)
            ck_button.pack()
            self.orm[tv_item]=[ck_button]
        #每次点击插入tree，先设定全选按钮不打勾，接着打勾并且调用其函数
        self.all_buttonvar.set(0)
        #self.all_button.invoke()
 
        #更新canvas的高度
        height = (len(self.tv.get_children()) + 1) * self.rowheight  # treeview实际高度
        self.canvas.itemconfigure(self.tv_frame, height=height) #设定窗口tv_frame的高度
        self.tk.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))#滚动指定的范围
 
    def select_all(self):
        '''全选按钮的回调函数
           作用：所有多选按钮打勾、tree所有行都改变底色(被选中)'''
        for item,[button] in self.orm.items():
            if self.all_buttonvar.get()==1:
                button.select()
                self.tv.item(item, tags='select')
            else:
                button.deselect()
                self.tv.item(item, tags='oddrow')

    def select_button(self,item):
        '''多选按钮的回调函数
            作用：1.根据按钮的状态，改变对应item的底色(被选中)
                 2.根据所有按钮被选的情况，修改all_button的状态'''
        
        button=self.orm[item][0]
        button_value=button.getvar(button['variable'])
        if button_value=='1':
            self.tv.item(item,tags='select')
        else:
            self.tv.item(item, tags='oddrow')
        self.all_button_select()#根据所有按钮改变 全选按钮状态

    def select_tree(self,event):
        '''tree绑定的回调函数
           作用：根据所点击的item改变 对应的按钮'''
        select_item=self.tv.focus()
        button = self.orm[select_item][0]
        button.invoke()  #改变对应按钮的状态，而且调用其函数

    def all_button_select(self):
        '''根据所有按钮改变 全选按钮状态
            循环所有按钮，当有一个按钮没有被打勾时，全选按钮取消打勾'''
        for [button] in self.orm.values():
            button_value = button.getvar(button['variable'])
            if button_value=='0':
                self.all_buttonvar.set(0)
                break
        else:
            self.all_buttonvar.set(1)

    def getSelected(self):
        tmp=1
        output=[]
        for [button] in self.orm.values():
            button_value = button.getvar(button['variable'])
            if button_value!='0':
                output.append(tmp)
            tmp+=1
        return output
