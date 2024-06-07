from tkinter import *
from tkinter.ttk import Style

from ClubFeeFrame import ClubFeeFrame
from ClubSearchFrame import ClubSearchFrame
from ClubJoinFrame import ClubJoinFrame
from EventCheckInFrame import EventCheckInFrame
from EventRegisterFrame import EventRegisterFrame

import ManipulateDB

class MemberPage:
    def __init__(self, window: Tk, username: str, password: str, role: str):
        self.role = role
        self.username = username
        self.password = password
        self.name = ManipulateDB.get_name_by_usr_and_pwd(username, password)
        self.club = ManipulateDB.get_club_by_usr_and_pwd(username, password)
        self.window = window
        self.window.title("社员端")
        self.window.geometry("1280x720")
        self.window.iconphoto(True, PhotoImage(file="SCAU.png"))
        self.style = Style()
        self.style.theme_use('default')
        self.create_menu_bar()
        self.frames = {'search': None, 'join': None, 'event_register': None, 'club_fee': None, 'event_check_in': None}

    def create_menu_bar(self):
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        menubar.add_command(label='社团查询', command=self.show_club_search_frame)
        menubar.add_command(label='社团加入', command=self.show_club_join_frame)
        menubar.add_command(label='活动报名', command=self.show_event_register_frame)
        menubar.add_command(label='缴费管理', command=self.show_club_fee_frame)
        menubar.add_command(label='签到管理', command=self.show_event_check_in_frame)
        menubar.add_command(label='返回主页', command=self.to_login_page)

    def show_club_search_frame(self):
        self.clear_other_frames('search')
        self.search_frame = ClubSearchFrame(self.window)
        self.frames['search'] = self.search_frame

    def show_club_join_frame(self):
        self.clear_other_frames('join')
        self.join_frame = ClubJoinFrame(self.window)
        self.frames['join'] = self.join_frame

    def show_event_register_frame(self):
        self.clear_other_frames('event_register')
        self.event_register_frame = EventRegisterFrame(self.window, self.username, self.password)
        self.frames['event_register'] = self.event_register_frame

    def show_club_fee_frame(self):
        self.clear_other_frames('club_fee')
        self.club_fee_frame = ClubFeeFrame(self.window, self.name, self.club)
        self.frames['club_fee'] = self.club_fee_frame

    def show_event_check_in_frame(self):
        self.clear_other_frames('event_check_in')
        self.event_check_in_frame = EventCheckInFrame(self.window, self.name)
        self.frames['event_check_in'] = self.event_check_in_frame

    def to_login_page(self):
        self.window.destroy()
        from LoginPage import LoginPage
        LoginPage(Tk())

    def clear_other_frames(self, frame):
        for key in self.frames:
            if key != frame and self.frames[key] is not None:
                self.frames[key].clear()


if __name__ == '__main__':
    window = Tk()
    MemberPage(window, 'user324', 'passuser324', '社员')
    window.mainloop()
