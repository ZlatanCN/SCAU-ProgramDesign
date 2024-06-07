from tkinter import *
from tkinter import ttk
from ClubAuditFrame import ClubAuditFrame
from DataAnalysisFrame import DataAnalysisFrame
from DataManageFrame import DataManageFrame

class AdminPage:
    def __init__(self, window: Tk):
        self.window = window
        self.window.title("管理员端")
        self.window.geometry("1420x980")
        self.window.iconphoto(True, PhotoImage(file="SCAU.png"))
        self.create_styles()
        self.create_menu_bar()
        self.frames = {'club_audit': None, 'data_manage': None, 'system_setting': None, 'data_analysis': None}

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure('TMenu', font=('Helvetica', 12))
        self.style.configure('TMenuItem', font=('Helvetica', 12))

    def create_menu_bar(self):
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        menubar.add_command(label='社团审核', command=self.show_club_audit_frame)
        menubar.add_command(label='数据管理', command=self.show_data_manage_frame)
        menubar.add_command(label='统计分析', command=self.show_data_analysis_frame)
        menubar.add_command(label='返回主页', command=self.to_login_page)

    def show_club_audit_frame(self):
        self.clear_other_frames('club_audit')
        self.club_audit_frame = ClubAuditFrame(self.window)
        self.frames['club_audit'] = self.club_audit_frame

    def show_data_manage_frame(self):
        self.clear_other_frames('data_manage')
        self.data_manage_frame = DataManageFrame(self.window)
        self.frames['data_manage'] = self.data_manage_frame

    def show_data_analysis_frame(self):
        self.clear_other_frames('data_analysis')
        self.data_analysis_frame = DataAnalysisFrame(self.window)
        self.frames['data_analysis'] = self.data_analysis_frame

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
    AdminPage(window)
    window.mainloop()
