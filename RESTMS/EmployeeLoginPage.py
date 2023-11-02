import tkinter.messagebox
from tkinter import *
from EmployeePage import EmployeePage

import EmployeeDB


class EmployeeLoginPage:
    def __init__(self, window: Tk):
        '''
        Initialize the EmployeeLoginPage
        :param window:
        '''
        self.window = window
        self.window.geometry('280x140')
        self.window.title('员工登录')
        self.window.iconphoto(True, PhotoImage(file="Saloon.ico"))

        self.page = Frame(self.window)
        self.page.pack()

        self.username = StringVar()
        self.password = StringVar()

        Label(self.page, text='账号:').grid(row=0, column=0, padx=(10, 0), pady=10)
        Entry(self.page, textvariable=self.username).grid(row=0, column=1, columnspan=2, padx=(0, 10))

        Label(self.page, text='密码:').grid(row=1, column=0, padx=(10, 0))
        Entry(self.page, textvariable=self.password).grid(row=1, column=1, columnspan=2, padx=(0, 10))

        Button(self.page, text='登录', command=self.login_check).grid(row=2, column=1, pady=10, ipadx=10)
        Button(self.page, text='退出', command=self.page.quit).grid(row=2, column=2, ipadx=10)

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - 280) // 2
        y = (screen_height - 140) // 2

        self.window.geometry(f"280x140+{x}+{y}")

    def login_check(self):
        '''
        Check the login information
        :return:
        '''
        name = self.username.get()
        pwd = self.password.get()
        if EmployeeDB.is_employee(name, pwd):
            self.page.destroy()
            permission = EmployeeDB.get_permission(name, pwd)
            EmployeePage(self.window, permission)
        else:
            tkinter.messagebox.showwarning(title='警告', message='用户名或密码错误！')


if __name__ == '__main__':
    window = Tk()
    EmployeeLoginPage(window)
    window.mainloop()
