from tkinter import *
from tkinter import ttk
from tkinter import font, messagebox
from PIL import ImageTk, Image

import ManipulateDB
from AdminPage import AdminPage
from MemberPage import MemberPage
from PresidentPage import PresidentPage

class LoginPage:
    def __init__(self, window: Tk):
        self.window = window
        self.window.title("社团管理系统")
        self.window.geometry("1280x720")
        self.window.resizable(0, 0)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.window.iconphoto(True, PhotoImage(file="SCAU.png"))

        self.page = ttk.Frame(self.window)
        self.page.pack(fill='both', expand=True)

        self.username = StringVar()
        self.password = StringVar()
        self.role = StringVar()

        label_font = font.Font(size=16, weight='bold')
        entry_font = font.Font(size=16, weight='bold')

        self.scau_image = ImageTk.PhotoImage(Image.open("SCAU.png").resize((75, 75)))
        scau_logo_label = ttk.Label(self.page, image=self.scau_image)
        scau_logo_label.place(relx=0.5, rely=0, x=-200, y=200)  # Adjusted y-coordinate

        system_title_label = ttk.Label(self.page, text='SCAU 社团管理系统', font=font.Font(size=24))
        system_title_label.place(relx=0.5, rely=0, x=-100, y=220)  # Adjusted y-coordinate

        username_label = ttk.Label(self.page, text='账号:', font=label_font)
        username_label.place(relx=0.5, rely=0, x=-200, y=300)  # Adjusted y-coordinate

        username_entry = ttk.Entry(self.page, textvariable=self.username, font=entry_font)
        username_entry.place(relx=0.5, rely=0, x=-100, y=300)  # Adjusted y-coordinate

        password_label = ttk.Label(self.page, text='密码:', font=label_font)
        password_label.place(relx=0.5, rely=0, x=-200, y=350)  # Adjusted y-coordinate

        password_entry = ttk.Entry(self.page, textvariable=self.password, font=entry_font, show="*")
        password_entry.place(relx=0.5, rely=0, x=-100, y=350)  # Adjusted y-coordinate

        role_label = ttk.Label(self.page, text='身份:', font=label_font)
        role_label.place(relx=0.5, rely=0, x=-200, y=400)  # Adjusted y-coordinate

        role_member = ttk.Radiobutton(self.page, text="社员", variable=self.role, value="社员")
        role_member.place(relx=0.5, rely=0, x=-100, y=400)  # Adjusted y-coordinate

        role_president = ttk.Radiobutton(self.page, text="社长", variable=self.role, value="社长")
        role_president.place(relx=0.5, rely=0, x=0, y=400)  # Adjusted y-coordinate

        role_admin = ttk.Radiobutton(self.page, text="管理员", variable=self.role, value="管理员")
        role_admin.place(relx=0.5, rely=0, x=90, y=400)  # Adjusted y-coordinate

        login_button = ttk.Button(self.page, text='登录', command=self.login_check, width=10)
        login_button.place(relx=0.5, rely=0, x=-100, y=450)  # Adjusted y-coordinate

        quit_button = ttk.Button(self.page, text='退出', command=self.page.quit, width=10, )
        quit_button.place(relx=0.5, rely=0, x=65, y=450)  # Adjusted y-coordinate

        create_club_button = ttk.Button(self.page, text='创建社团', command=self.create_club, width=10)
        create_club_button.place(relx=0.5, rely=0, x=-100, y=500)  # Adjusted y-coordinate

        register_button = ttk.Button(self.page, text='社员注册', command=self.register, width=10)
        register_button.place(relx=0.5, rely=0, x=65, y=500)  # Adjusted y-coordinate

    def login_check(self):
        if self.username.get() == '' or self.password.get() == '' or self.role.get() == '':
            messagebox.showwarning('警告', '账号、密码或身份不能为空！')
            return
        is_user_exist = ManipulateDB.is_user_in_exist(self.username.get(), self.password.get())
        role = self.role.get()
        if is_user_exist:
            legal_role = ManipulateDB.get_role_by_usr_and_pwd(self.username.get(), self.password.get())
            if role == '社员' and '社员' == legal_role:
                MemberPage(self.window, self.username.get(), self.password.get(), self.role.get())
            elif role == '社长' and '社长' == legal_role:
                PresidentPage(self.window, self.username.get(), self.password.get(), self.role.get())
            elif role == '管理员' and '管理员' == legal_role:
                AdminPage(self.window)
            else:
                messagebox.showerror('错误', '身份错误！')
                return
            self.page.destroy()
        else:
            messagebox.showerror('错误', '账号或密码错误！')
            return

    def create_club(self):
        self.clear()
        label_font = font.Font(size=13, weight='bold')
        entry_font = font.Font(size=16, weight='bold')
        button_font = font.Font(size=16)

        ttk.Label(self.page, text='社团名称:', font=label_font).place(x=490, y=100)
        self.club_name = StringVar()
        ttk.Entry(self.page, textvariable=self.club_name, font=entry_font).place(x=600, y=100)

        ttk.Label(self.page, text='社团类型:', font=label_font).place(x=490, y=150)
        self.club_type = StringVar()
        ttk.Entry(self.page, textvariable=self.club_type, font=entry_font).place(x=600, y=150)

        ttk.Label(self.page, text='社长:', font=label_font).place(x=490, y=200)
        self.principal = StringVar()
        ttk.Entry(self.page, textvariable=self.principal, font=entry_font).place(x=600, y=200)

        ttk.Label(self.page, text='学院:', font=label_font).place(x=490, y=250)
        self.college = StringVar()
        ttk.Entry(self.page, textvariable=self.college, font=entry_font).place(x=600, y=250)

        ttk.Label(self.page, text='指导老师:', font=label_font).place(x=490, y=300)
        self.advisor = StringVar()
        ttk.Entry(self.page, textvariable=self.advisor, font=entry_font).place(x=600, y=300)

        ttk.Label(self.page, text='联系方式:', font=label_font).place(x=490, y=350)
        self.contact = StringVar()
        ttk.Entry(self.page, textvariable=self.contact, font=entry_font).place(x=600, y=350)

        ttk.Label(self.page, text='社团简介:', font=label_font).place(x=490, y=400)
        self.description = StringVar()
        ttk.Entry(self.page, textvariable=self.description, font=entry_font).place(x=600, y=400)

        ttk.Label(self.page, text='社长账号:', font=label_font).place(x=490, y=450)
        self.account = StringVar()
        ttk.Entry(self.page, textvariable=self.account, font=entry_font).place(x=600, y=450)

        ttk.Label(self.page, text='社长密码:', font=label_font).place(x=490, y=500)
        self.pwd = StringVar()
        ttk.Entry(self.page, textvariable=self.pwd, font=entry_font).place(x=600, y=500)

        ttk.Button(self.page, text='提交', command=self.submit_club, width=10).place(x=600, y=550)
        ttk.Button(self.page, text='返回', command=self.to_login, width=10).place(x=785, y=550)

    def clear(self):
        for widget in self.page.winfo_children():
            widget.destroy()

    def submit_club(self):
        info = {'ClubName': self.club_name.get(),
                'Type': self.club_type.get(),
                'Principal': self.principal.get(),
                'College': self.college.get(),
                'Advisor': self.advisor.get(),
                'Contact': self.contact.get(),
                'Description': self.description.get(),
                'Username': self.account.get(),
                'Password': self.pwd.get()}
        print(info)
        if any(value == '' for value in info.values()):
            messagebox.showwarning('警告', '社团信息未填写完整！')
            return
        elif ManipulateDB.is_club_exist(info['ClubName']):
            messagebox.showwarning('错误', '社团已存在！')
            return
        elif ManipulateDB.is_user_in_exist(info['Username'], info['Password']):
            messagebox.showwarning('错误', '账号已存在！')
            return
        else:
            ManipulateDB.add_approval(info)
            messagebox.showinfo('提示', '提交成功！')

    def register(self):
        self.clear()
        label_font = font.Font(size=13, weight='bold')
        entry_font = font.Font(size=16, weight='bold')
        button_font = font.Font(size=16)

        ttk.Label(self.page, text='账号:', font=label_font).place(x=490, y=100)
        self.new_username = StringVar()
        ttk.Entry(self.page, textvariable=self.new_username, font=entry_font).place(x=600, y=100)

        ttk.Label(self.page, text='密码:', font=label_font).place(x=490, y=150)
        self.new_password = StringVar()
        ttk.Entry(self.page, textvariable=self.new_password, font=entry_font).place(x=600, y=150)

        ttk.Label(self.page, text='意向社团:', font=label_font).place(x=490, y=200)
        clubs = ManipulateDB.get_club_list()
        self.club = StringVar()
        club_combobox = ttk.Combobox(self.page, textvariable=self.club, font=entry_font, state='readonly')
        club_combobox['values'] = clubs
        club_combobox.place(x=600, y=200)
        ttk.Entry(self.page, textvariable=self.club, font=entry_font).place(x=600, y=200)

        ttk.Label(self.page, text='姓名:', font=label_font).place(x=490, y=250)
        self.name = StringVar()
        ttk.Entry(self.page, textvariable=self.name, font=entry_font).place(x=600, y=250)

        ttk.Label(self.page, text='联系方式:', font=label_font).place(x=490, y=300)
        self.contact = StringVar()
        ttk.Entry(self.page, textvariable=self.contact, font=entry_font).place(x=600, y=300)

        ttk.Label(self.page, text='年级:', font=label_font).place(x=490, y=350)
        self.grade = StringVar()
        ttk.Entry(self.page, textvariable=self.grade, font=entry_font).place(x=600, y=350)

        ttk.Label(self.page, text='专业:', font=label_font).place(x=490, y=400)
        self.major = StringVar()
        ttk.Entry(self.page, textvariable=self.major, font=entry_font).place(x=600, y=400)

        ttk.Label(self.page, text='班级:', font=label_font).place(x=490, y=450)
        self.class_ = StringVar()
        ttk.Entry(self.page, textvariable=self.class_, font=entry_font).place(x=600, y=450)

        ttk.Button(self.page, text='提交', command=self.submit_register).place(x=600, y=500)
        ttk.Button(self.page, text='返回', command=self.to_login).place(x=785, y=500)

    def to_login(self):
        self.clear()
        self.page.destroy()
        self.__init__(self.window)

    def submit_register(self):
        info = {'Username': self.new_username.get(),
                'Password': self.new_password.get(),
                'Club': self.club.get(),
                'Name': self.name.get(),
                'Contact': self.contact.get(),
                'Grade': self.grade.get(),
                'Major': self.major.get(),
                'Class': self.class_.get()}
        print(info)
        if any(value == '' for value in info.values()):
            messagebox.showwarning('警告', '信息未填写完整！')
            return
        elif ManipulateDB.is_user_in_exist(info['Username'], info['Password']):
            messagebox.showwarning('错误', '账号已存在！')
            return
        else:
            ManipulateDB.add_user(info)
            messagebox.showinfo('提示', '注册成功，请等待审核完成！')

if __name__ == '__main__':
    window = Tk()
    LoginPage(window)
    window.mainloop()
