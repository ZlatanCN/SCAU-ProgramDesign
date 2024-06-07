from tkinter import *
from tkinter import messagebox

import ManipulateDB

class ClubJoinFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.window = window
        self.name = StringVar()
        self.contact = StringVar()
        self.grade = IntVar()
        self.major = StringVar()
        self.class_ = IntVar()
        self.club_to_join = StringVar()
        self.create_page()
        self.place(relx=0.5, rely=0.5, anchor='center')

    def create_page(self):
        #print('create page')
        Label(self, text='意向社团').grid(row=0, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.club_to_join).grid(row=0, column=1, padx=10, pady=10)

        Label(self, text='姓名').grid(row=1, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.name).grid(row=1, column=1, padx=10, pady=10)

        Label(self, text='联系方式').grid(row=2, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.contact).grid(row=2, column=1, padx=10, pady=10)

        Label(self, text='年级(如: 2022)').grid(row=3, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.grade).grid(row=3, column=1, padx=10, pady=10)

        Label(self, text='专业').grid(row=4, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.major).grid(row=4, column=1, padx=10, pady=10)

        Label(self, text='班级(如: 1)').grid(row=5, column=0, padx=10, pady=10)
        Entry(self, textvariable=self.class_).grid(row=5, column=1, padx=10, pady=10)

        Button(self, text='申请加入', command=self.join).grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='E')

    def join(self):
        is_legal = self.validate_legality()
        if is_legal:
            ManipulateDB.send_application(self.name.get(), self.contact.get(), self.grade.get(), self.major.get(), self.class_.get(), self.club_to_join.get())
            messagebox.showinfo('提示', '申请成功！')
            self.refresh()

    def validate_legality(self):
        flag = True
        if self.name.get() == '' or self.contact.get() == '' or self.grade.get() == 0 or self.major.get() == '' or self.class_.get() == 0 or self.club_to_join.get() == '':
            messagebox.showwarning('警告', '请填写完整信息！')
            flag = False
        elif not self.club_is_exist(self.club_to_join.get()):
            messagebox.showerror('错误', '社团不存在！')
            flag = False
        elif self.is_in_club(self.name.get(), self.club_to_join.get()):
            messagebox.showerror('错误', '您已加入该社团！')
            flag = False
        elif self.is_in_application(self.club_to_join.get(), self.name.get(), self.contact.get(), self.grade.get(), self.major.get(), self.class_.get()):
            messagebox.showerror('错误', '申请已存在！')
            flag = False
        return flag

    def club_is_exist(self, club_name):
        return ManipulateDB.search_club(club_name)[0]

    def is_in_club(self, name, club_name):
        return ManipulateDB.name_is_in_club(name, club_name)

    def is_in_application(self, club_name, name, contact, grade, major, class_):
        return ManipulateDB.is_application_exist(club_name, name, contact, grade, major, class_)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def refresh(self):
        self.name.set('')
        self.contact.set('')
        self.grade.set(0)
        self.major.set('')
        self.class_.set(0)
        self.club_to_join.set('')