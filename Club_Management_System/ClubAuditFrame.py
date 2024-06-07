from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview, Style
import tkinter.messagebox

import ManipulateDB

class ClubAuditFrame(Frame):
    def __init__(self ,window: Tk):
        super().__init__(window)
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.style = Style()
        self.create_page()
        self.show_apps()

    def create_page(self):
        columns = ('approval_id', 'club_name', 'type', 'principal', 'college', 'advisor', 'contact', 'description',
                   'username', 'password')

        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=20, selectmode='browse')

        self.tree_view.column('approval_id', width=75, anchor='center')
        self.tree_view.column('club_name', width=150, anchor='center')
        self.tree_view.column('type', width=150, anchor='center')
        self.tree_view.column('principal', width=100, anchor='center')
        self.tree_view.column('college', width=150, anchor='center')
        self.tree_view.column('advisor', width=100, anchor='center')
        self.tree_view.column('contact', width=150, anchor='center')
        self.tree_view.column('description', width=150, anchor='center')
        self.tree_view.column('username', width=100, anchor='center')
        self.tree_view.column('password', width=100, anchor='center')

        self.tree_view.heading('approval_id', text='审核编号')
        self.tree_view.heading('club_name', text='社团名称')
        self.tree_view.heading('type', text='类型')
        self.tree_view.heading('principal', text='负责人')
        self.tree_view.heading('college', text='学院')
        self.tree_view.heading('advisor', text='指导老师')
        self.tree_view.heading('contact', text='联系方式')
        self.tree_view.heading('description', text='简介')
        self.tree_view.heading('username', text='用户名')
        self.tree_view.heading('password', text='密码')

        self.style.configure('Treeview', rowheight=30, font=('Helvetica', 12))
        self.tree_view.pack(fill=BOTH, expand=True)

        ttk.Button(self.view, text='通过', width=7, command=self.approve).pack(side=LEFT, padx=10, pady=10)
        ttk.Button(self.view, text='拒绝', width=7, command=self.reject).pack(side=LEFT, padx=10, pady=10)

    def approve(self):
        item = tuple(self.tree_view.set(self.tree_view.focus()).values())
        if not item:
            tkinter.messagebox.showwarning('警告', '请选择一项申请')
            return
        ManipulateDB.approve_club(item)
        tkinter.messagebox.showinfo('提示', '审核通过')
        self.refresh()

    def reject(self):
        item = tuple(self.tree_view.set(self.tree_view.focus()).values())
        if not item:
            tkinter.messagebox.showwarning('警告', '请选择一项申请')
            return
        ManipulateDB.reject_club(item)
        tkinter.messagebox.showinfo('提示', '审核拒绝')
        self.refresh()

    def refresh(self):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.create_page()
        self.show_apps()

    def show_apps(self):
        approvals = ManipulateDB.get_approvals()
        for approval in approvals:
            self.tree_view.insert('', 'end', values=approval)

    def clear(self):
        self.view.destroy()