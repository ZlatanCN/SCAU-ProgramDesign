from tkinter import *
from tkinter import ttk, messagebox

import ManipulateDB

class ClubInfoFrame(Frame):
    def __init__(self, window: Tk, club: str):
        super().__init__(window)
        self.domain_club = club
        self.club_info = ManipulateDB.get_club_info(self.domain_club)
        self.new_club_type = StringVar()
        self.new_club_principal = StringVar()
        self.new_club_contact = StringVar()
        self.new_club_description = StringVar()
        self.new_club_college = StringVar()
        self.new_club_advisor = StringVar()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.style = ttk.Style()
        self.create_page()
        self.new_info = {}

    def create_page(self):
        font_style = ('Helvetica', 14)
        padx_value = 10
        pady_value = 10

        Label(self.view, text='社团名称: ', font=font_style).grid(row=0, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.domain_club, font=font_style).grid(row=0, column=1, sticky='w', pady=pady_value)

        Label(self.view, text="社团类型: ", font=font_style).grid(row=1, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.club_info[0], font=font_style).grid(row=1, column=1, sticky='w', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_club_type).grid(row=1, column=2, pady=pady_value, padx=padx_value)

        Label(self.view, text="社团负责人: ", font=font_style).grid(row=2, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.club_info[1], font=font_style).grid(row=2, column=1, sticky='w', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_club_principal).grid(row=2, column=2, pady=pady_value,
                                                                        padx=padx_value)

        Label(self.view, text="所属学院: ", font=font_style).grid(row=3, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.club_info[2], font=font_style).grid(row=3, column=1, sticky='w', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_club_college).grid(row=3, column=2, pady=pady_value, padx=padx_value)

        Label(self.view, text="顾问教师: ", font=font_style).grid(row=4, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.club_info[3], font=font_style).grid(row=4, column=1, sticky='w', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_club_advisor).grid(row=4, column=2, pady=pady_value, padx=padx_value)

        Label(self.view, text="联系方式: ", font=font_style).grid(row=5, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.club_info[4], font=font_style).grid(row=5, column=1, sticky='w', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_club_contact).grid(row=5, column=2, pady=pady_value, padx=padx_value)

        Label(self.view, text="社团简介: ", font=font_style).grid(row=6, column=0, sticky='e', pady=pady_value)
        Label(self.view, text=self.club_info[5], font=font_style).grid(row=6, column=1, sticky='w', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_club_description).grid(row=6, column=2, pady=pady_value,
                                                                          padx=padx_value)

        ttk.Button(self.view, text='修改', command=self.update_info).grid(row=7, column=2, columnspan=5,
                                                                          pady=pady_value, sticky='e')

    def update_info(self):
        self.new_info = {"Type": self.new_club_type.get(),
                         "Principal": self.new_club_principal.get(),
                         "College": self.new_club_college.get(),
                         "Advisor": self.new_club_advisor.get(),
                         "Contact": self.new_club_contact.get(),
                         "Description": self.new_club_description.get()}

        if all(x == '' for x in self.new_info.values()):
            messagebox.showwarning('警告', '未填写任何修改信息！')
            return

        ManipulateDB.update_club_info(self.new_info, self.domain_club)
        messagebox.showinfo('提示', '修改成功！')
        self.refresh()

    def clear(self):
        self.view.destroy()

    def refresh(self):
        self.clear()
        self.club_info = ManipulateDB.get_club_info(self.domain_club)
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')

        self.new_club_type.set('')
        self.new_club_principal.set('')
        self.new_club_contact.set('')
        self.new_club_description.set('')
        self.new_club_college.set('')
        self.new_club_advisor.set('')

        self.create_page()
