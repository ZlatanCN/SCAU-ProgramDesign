from tkinter import *
from tkinter.ttk import Treeview, Style
import tkinter.messagebox

import ManipulateDB

class ClubFeeFrame(Frame):
    def __init__(self, window: Tk, name: str, club):
        super().__init__(window)
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.style = Style()
        self.name = name
        self.club = club
        self.fee = ManipulateDB.get_fee(self.name, self.club)
        self.create_page()

    def create_page(self):
        Label(self.view, text=self.name + "同学" + ", 您本月还需缴费: ", font=("Helvetica", 14)).pack(side="left", pady=15)
        Label(self.view, text=str(self.fee) + '元', font=("Helvetica", 14)).pack(
            side="left", pady=15)
        Button(self.view, text='缴费', font=("Helvetica", 14), command=self.pay_fee).pack(side="left", pady=15, padx=10)

    def pay_fee(self):
        if self.fee == 0:
            tkinter.messagebox.showerror('错误', '您无需缴费！')
            return
        ManipulateDB.pay_fee(self.name, self.club)
        tkinter.messagebox.showinfo('提示', '缴费成功！')
        self.fee = 0
        self.refresh()

    def refresh(self):
        self.view.destroy()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.create_page()

    def clear(self):
        self.view.destroy()