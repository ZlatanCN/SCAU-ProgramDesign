from datetime import datetime
from tkinter import *
from tkinter.ttk import Treeview, Style
import tkinter.messagebox

import ManipulateDB

class EventCheckInFrame(Frame):
    def __init__(self, window: Tk, name: str):
        super().__init__(window)
        self.name = name
        self.check_in_id = IntVar()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.search_event_name = StringVar()
        self.style = Style()
        self.clean_expired_events()
        self.create_page()
        self.show_events()

    def create_page(self):
        columns = ('event_id', 'club', 'event', 'description', 'venue', 'date', 'contact')
        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=30)

        self.tree_view.column('event_id', width=50, anchor='center')
        self.tree_view.column('club', width=150, anchor='center')
        self.tree_view.column('event', width=150, anchor='center')
        self.tree_view.column('description', width=200, anchor='center')
        self.tree_view.column('venue', width=100, anchor='center')
        self.tree_view.column('date', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')

        self.tree_view.heading('event_id', text='ID')
        self.tree_view.heading('club', text='所属社团')
        self.tree_view.heading('event', text='活动名称')
        self.tree_view.heading('description', text='活动简介')
        self.tree_view.heading('venue', text='活动地点')
        self.tree_view.heading('date', text='活动日期')
        self.tree_view.heading('contact', text='联系方式')

        self.style.configure('Treeview', font=('宋体', 12))

        self.tree_view.pack(fill=BOTH, expand=True)

        Label(self.view, text='请输入活动ID: ').pack(side=LEFT, pady=15)
        Entry(self.view, textvariable=self.check_in_id).pack(side=LEFT, pady=15, padx=10)
        Button(self.view, text='签到', command=self.check_in).pack(side=LEFT, pady=15, padx=10)

    def show_events(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        events = ManipulateDB.get_my_events(self.name)
        # print(events)
        for event in events:
            self.tree_view.insert('', 'end', values=event)

    def check_in(self):
        flag = self.validate_legality()
        if flag:
            date = datetime.now().strftime("%Y-%m-%d")
            if date < ManipulateDB.get_event_date(self.check_in_id.get()):
                tkinter.messagebox.showerror('错误', '活动尚未开始！')
                return
            else:
                ManipulateDB.check_in(self.name, self.check_in_id.get())
                tkinter.messagebox.showinfo('提示', '签到成功！')
                self.refresh()

    def validate_legality(self):
        flag = True
        if self.check_in_id.get() == 0:
            tkinter.messagebox.showwarning('警告', '请输入活动ID！')
            flag = False
        elif not ManipulateDB.is_my_event_exist(self.check_in_id.get(), self.name):
            print(self.check_in_id.get(), self.name, ManipulateDB.is_my_event_exist(self.check_in_id.get(), self.name))
            tkinter.messagebox.showerror('错误', '已签到或活动不存在!')
            flag = False
        return flag

    def clear(self):
        self.view.destroy()

    def clean_expired_events(self):
        ManipulateDB.clean_expired_events()

    def refresh(self):
        self.view.destroy()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.create_page()
        self.show_events()