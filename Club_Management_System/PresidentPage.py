from tkinter import *
from tkinter import ttk, messagebox

from ClubInfoFrame import ClubInfoFrame
import ManipulateDB
from EventManageFrame import EventManageFrame
from EventPublishFrame import EventPublishFrame
from MemberManageFrame import MemberManageFrame

class PresidentPage(Frame):
    def __init__(self, window: Tk, username: str, password: str, role: str):
        super().__init__(window)
        self.role = role
        self.username = username
        self.password = password
        self.name = ManipulateDB.get_name_by_usr_and_pwd(username, password)
        self.domain_club = ManipulateDB.get_dominant_club(self.name, self.role)
        self.window = window
        self.window.title("社长端")
        self.window.geometry("1420x980")
        self.window.iconphoto(True, PhotoImage(file="SCAU.png"))
        self.create_menu_bar()
        self.frames = {'club_info': None, 'event_publish': None, 'member_manage': None, 'event_manage': None}

    def create_menu_bar(self):
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.map('TButton', foreground=[('active', 'white')], background=[('active', '#4CAF50')])

        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        menubar.add_command(label='社团信息管理', command=self.show_club_info_frame)
        menubar.add_command(label='活动发布', command=self.show_event_publish_frame)
        menubar.add_command(label='成员管理', command=self.show_member_manage_frame)
        menubar.add_command(label='活动管理', command=self.show_event_manage_frame)
        menubar.add_command(label='返回主页', command=self.to_login_page)

    def show_club_info_frame(self):
        self.clear_other_frames('club_info')
        self.club_info_frame = ClubInfoFrame(self.window, self.domain_club)
        self.frames['club_info'] = self.club_info_frame

    def show_event_publish_frame(self):
        self.clear_other_frames('event_publish')
        self.event_publish_frame = EventPublishFrame(self.window, self.domain_club)
        self.frames['event_publish'] = self.event_publish_frame

    def show_member_manage_frame(self):
        self.clear_other_frames('member_manage')
        self.member_manage_frame = MemberManageFrame(self.window, self.domain_club)
        self.frames['member_manage'] = self.member_manage_frame

    def show_event_manage_frame(self):
        self.clear_other_frames('event_manage')
        self.event_manage_frame = EventManageFrame(self.window, self.domain_club)
        self.frames['event_manage'] = self.event_manage_frame

    def to_login_page(self):
        self.window.destroy()
        from LoginPage import LoginPage
        LoginPage(Tk())


    def clear_other_frames(self, frame):
        for key in self.frames:
            if self.frames[key] is not None:
                self.frames[key].clear()

if __name__ == '__main__':
    window = Tk()
    PresidentPage(window, 'zjy', 'zjy', '社长')
    window.mainloop()
