from tkinter import *
from tkinter.ttk import Treeview, Style
import tkinter.messagebox

import ManipulateDB

class ClubSearchFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.search_club_name = StringVar()
        self.style = Style()
        self.create_page()
        self.show_clubs()

    def create_page(self):
        columns = ('id', 'name', 'type', 'president', 'college', 'advisor', 'contact', 'description')
        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=30, style='Custom.Treeview')

        self.tree_view.column('id', width=50, anchor='center')
        self.tree_view.column('name', width=150, anchor='center')
        self.tree_view.column('type', width=150, anchor='center')
        self.tree_view.column('president', width=100, anchor='center')
        self.tree_view.column('college', width=150, anchor='center')
        self.tree_view.column('advisor', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')
        self.tree_view.column('description', width=200, anchor='center')

        self.tree_view.heading('id', text='ID')
        self.tree_view.heading('name', text='社团名称')
        self.tree_view.heading('type', text='社团类型')
        self.tree_view.heading('president', text='社长')
        self.tree_view.heading('college', text='学院')
        self.tree_view.heading('advisor', text='指导老师')
        self.tree_view.heading('contact', text='联系方式')
        self.tree_view.heading('description', text='社团简介')

        self.style.configure('Custom.Treeview', font=('宋体', 12))
        self.style.theme_use('default')

        self.tree_view.pack(fill=BOTH, expand=True)

        Label(self.view, text='请输入社团名称').pack(side=LEFT, pady=15)
        Entry(self.view, textvariable=self.search_club_name).pack(side=LEFT, pady=15, padx=10)
        Button(self.view, text='搜索', command=self.search_club).pack(side=LEFT, pady=15, padx=10)

    def show_clubs(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        clubs = ManipulateDB.get_clubs()
        for club in clubs:
            self.tree_view.insert('', 'end', values=club)

    def search_club(self):
        club_name = self.search_club_name.get()
        if club_name == '':
            tkinter.messagebox.showwarning('警告', '请输入社团名称！')
            return
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        is_club_exist, club = ManipulateDB.search_club(club_name)
        if is_club_exist:
            self.tree_view.insert('', 'end', values=club)
        else:
            tkinter.messagebox.showinfo('提示', '未找到该社团！')
            self.show_clubs()

    def clear(self):
        self.tree_view.destroy()
        for widget in self.view.winfo_children():
            widget.destroy()
        self.search_club_name.set('')
