import re
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style

import ManipulateDB

class EventManageFrame(Frame):
    def __init__(self, window: Tk, club: str):
        super().__init__(window)
        self.view = Frame()
        self.domain_club = club
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.style = Style()
        self.create_page()
        self.show_events()

    def create_page(self):
        columns = ('event_id', 'event_name', 'description', 'venue', 'date', 'contact')

        self.tree_view = Treeview(self.view, show='headings', columns=columns, height=30, selectmode='browse')

        self.tree_view.column('event_id', width=50, anchor='center')
        self.tree_view.column('event_name', width=150, anchor='center')
        self.tree_view.column('description', width=200, anchor='center')
        self.tree_view.column('venue', width=100, anchor='center')
        self.tree_view.column('date', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')

        self.tree_view.heading('event_id', text='ID')
        self.tree_view.heading('event_name', text='活动名称')
        self.tree_view.heading('description', text='活动简介')
        self.tree_view.heading('venue', text='活动地点')
        self.tree_view.heading('date', text='活动日期')
        self.tree_view.heading('contact', text='联系方式')

        self.style.configure('Treeview', font=('宋体', 12))

        self.tree_view.pack(fill=BOTH, expand=True)

        Button(self.view, text='修改活动信息', font=("Helvetica", 12), command=self.update_event).pack(side='left',
                                                                                                       padx=10, pady=30)
        Button(self.view, text='删除活动', font=("Helvetica", 12), command=self.delete_event).pack(side='left', padx=10,
                                                                                                   pady=30)

    def show_events(self):
        events = ManipulateDB.get_events(self.domain_club)
        for event in events:
            self.tree_view.insert('', 'end', values=(event[0],) + event[2:])

    def update_event(self):
        selected_item = self.tree_view.item(self.tree_view.focus())
        if not selected_item['values']:
            messagebox.showwarning('警告', '请选择一个活动！')
            return
        self.create_update_frame(selected_item)

    def create_update_frame(self, selected_item):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.event_id = selected_item['values'][0]
        self.new_event_name = StringVar(value=selected_item['values'][1])
        self.new_event_description = StringVar(value=selected_item['values'][2])
        self.new_event_venue = StringVar(value=selected_item['values'][3])
        self.new_event_date = StringVar(value=selected_item['values'][4])
        self.new_event_contact = StringVar(value=selected_item['values'][5])

        Label(self.view, text='活动ID: ', font=("Helvetica", 12)).grid(row=0, column=0, sticky='e', pady=2)
        Label(self.view, text=self.event_id).grid(row=0, column=1, sticky='w')

        Label(self.view, text='活动名称: ', font=("Helvetica", 12)).grid(row=1, column=0, sticky='e', pady=2)
        Entry(self.view, textvariable=self.new_event_name).grid(row=1, column=1, sticky='w')

        Label(self.view, text='活动简介: ', font=("Helvetica", 12)).grid(row=2, column=0, sticky='e', pady=2)
        Entry(self.view, textvariable=self.new_event_description).grid(row=2, column=1, sticky='w')

        Label(self.view, text='活动地点: ', font=("Helvetica", 12)).grid(row=3, column=0, sticky='e', pady=2)
        Entry(self.view, textvariable=self.new_event_venue).grid(row=3, column=1, sticky='w')

        Label(self.view, text='活动日期: ', font=("Helvetica", 12)).grid(row=4, column=0, sticky='e', pady=2)
        Entry(self.view, textvariable=self.new_event_date).grid(row=4, column=1, sticky='w')

        Label(self.view, text='联系方式: ', font=("Helvetica", 12)).grid(row=5, column=0, sticky='e', pady=2)
        Entry(self.view, textvariable=self.new_event_contact).grid(row=5, column=1, sticky='w')

        Button(self.view, text='确认修改', font=("Helvetica", 12), command=self.update_event_info).grid(row=6, column=1,
                                                                                                        sticky='w',
                                                                                                        pady=10)
        Button(self.view, text='返回', font=("Helvetica", 12), command=self.back).grid(row=6, column=2, pady=10)

    def update_event_info(self):
        new_item = {'EventId': self.event_id,
                    'Name': self.new_event_name.get(),
                    'Description': self.new_event_description.get(),
                    'Venue': self.new_event_venue.get(),
                    'Date': self.new_event_date.get(),
                    'Contact': self.new_event_contact.get()}
        ManipulateDB.update_event_info(new_item)
        messagebox.showinfo('提示', '修改成功！')

    def back(self):
        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.tree_view = None
        self.create_page()
        self.show_events()

    def delete_event(self):
        item = self.tree_view.item(self.tree_view.focus())
        if not item['values']:
            messagebox.showwarning('警告', '请选择一个活动！')
            return
        confirmation = messagebox.askyesno('确认', '确定删除该活动吗？')
        if confirmation:
            ManipulateDB.delete_event(item['values'][0])
            self.back()

    def clear(self):
        self.view.destroy()
        for widget in self.winfo_children():
            widget.destroy()
