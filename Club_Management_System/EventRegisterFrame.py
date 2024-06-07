from tkinter import *
from tkinter.ttk import Treeview, Style
import tkinter.messagebox

import ManipulateDB

class EventRegisterFrame(Frame):
    def __init__(self, window: Tk, username: str, password: str):
        super().__init__(window)
        self.name = ManipulateDB.get_name_by_usr_and_pwd(username, password)
        self.username = username
        self.password = password
        self.club = ManipulateDB.get_club_by_usr_and_pwd(self.username, self.password)
        self.search_event_name = StringVar()
        self.event_id = IntVar()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.style = Style()
        self.create_page()
        self.show_events()

    def create_page(self):
        columns = ('id', 'club', 'name', 'description', 'venue', 'date', 'contact')
        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=30)

        self.tree_view.column('id', width=50, anchor='center')
        self.tree_view.column('club', width=150, anchor='center')
        self.tree_view.column('name', width=150, anchor='center')
        self.tree_view.column('description', width=200, anchor='center')
        self.tree_view.column('venue', width=100, anchor='center')
        self.tree_view.column('date', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')

        self.tree_view.heading('id', text='ID')
        self.tree_view.heading('club', text='社团')
        self.tree_view.heading('name', text='活动名称')
        self.tree_view.heading('description', text='活动简介')
        self.tree_view.heading('venue', text='活动地点')
        self.tree_view.heading('date', text='活动日期')
        self.tree_view.heading('contact', text='联系方式')

        self.style.configure('Treeview', font=('宋体', 12))

        self.tree_view.pack(fill=BOTH, expand=True)

        Label(self.view, text='请输入活动名称').pack(side=LEFT, pady=15)
        Entry(self.view, textvariable=self.search_event_name).pack(side=LEFT, pady=15, padx=10)
        Button(self.view, text='搜索', command=self.search_event).pack(side=LEFT, pady=15, padx=10)

        Label(self.view, text='请输入活动ID').pack(side=LEFT, pady=15)
        Entry(self.view, textvariable=self.event_id).pack(side=LEFT, pady=15, padx=10)
        Button(self.view, text='报名', command=self.register_event).pack(side=LEFT, pady=15, padx=10)


    def show_events(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        events = ManipulateDB.get_events(self.club)
        for event in events:
            self.tree_view.insert('', 'end', values=event)

    def search_event(self):
        event_name = self.search_event_name.get()
        if event_name == '':
            tkinter.messagebox.showwarning('警告', '请输入活动名称！')
            return
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        is_event_exist, event = ManipulateDB.search_event(event_name)
        if is_event_exist:
            self.tree_view.insert('', 'end', values=event)
        else:
            tkinter.messagebox.showinfo('提示', '未找到该活动！')
            self.show_events()

    def register_event(self):
        event_id = self.event_id.get()
        is_legal = self.validate_legality(event_id)
        if is_legal:
            ManipulateDB.register_event(event_id, self.club, self.name)
            tkinter.messagebox.showinfo('提示', '报名成功！')

    def validate_legality(self, event_id):
        flag = True
        if event_id == 0:
            tkinter.messagebox.showwarning('警告', '请输入活动ID！')
            flag = False
        elif event_id not in ManipulateDB.get_event_ids(self.club):
            tkinter.messagebox.showerror('错误', '活动ID输入错误！')
            flag = False
        elif ManipulateDB.has_registered(event_id, self.club, self.name):
            tkinter.messagebox.showinfo('提示', '您已报名该活动！')
            flag = False
        return flag

    def clear(self):
        self.tree_view.destroy()
        for widget in self.view.winfo_children():
            widget.destroy()