import re
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Entry, Label, Button

import ManipulateDB

class MemberManageFrame(Frame):
    def __init__(self, window: Tk, club: str):
        super().__init__(window)
        self.domain_club = club
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.style = Style()
        self.fee_to_publish = StringVar()
        self.create_page()
        self.show_members()

    def create_page(self):
        font_style = ('Helvetica', 12)
        padx_value = 10
        pady_value = 30

        columns = ('member_id', 'name', 'contact', 'role', 'grade', 'major', 'class', 'fee')

        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=30, selectmode='browse')

        self.tree_view.column('member_id', width=50, anchor='center')
        self.tree_view.column('name', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')
        self.tree_view.column('role', width=50, anchor='center')
        self.tree_view.column('grade', width=50, anchor='center')
        self.tree_view.column('major', width=200, anchor='center')
        self.tree_view.column('class', width=50, anchor='center')
        self.tree_view.column('fee', width=100, anchor='center')

        self.tree_view.heading('member_id', text='ID')
        self.tree_view.heading('name', text='姓名')
        self.tree_view.heading('contact', text='联系方式')
        self.tree_view.heading('role', text='身份')
        self.tree_view.heading('grade', text='年级')
        self.tree_view.heading('major', text='专业')
        self.tree_view.heading('class', text='班级')
        self.tree_view.heading('fee', text='缴费状态')

        self.style.configure('Treeview', font=font_style)

        self.tree_view.pack(fill=BOTH, expand=True)

        Button(self.view, text='修改成员信息', command=self.update_info).pack(side='left', padx=padx_value, pady=pady_value)
        Button(self.view, text='删除成员', command=self.delete_member).pack(side='left', padx=padx_value, pady=pady_value)
        Button(self.view, text='审核入社申请', command=self.check_application).pack(side='left', padx=padx_value, pady=pady_value)

        Label(self.view, text='社费发布:', font=font_style).pack(side='left', padx=padx_value, pady=pady_value)
        Entry(self.view, textvariable=self.fee_to_publish).pack(side='left', padx=padx_value, pady=pady_value, anchor='w')
        Button(self.view, text='发布', command=self.publish_fee).pack(side='left', padx=padx_value, pady=pady_value)

    def show_members(self):
        members = ManipulateDB.get_members_by_club(self.domain_club)
        for member in members:
            self.tree_view.insert('', 'end', values=member)

    def publish_fee(self):
        fee = self.fee_to_publish.get()
        if not re.match(r'^\d+$', fee):
            messagebox.showwarning('警告', '请输入数字！')
            return
        ManipulateDB.publish_fee(self.domain_club, fee)
        messagebox.showinfo('提示', '发布成功！')
        self.fee_to_publish.set('')
        self.refresh()

    def clear(self):
        self.view.destroy()
        for widget in self.winfo_children():
            widget.destroy()

    def update_info(self):
        item = self.tree_view.item(self.tree_view.selection())
        print(item)
        if not item['values']:
            messagebox.showwarning('警告', '请选择一个成员！')
            return
        self.create_update_page(item)

    def delete_member(self):
        item = self.tree_view.item(self.tree_view.selection())
        if not item['values']:
            messagebox.showwarning('警告', '请选择一个成员！')
            return
        is_yes = messagebox.askyesno('警告', '确定删除该成员？')
        if is_yes:
            ManipulateDB.delete_member(item['values'][0])
            messagebox.showinfo('提示', '删除成功！')
            self.refresh()

    def check_application(self):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        columns = ('name', 'contact', 'grade', 'major', 'class', 'username', 'password')
        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=30, selectmode='browse')

        self.tree_view.column('name', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')
        self.tree_view.column('grade', width=50, anchor='center')
        self.tree_view.column('major', width=200, anchor='center')
        self.tree_view.column('class', width=50, anchor='center')
        self.tree_view.column('username', width=100, anchor='center')
        self.tree_view.column('password', width=100, anchor='center')

        self.tree_view.heading('name', text='姓名')
        self.tree_view.heading('contact', text='联系方式')
        self.tree_view.heading('grade', text='年级')
        self.tree_view.heading('major', text='专业')
        self.tree_view.heading('class', text='班级')
        self.tree_view.heading('username', text='用户名')
        self.tree_view.heading('password', text='密码')

        self.style.configure('Treeview', font=('宋体', 12))

        self.tree_view.pack(fill=BOTH, expand=True)

        Button(self.view, text='全部通过', command=self.pass_all).pack(side='left', padx=10, pady=30)
        Button(self.view, text='全部拒绝', command=self.refuse_all).pack(side='left', padx=10, pady=30)
        Button(self.view, text='通过', command=self.pass_one).pack(side='left', padx=10, pady=30)
        Button(self.view, text='拒绝', command=self.refuse_one).pack(side='left', padx=10, pady=30)
        Button(self.view, text='返回', command=self.back).pack(side='left', padx=10, pady=30)

        applications = ManipulateDB.get_applications(self.domain_club)
        for application in applications:
            self.tree_view.insert('', 'end', values=application)

    def back(self):
        self.clear()
        self.tree_view.destroy()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.create_page()
        self.show_members()

    def pass_all(self):
        applications = ManipulateDB.get_applications(self.domain_club)
        for application in applications:
            ManipulateDB.add_member(application, self.domain_club)
        messagebox.showinfo('提示', '全部通过！')
        self.check_refresh()

    def pass_one(self):
        item = self.tree_view.item(self.tree_view.selection())
        if not item['values']:
            messagebox.showwarning('警告', '请选择一个申请！')
            return
        ManipulateDB.add_member(item['values'], self.domain_club)
        messagebox.showinfo('提示', '通过成功！')
        self.check_refresh()

    def refuse_one(self):
        item = self.tree_view.item(self.tree_view.selection())
        if not item:
            messagebox.showwarning('警告', '请选择一个申请！')
            return
        ManipulateDB.delete_application(item['values'], self.domain_club)
        messagebox.showinfo('提示', '拒绝成功！')
        self.check_refresh()

    def refuse_all(self):
        applications = ManipulateDB.get_applications(self.domain_club)
        for application in applications:
            ManipulateDB.delete_application(application, self.domain_club)
        messagebox.showinfo('提示', '全部拒绝！')
        self.check_refresh()

    def check_refresh(self):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.check_application()

    def refresh(self):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.create_page()
        self.show_members()

    def create_update_page(self, item):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.id = item['values'][0]
        self.new_name = StringVar(value=item['values'][1])
        self.new_contact = StringVar(value=item['values'][2])
        self.new_role = StringVar(value=item['values'][3])
        self.new_grade = StringVar(value=item['values'][4])
        self.new_major = StringVar(value=item['values'][5])
        self.new_class = StringVar(value=item['values'][6])
        self.new_fee = StringVar(value=item['values'][7])

        Label(self.view, text='姓名:', font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_name).grid(row=0, column=1, padx=10, pady=10)

        Label(self.view, text='联系方式:', font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_contact).grid(row=1, column=1, padx=10, pady=10)

        Label(self.view, text='身份:', font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_role).grid(row=2, column=1, padx=10, pady=10)

        Label(self.view, text='年级:', font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_grade).grid(row=3, column=1, padx=10, pady=10)

        Label(self.view, text='专业:', font=('Helvetica', 12)).grid(row=4, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_major).grid(row=4, column=1, padx=10, pady=10)

        Label(self.view, text='班级:', font=('Helvetica', 12)).grid(row=5, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_class).grid(row=5, column=1, padx=10, pady=10)

        Label(self.view, text='社费:', font=('Helvetica', 12)).grid(row=6, column=0, padx=10, pady=10)
        Entry(self.view, textvariable=self.new_fee).grid(row=6, column=1, padx=10, pady=10)

        Button(self.view, text='确认修改', command=self.update_to_db).grid(row=7, column=1, padx=10, pady=10)
        Button(self.view, text='返回', command=self.refresh).grid(row=7, column=0, padx=10, pady=10)

    def update_to_db(self):
        new_item = {"Name": self.new_name.get(),
                    "Contact": self.new_contact.get(),
                    "Role": self.new_role.get(),
                    "Grade": self.new_grade.get(),
                    "Major": self.new_major.get(),
                    "Class": self.new_class.get(),
                    "FeeToPay": self.new_fee.get()}
        ManipulateDB.update_member_info(new_item, self.id)
        messagebox.showinfo('提示', '修改成功！')
        self.clear()
