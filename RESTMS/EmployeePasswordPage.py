from tkinter import *
from tkinter.ttk import Treeview

import EmployeeDB


class EmployeePasswordPage:
    def __init__(self, window: Tk):
        '''
        Initialize the EmployeePasswordPage
        :param window:
        '''
        self.tree_view = None
        self.window = window
        self.window.geometry('560x280')
        self.window.title('查看账号密码')
        self.create_table()
        self.show_data()

    def create_table(self):
        '''
        Create a table to show the login information
        :return:
        '''
        columns = ('id', 'name', 'username', 'password', 'permission')
        self.tree_view = Treeview(self.window, show='headings', columns=columns)

        self.tree_view.column('id', width=10, anchor='center')
        self.tree_view.heading('id', text='工号')

        self.tree_view.column('name', width=10, anchor='center')
        self.tree_view.heading('name', text='姓名')

        self.tree_view.column('username', width=10, anchor='center')
        self.tree_view.heading('username', text='用户名')

        self.tree_view.column('password', width=10, anchor='center')
        self.tree_view.heading('password', text='密码')

        self.tree_view.column('permission', width=10, anchor='center')
        self.tree_view.heading('permission', text='权限')

        self.tree_view.pack(fill=BOTH, expand=True)

    def show_data(self):
        '''
        Show the login information
        :return:
        '''
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        EmployeeDB.show_login_info(self)


if __name__ == '__main__':
    window = Tk()
    EmployeePasswordPage(window)
    window.mainloop()
