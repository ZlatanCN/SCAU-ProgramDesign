import os
from tkinter import *
from tkinter.ttk import Treeview, Style
import tkinter.messagebox

from PIL import Image, ImageTk

import BarFoodDB
import EmployeeDB
from EmployeePasswordPage import EmployeePasswordPage


class ModifyFrame(Frame):
    def __init__(self, window, permission):
        '''
        Initialize the ModifyFrame
        :param window:
        :param permission:
        '''
        super().__init__(window)
        self.login_permission = permission
        self.check = False
        self.static_id = None
        self.id = StringVar()
        self.name = StringVar()
        self.job = StringVar()
        self.salary = IntVar()
        self.address = StringVar()
        self.phone_number = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.permission = StringVar()
        self.status = StringVar()
        self.create_page()

    def create_page(self):
        '''
        Create a page to modify the employee information
        :return:
        '''
        Label(self, text='请先输入工号获取员工信息: ').grid(row=0, column=2)

        Label(self, text='工号(必填): ').grid(row=1, column=1, pady=2)
        Entry(self, textvariable=self.id).grid(row=1, column=2)

        Label(self, text='姓名: ').grid(row=2, column=1, pady=2)
        Entry(self, textvariable=self.name).grid(row=2, column=2)

        Label(self, text='职位: ').grid(row=3, column=1, pady=2)
        Entry(self, textvariable=self.job).grid(row=3, column=2)

        Label(self, text='月薪: ').grid(row=4, column=1, pady=2)
        Entry(self, textvariable=self.salary).grid(row=4, column=2)

        Label(self, text='住址: ').grid(row=5, column=1, pady=2)
        Entry(self, textvariable=self.address).grid(row=5, column=2)

        Label(self, text='联系方式: ').grid(row=6, column=1, pady=2)
        Entry(self, textvariable=self.phone_number).grid(row=6, column=2)

        Label(self, text='用户名: ').grid(row=7, column=1, pady=2)
        Entry(self, textvariable=self.username).grid(row=7, column=2)

        Label(self, text='密码: ').grid(row=8, column=1, pady=2)
        Entry(self, textvariable=self.password).grid(row=8, column=2)

        Label(self, text='权限: ').grid(row=9, column=1, pady=2)
        Entry(self, textvariable=self.permission).grid(row=9, column=2)

        Button(self, text='查询', command=self.show_data).grid(row=10, column=1, pady=10, sticky=E)
        Button(self, text='修改', command=self.update_data).grid(row=10, column=2, pady=10, sticky=E)

        Label(self, textvariable=self.status).grid(row=11, column=2, sticky=E)

    def show_data(self):
        '''
        Show the employee information
        :return:
        '''
        if self.login_permission == 'admin':
            if EmployeeDB.id_is_exist(self, self.id.get()):
                self.static_id = self.id.get()
                info = EmployeeDB.all_data_in_dict(self, self.id.get())
                # print(info)
                self.id.set(info['id'])
                self.name.set(info['name'])
                self.job.set(info['job'])
                self.salary.set(info['salary'])
                self.address.set(info['address'])
                self.phone_number.set(info['phone_number'])
                self.username.set(info['username'])
                self.password.set(info['password'])
                self.permission.set(info['permission'])
                self.check = True
            else:
                tkinter.messagebox.showwarning(title='提示', message='该用户不存在或已删除')
        else:
            tkinter.messagebox.showwarning(title='警告', message='仅限管理员使用')

    def update_data(self):
        '''
        Update the employee information
        :return:
        '''
        if self.check:
            updated_info = {"id": self.id.get(),
                            "name": self.name.get(),
                            "job": self.job.get(),
                            "salary": self.salary.get(),
                            "address": self.address.get(),
                            "phone_number": self.phone_number.get(),
                            "username": self.username.get(),
                            "password": self.password.get(),
                            "permission": self.permission.get()}
            if updated_info['id'] == self.static_id:
                # print(updated_info)
                EmployeeDB.update_all_data(self.static_id, updated_info)
                self.status.set('修改成功!')
                self.clear_modify_data()
            else:
                tkinter.messagebox.showwarning(title='警告', message='工号不能被修改， 请输入正确的工号!')
        else:
            tkinter.messagebox.showwarning(title='提示', message='请先填写工号并点击查询按钮！')

    def clear_modify_data(self):
        '''
        Clear the data in the entry
        :return:
        '''
        self.name.set('')
        self.job.set('')
        self.salary.set(0)
        self.address.set('')
        self.phone_number.set('')
        self.username.set('')
        self.password.set('')
        self.permission.set('')

    def pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        SearchFrame.pack_forget(self.search_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        AddFrame.pack_forget(self.add_frame)
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        FoodSearchFrame.pack_forget(self.food_search_frame)


class AddFrame(Frame):
    def __init__(self, window, permission):
        '''
        Initialize the AddFrame
        :param window:
        :param permission:
        '''
        super().__init__(window)
        self.login_permission = permission
        self.id = StringVar()
        self.name = StringVar()
        self.job = StringVar()
        self.salary = IntVar()
        self.address = StringVar()
        self.phone_number = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.permission = StringVar()
        self.status = StringVar()
        self.create_page()

    def create_page(self):
        '''
        Create a page to add the employee information
        :return:
        '''
        Label(self).grid(row=0)

        Label(self, text='工号(必填): ').grid(row=1, column=1, pady=2)
        Entry(self, textvariable=self.id).grid(row=1, column=2)

        Label(self, text='姓名(必填): ').grid(row=2, column=1, pady=2)
        Entry(self, textvariable=self.name).grid(row=2, column=2)

        Label(self, text='职位: ').grid(row=3, column=1, pady=2)
        Entry(self, textvariable=self.job).grid(row=3, column=2)

        Label(self, text='月薪: ').grid(row=4, column=1, pady=2)
        Entry(self, textvariable=self.salary).grid(row=4, column=2)

        Label(self, text='住址: ').grid(row=5, column=1, pady=2)
        Entry(self, textvariable=self.address).grid(row=5, column=2)

        Label(self, text='联系方式: ').grid(row=6, column=1, pady=2)
        Entry(self, textvariable=self.phone_number).grid(row=6, column=2)

        Label(self, text='用户名: ').grid(row=7, column=1, pady=2)
        Entry(self, textvariable=self.username).grid(row=7, column=2)

        Label(self, text='密码: ').grid(row=8, column=1, pady=2)
        Entry(self, textvariable=self.password).grid(row=8, column=2)

        Label(self, text='权限: ').grid(row=9, column=1, pady=2)
        Entry(self, textvariable=self.permission).grid(row=9, column=2)

        Button(self, text='录入', command=self.record_info).grid(row=10, column=2, pady=5, sticky=E)

        Label(self, textvariable=self.status).grid(row=11, column=2, sticky=E)

    def clear_add_data(self):
        '''
        Clear the data in the entry
        :return:
        '''
        self.id.set('')
        self.name.set('')
        self.job.set('')
        self.salary.set(0)
        self.address.set('')
        self.phone_number.set('')
        self.username.set('')
        self.password.set('')
        self.permission.set('')

    def record_info(self):
        '''
        Record the employee information
        :return:
        '''
        if self.login_permission == 'admin':
            info = {"id": self.id.get(),
                    "name": self.name.get(),
                    "job": self.job.get(),
                    "salary": self.salary.get(),
                    "address": self.address.get(),
                    "phone_number": self.phone_number.get(),
                    "username": self.username.get(),
                    "password": self.password.get(),
                    "permission": self.permission.get()}
            if info['id'] == '' or info['name'] == '':
                tkinter.messagebox.showwarning(title='提示', message='工号或姓名未填写！')
            elif EmployeeDB.id_is_exist(self, self.id.get()):
                tkinter.messagebox.showwarning(title='警告', message='该工号已存在，请输入新的工号!')
            else:
                EmployeeDB.add_employee(info)
                self.status.set('录入成功！')
                self.clear_add_data()
        else:
            tkinter.messagebox.showwarning(title='警告', message='仅限管理员使用！')

    def pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        ModifyFrame.pack_forget(self.modify_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        SearchFrame.pack_forget(self.search_frame)
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        FoodSearchFrame.pack_forget(self.food_search_frame)


class DeleteFrame(Frame):
    def __init__(self, window, permission):
        '''
        Initialize the DeleteFrame
        :param window:
        :param permission:
        '''
        super().__init__(window)
        self.permission = permission
        self.view = Frame()
        self.view.pack()
        self.tree_view = None
        self.id = StringVar()
        self.status = StringVar()
        self.create_page()

    def create_page(self):
        '''
        Create a page to delete the employee information
        :return:
        '''
        Label(self, text='请输入该员工的工号: ').grid(row=0, column=0)
        Entry(self, textvariable=self.id).grid(row=1, column=0)
        Button(self, text='确认', command=self.show_table).grid(row=2, pady=5)

    def show_table(self):
        '''
        Show the employee information
        :return:
        '''
        if self.permission == 'admin':
            columns = ('id', 'name', 'job', 'salary', 'address', 'phone_number', 'username', 'password', 'permission')
            self.tree_view = Treeview(self, show='headings', columns=columns, height=1)

            self.tree_view.column('id', width=50, anchor='center')
            self.tree_view.heading('id', text='工号')

            self.tree_view.column('name', width=50, anchor='center')
            self.tree_view.heading('name', text='姓名')

            self.tree_view.column('job', width=50, anchor='center')
            self.tree_view.heading('job', text='职务')

            self.tree_view.column('salary', width=50, anchor='center')
            self.tree_view.heading('salary', text='月薪')

            self.tree_view.column('address', width=125, anchor='center')
            self.tree_view.heading('address', text='住址')

            self.tree_view.column('phone_number', width=100, anchor='center')
            self.tree_view.heading('phone_number', text='联系方式')

            self.tree_view.column('username', width=50, anchor='center')
            self.tree_view.heading('username', text='用户名')

            self.tree_view.column('password', width=55, anchor='center')
            self.tree_view.heading('password', text='密码')

            self.tree_view.column('permission', width=50, anchor='center')
            self.tree_view.heading('permission', text='权限')

            self.tree_view.grid(row=3, pady=5)

            self.show_table_data()
        else:
            tkinter.messagebox.showwarning(title='警告', message='仅限管理员使用')

    def show_table_data(self):
        '''
        Show the employee information
        :return:
        '''
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        if EmployeeDB.id_is_exist(self, self.id.get()):
            EmployeeDB.show_all_data(self, self.id.get())
            Label(self, text='确认删除以上员工信息: ').grid(row=4, column=0, pady=15, sticky=W)
            Button(self, text='删除', command=self.delete_data).grid(row=5, column=0, sticky=W)
            Button(self, text='退出', command=self.tree_view.quit).grid(row=6, column=0, pady=5, sticky=W)
            Label(self, textvariable=self.status).grid(row=7)
        else:
            tkinter.messagebox.showwarning(title='提示', message='用户已删除或不存在！')

    def delete_data(self):
        '''
        Delete the employee information
        :return:
        '''
        if EmployeeDB.get_permission_use_id(self.id.get()) == 'admin':
            tkinter.messagebox.showwarning(title='警告', message='无法删除管理员，请先修改权限！')
        else:
            EmployeeDB.delete_one_row(self.id.get())
            self.status.set('删除成功！')
            self.id.set('')

    def pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        ModifyFrame.pack_forget(self.modify_frame)
        SearchFrame.pack_forget(self.search_frame)
        AddFrame.pack_forget(self.add_frame)
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        FoodSearchFrame.pack_forget(self.food_search_frame)


class SearchFrame(Frame):
    def __init__(self, window, permission):
        '''
        Initialize the SearchFrame
        :param window:
        :param permission:
        '''
        super().__init__(window)
        self.view = Frame()
        self.view.pack()
        self.tree_view = None
        self.creat_page()
        self.create_buttons()
        self.show_data()
        self.permission = permission

    def creat_page(self):
        '''
        Create a page to search the employee information
        :return:
        '''
        columns = ('id', 'name', 'job', 'salary', 'address', 'phone_number')
        self.tree_view = Treeview(self, show='headings', columns=columns)

        self.tree_view.column('id', width=50, anchor='center')
        self.tree_view.heading('id', text='工号')

        self.tree_view.column('name', width=75, anchor='center')
        self.tree_view.heading('name', text='姓名')

        self.tree_view.column('job', width=75, anchor='center')
        self.tree_view.heading('job', text='职务')

        self.tree_view.column('salary', width=75, anchor='center')
        self.tree_view.heading('salary', text='月薪')

        self.tree_view.column('address', width=150, anchor='center')
        self.tree_view.heading('address', text='住址')

        self.tree_view.column('phone_number', width=150, anchor='center')
        self.tree_view.heading('phone_number', text='联系方式')

        self.tree_view.pack(fill=BOTH, expand=True)

    def show_data(self):
        '''
        Show the employee information
        :return:
        '''
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        EmployeeDB.show_search_data(self)

    def create_buttons(self):
        '''
        Create buttons
        :return:
        '''
        button_frame = Frame(self)
        button_frame.pack(side=BOTTOM, padx=10, pady=10)

        pwd_button = Button(button_frame, text='查看账号密码', command=self.query_name_and_pwd)
        pwd_button.pack(side=LEFT, padx=10)

        refresh_button = Button(button_frame, text='刷新数据', command=self.refresh_data)
        refresh_button.pack(side=LEFT)

    def query_name_and_pwd(self):
        '''
        Query the name and password
        :return:
        '''
        if self.permission == 'admin':
            EmployeePasswordPage(Tk())
        else:
            tkinter.messagebox.showwarning(title='警告', message='仅限管理员使用！')

    def refresh_data(self):
        '''
        Refresh the data
        :return:
        '''
        self.show_data()

    def pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        ModifyFrame.pack_forget(self.modify_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        AddFrame.pack_forget(self.add_frame)
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        FoodSearchFrame.pack_forget(self.food_search_frame)


class FoodSearchFrame(Frame):
    def __init__(self, master, **kw):
        '''
        Initialize the FoodSearchFrame
        :param master:
        :param kw:
        '''
        self.master = master
        self.SortDir = True
        Frame.__init__(self, master)
        self.dataCols = ('id', 'name', 'price', 'category')
        self.tree = Treeview(self, columns=self.dataCols)
        self.create_page()
        self.show_data()
        self.create_buttons()

    def create_page(self):
        '''
        Create a page to search the food information
        :return:
        '''
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # Setup column heading
        self.tree.heading('#0', text='图片', anchor='center')
        self.tree.column('#0', width=75, anchor='center')

        self.tree.heading('#1', text='编号', anchor='center')
        self.tree.column('#1', width=50, anchor='center')

        self.tree.heading('#2', text='名字', anchor='center')
        self.tree.column('#2', width=100, anchor='center')

        self.tree.heading('#3', text='价格', anchor='center')
        self.tree.column('#3', width=50, anchor='center')

        self.tree.heading('#4', text='类别', anchor='center')
        self.tree.column('#4', width=75, anchor='center')

        style = Style(self.master)
        style.configure('Treeview', rowheight=50)

    def show_data(self):
        '''
        Show the food information
        :return:
        '''
        self.reload_info()
        '''
        for i in range(len(self.img)):
            self.tree.insert('', 'end', image=self.photo[i], value=(
                i+1,
                BarFoodDB.display_name_use_id(i+1),
                BarFoodDB.display_price_use_id(i+1),
                BarFoodDB.display_category_use_id(i+1)
            ))
        '''
        i = 1
        j = 0
        # print(BarFoodDB.get_last_id())
        length = len(self.photo)
        while i <= BarFoodDB.get_last_id() and j <= length:
            if BarFoodDB.id_is_exist(i):
                self.tree.insert('', 'end', image=self.photo[j], value=(
                    i,
                    BarFoodDB.display_name_use_id(i),
                    BarFoodDB.display_price_use_id(i),
                    BarFoodDB.display_category_use_id(i)
                ))
                j += 1
            i += 1

    def create_buttons(self):
        '''
        Create buttons
        :return:
        '''
        button_frame = Frame(self)
        button_frame.grid()

        refresh_button = Button(button_frame, text='刷新数据', command=self.refresh)
        refresh_button.grid(pady=10, row=2, column=0)

        desc_button = Button(button_frame, text='降序', command=self.desc_sort)
        desc_button.grid(row=2, column=1, padx=10)

    def refresh(self):
        '''
        Refresh the data
        :return:
        '''
        self.clear_treeview()
        self.show_data()

    def reload_info(self):
        '''
        Reload the information
        :return:
        '''
        self.img = BarFoodDB.food_image_address()
        self.photo = []
        for i in range(len(self.img)):
            self.photo.append(PhotoImage(file=self.img[i]))

    def desc_sort(self):
        '''
        Sort the data
        :return:
        '''
        self.clear_treeview()
        self.reload_info()
        i = BarFoodDB.get_last_id()
        j = len(self.photo)
        while i >= 1:
            if BarFoodDB.id_is_exist(i):
                self.tree.insert('', 'end', image=self.photo[j - 1], value=(
                    i,
                    BarFoodDB.display_name_use_id(i),
                    BarFoodDB.display_price_use_id(i),
                    BarFoodDB.display_category_use_id(i)
                ))
                j -= 1
            i -= 1

    def clear_treeview(self):
        '''
        Clear the treeview
        :return:
        '''
        self.tree.delete(*self.tree.get_children())

    def food_pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        ModifyFrame.pack_forget(self.modify_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        AddFrame.pack_forget(self.add_frame)
        SearchFrame.pack_forget(self.search_frame)


class FoodAddFrame(Frame):
    def __init__(self, window):
        '''
        Initialize the FoodAddFrame
        :param window:
        '''
        super().__init__(window)
        self.name = StringVar()
        self.price = IntVar()
        self.category = StringVar()
        self.image_address = StringVar()
        self.status = StringVar()
        self.create_page()

    def create_page(self):
        '''
        Create a page to add the food information
        :return:
        '''
        Label(self).grid(row=0)

        Label(self, text='名字(必填): ').grid(row=1, column=1, pady=2)
        Entry(self, textvariable=self.name).grid(row=1, column=2)

        Label(self, text='价格: ').grid(row=2, column=1, pady=2)
        Entry(self, textvariable=self.price).grid(row=2, column=2)

        Label(self, text='类别: ').grid(row=3, column=1, pady=2)
        Entry(self, textvariable=self.category).grid(row=3, column=2)

        Label(self, text='图片地址: ').grid(row=4, column=1, pady=2)
        Entry(self, textvariable=self.image_address).grid(row=4, column=2)

        Button(self, text='录入', command=self.record_info).grid(row=10, column=2, pady=5, sticky=E)

        Label(self, textvariable=self.status).grid(row=11, column=2, sticky=E)

    def record_info(self):
        '''
        Record the food information
        :return:
        '''
        info = {"name": self.name.get(),
                "price": self.price.get(),
                "category": self.category.get(),
                "image_address": self.image_address.get()}
        if info['name'] == '':
            tkinter.messagebox.showwarning(title='提示', message='名字未填写！')
        elif BarFoodDB.name_is_exist(self.name.get()):
            tkinter.messagebox.showwarning(title='警告', message='该名字已存在，请输入新的名字!')
        else:
            BarFoodDB.add_food(info)
            self.status.set('录入成功！')
            self.clear_add_data()

    def clear_add_data(self):
        '''
        Clear the data in the entry
        :return:
        '''
        self.name.set('')
        self.price.set(0)
        self.category.set('')
        self.image_address.set('')

    def food_pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodSearchFrame.pack_forget(self.food_search_frame)
        ModifyFrame.pack_forget(self.modify_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        AddFrame.pack_forget(self.add_frame)
        SearchFrame.pack_forget(self.search_frame)


class FoodModifyFrame(Frame):
    def __init__(self, window):
        '''
        Initialize the FoodModifyFrame
        :param window:
        '''
        super().__init__(window)
        self.name = StringVar()
        self.price = IntVar()
        self.category = StringVar()
        self.image_address = StringVar()
        self.status = StringVar()
        self.check = False
        self.old_name = None
        self.create_page()

    def create_page(self):
        '''
        Create a page to modify the food information
        :return:
        '''
        Label(self, text='请先输入名字获取信息: ').grid(row=0,column=2)

        Label(self, text='名字(必填): ').grid(row=1, column=1, pady=2)
        Entry(self, textvariable=self.name).grid(row=1, column=2)

        Label(self, text='价格: ').grid(row=2, column=1, pady=2)
        Entry(self, textvariable=self.price).grid(row=2, column=2)

        Label(self, text='类别: ').grid(row=3, column=1, pady=2)
        Entry(self, textvariable=self.category).grid(row=3, column=2)

        Label(self, text='图片地址: ').grid(row=4, column=1, pady=2)
        Entry(self, textvariable=self.image_address).grid(row=4, column=2)

        Button(self, text='查询', command=self.set_info).grid(row=5, column=1, pady=5, sticky=E)
        Button(self, text='修改', command=self.update_info).grid(row=5, column=2, pady=10, sticky=E)

        Label(self, textvariable=self.status).grid(row=6, column=2, sticky=E)

    def set_info(self):
        '''
        Set the information
        :return:
        '''
        self.status.set('')
        if not self.name.get():
            tkinter.messagebox.showwarning(title='提示', message='名字未输入!')
        elif not BarFoodDB.name_is_exist(self.name.get()):
            tkinter.messagebox.showwarning(title='提示', message='名字不存在或已删除!')
        else:
            self.check = True
            self.old_name = self.name.get()
            info = BarFoodDB.all_info(self.name.get())
            self.price.set(info['price'])
            self.category.set(info['category'])
            self.image_address.set(info['image_address'])
            self.img = PhotoImage(file=self.image_address.get())
            Label(self, image=self.img).grid(row=4, column=3, padx=10)

    def update_info(self):
        '''
        Update the information
        :return:
        '''
        if self.check:
            updated_info = {'id': BarFoodDB.all_info(self.old_name)['id'],
                            'name': self.name.get(),
                            'price': self.price.get(),
                            'category': self.category.get(),
                            'image_address': self.image_address.get()}
            # print(updated_info)
            if not self.is_valid_image(updated_info['image_address']):
                tkinter.messagebox.showwarning(title='提示', message='图片不存在或已删除，请填写正确的图片地址!')
            else:
                # print('yes')
                BarFoodDB.update_all_data(updated_info)
                self.status.set('修改成功!')
                self.clear_data()
        else:
            tkinter.messagebox.showwarning(title='提示', message='请先填写名字并点击查询按钮')

    def is_valid_image(self, file_path):
        '''
        Check the image is valid or not
        :param file_path:
        :return:
        '''
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, file_path)
        try:
            with Image.open(full_path) as img:
                img.verify()
            return True
        except (IOError, SyntaxError):
            return False

    def clear_data(self):
        '''
        Clear the data in the entry
        :return:
        '''
        self.name.set('')
        self.price.set('')
        self.category.set('')
        self.image_address.set('')
        self.img = None

    def food_pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        FoodSearchFrame.pack_forget(self.food_search_frame)
        FoodDeleteFrame.pack_forget(self.food_delete_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        ModifyFrame.pack_forget(self.modify_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        AddFrame.pack_forget(self.add_frame)
        SearchFrame.pack_forget(self.search_frame)


class FoodDeleteFrame(Frame):
    def __init__(self, window):
        '''
        Initialize the FoodDeleteFrame
        :param window:
        '''
        super().__init__(window)
        self.window = window
        self.SortDir = True
        Frame.__init__(self, window)
        self.dataCols = ('id', 'name', 'price', 'category', 'image_address')
        self.tree = Treeview(self, columns=self.dataCols, height=1)
        self.name = StringVar()
        self.status = StringVar()
        self.create_page()

    def create_page(self):
        '''
        Create a page to delete the food information
        :return:
        '''
        Label(self, text='请输入菜名: ').grid(row=0, column=0)
        Entry(self, textvariable=self.name).grid(row=1, column=0)
        Button(self, text='确认', command=self.show_table).grid(row=2, pady=5)

    def show_table(self):
        '''
        Show the food information
        :return:
        '''
        self.status.set('')
        for _ in map(self.tree.delete, self.tree.get_children('')):
            pass
        if self.name.get() == '':
            tkinter.messagebox.showwarning(title='提示', message='未输入名字，请先键入名字!')
        elif not BarFoodDB.name_is_exist(self.name.get()):
            tkinter.messagebox.showwarning(title='提示', message='该菜色不存在或已删除!')
        else:
            self.tree.grid(row=3, column=0, sticky=NSEW)

            self.tree.heading('#0', text='图片', anchor='center')
            self.tree.column('#0', width=75, anchor='center')

            self.tree.heading('#1', text='编号', anchor='center')
            self.tree.column('#1', width=50, anchor='center')

            self.tree.heading('#2', text='名字', anchor='center')
            self.tree.column('#2', width=100, anchor='center')

            self.tree.heading('#3', text='价格', anchor='center')
            self.tree.column('#3', width=60, anchor='center')

            self.tree.heading('#4', text='类别', anchor='center')
            self.tree.column('#4', width=60, anchor='center')

            self.tree.heading('#5', text='图片地址', anchor='center')
            self.tree.column('#5', width=250, anchor='center')

            style = Style(self.master)
            style.configure('Treeview', rowheight=50)

            self.insert_data()

            Label(self, text='确认删除以上菜色信息: ').grid(row=4, column=0, pady=10, sticky=W)
            Label(self, textvariable=self.status).grid(row=7)
            Button(self, text='删除', command=self.delete_data).grid(row=5, column=0, sticky=W)
            Button(self, text='退出', command=self.tree.quit).grid(row=6, column=0, pady=5, sticky=W)

    def insert_data(self):
        '''
        Insert the data
        :return:
        '''
        self.info = BarFoodDB.all_info(self.name.get())
        self.img = PhotoImage(file=self.info['image_address'])
        # print(self.img)
        self.tree.insert('', 'end', image=self.img, value=(
            self.info['id'],
            self.info['name'],
            self.info['price'],
            self.info['category'],
            self.info['image_address']
        ))

    def delete_data(self):
        '''
        Delete the food information
        :return:
        '''
        food_id = BarFoodDB.display_id_use_name(self.name.get())
        BarFoodDB.delete_one_row(food_id)
        self.status.set('删除成功')

    def food_pack_forget_other(self):
        '''
        Pack forget other frames
        :return:
        '''
        FoodModifyFrame.pack_forget(self.food_modify_frame)
        FoodSearchFrame.pack_forget(self.food_search_frame)
        FoodAddFrame.pack_forget(self.food_add_frame)
        ModifyFrame.pack_forget(self.modify_frame)
        DeleteFrame.pack_forget(self.delete_frame)
        AddFrame.pack_forget(self.add_frame)
        SearchFrame.pack_forget(self.search_frame)
