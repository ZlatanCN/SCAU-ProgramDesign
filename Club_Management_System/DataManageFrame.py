from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Button, Style

import ManipulateDB

class DataManageFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.style = Style()
        self.create_page()

    def create_page(self):
        button_font = ("Helvetica", 12)

        Button(self.view, text='导出社团信息', style='TButton', command=self.export_club_info).grid(row=0, column=0, padx=10, pady=15)
        Button(self.view, text='导出成员信息', style='TButton', command=self.export_member_info).grid(row=0, column=1, padx=10, pady=15)
        Button(self.view, text='数据库备份', style='TButton', command=self.backup_db).grid(row=1, column=0, padx=10, pady=15)
        Button(self.view, text='数据库还原', style='TButton', command=self.restore_db).grid(row=1, column=1, padx=10, pady=15)

        self.style.configure('TButton', font=button_font)

    def export_club_info(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            ManipulateDB.export_club_info(folder_path)
            messagebox.showinfo('提示', '导出成功!')

    def export_member_info(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            ManipulateDB.export_member_info(folder_path)
            messagebox.showinfo('提示', '导出成功!')

    def backup_db(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            ManipulateDB.backup_db(folder_path)
            messagebox.showinfo('提示', '备份成功!')

    def restore_db(self):
        file_path = filedialog.askopenfilename()
        if file_path and file_path.endswith('.db'):
            ManipulateDB.restore_db(file_path)
            messagebox.showinfo('提示', '还原成功!')

    def clear(self):
        self.view.destroy()

if __name__ == '__main__':
    window = Tk()
    DataManageFrame(window)
    window.mainloop()
