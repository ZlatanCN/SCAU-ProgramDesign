import re
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox

import ManipulateDB

class EventPublishFrame(Frame):
    def __init__(self, window: Tk, club: str):
        super().__init__(window)
        self.domain_club = club
        self.new_event_name = StringVar()
        self.new_event_description = StringVar()
        self.new_event_venue = StringVar()
        self.new_event_date = StringVar()
        self.new_event_contact = StringVar()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='s')
        self.tree_view = None
        self.style = ttk.Style()
        self.create_page()
        self.show_events()

    def create_page(self):
        font_style = ('Helvetica', 12)
        padx_value = 5
        pady_value = 5

        columns = ('event_id', 'club', 'event', 'description', 'venue', 'date', 'contact')

        self.tree_view = ttk.Treeview(self.view, show='headings', columns=columns, height=10)

        self.tree_view.column('event_id', width=50, anchor='center')
        self.tree_view.column('club', width=150, anchor='center')
        self.tree_view.column('event', width=150, anchor='center')
        self.tree_view.column('description', width=200, anchor='center')
        self.tree_view.column('venue', width=100, anchor='center')
        self.tree_view.column('date', width=100, anchor='center')
        self.tree_view.column('contact', width=100, anchor='center')

        self.tree_view.heading('event_id', text='ID')
        self.tree_view.heading('club', text='所属社团')
        self.tree_view.heading('event', text='活动名称')
        self.tree_view.heading('description', text='活动简介')
        self.tree_view.heading('venue', text='活动地点')
        self.tree_view.heading('date', text='活动日期')
        self.tree_view.heading('contact', text='联系方式')

        self.style.configure('Treeview', font=font_style)

        self.tree_view.grid(row=0, column=0, columnspan=2, sticky='s')

        ttk.Label(self.view, text='活动名称: ', font=font_style).grid(row=1, column=0, sticky='e', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_event_name).grid(row=1, column=1, sticky='w', pady=pady_value, padx=padx_value)

        ttk.Label(self.view, text='活动简介: ', font=font_style).grid(row=2, column=0, sticky='e', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_event_description).grid(row=2, column=1, sticky='w', pady=pady_value, padx=padx_value)

        ttk.Label(self.view, text='活动地点: ', font=font_style).grid(row=3, column=0, sticky='e', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_event_venue).grid(row=3, column=1, sticky='w', pady=pady_value, padx=padx_value)

        ttk.Label(self.view, text='活动日期: ', font=font_style).grid(row=4, column=0, sticky='e', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_event_date).grid(row=4, column=1, sticky='w', pady=pady_value, padx=padx_value)
        ttk.Label(self.view, text='(格式: 2024-02-05)', font=("Helvetica", 10)).grid(row=4, column=1)

        ttk.Label(self.view, text='联系方式: ', font=font_style).grid(row=5, column=0, sticky='e', pady=pady_value)
        ttk.Entry(self.view, textvariable=self.new_event_contact).grid(row=5, column=1, sticky='w', pady=pady_value, padx=padx_value)

        ttk.Button(self.view, text='发布', command=self.publish_event).grid(row=6, column=1, pady=pady_value, sticky='e')

    def show_events(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children('')):
            pass
        events = ManipulateDB.get_events(self.domain_club)
        for event in events:
            self.tree_view.insert('', 'end', values=event)

    def publish_event(self):
        new_event = {"EventName": self.new_event_name.get(),
                     "Description": self.new_event_description.get(),
                     "Venue": self.new_event_venue.get(),
                     "Date": self.new_event_date.get(),
                     "Contact": self.new_event_contact.get()}
        is_legal = self.validate_legality(new_event)
        if is_legal:
            ManipulateDB.publish_event(new_event, self.domain_club)
            messagebox.showinfo('提示', '发布成功！')
            self.refresh()

    def validate_legality(self, new_event: dict):
        flag = True
        if any(x == '' for x in new_event.values()):
            messagebox.showwarning('警告', '活动信息未填写完整')
            flag = False
        elif not re.match(r'\d{4}-\d{2}-\d{2}', new_event["Date"]):
            messagebox.showwarning('警告', '日期格式错误！')
            flag = False
        elif datetime.strptime(new_event["Date"], '%Y-%m-%d') < datetime.now():
            messagebox.showwarning('警告', '活动日期不能早于今天！')
            flag = False
        return flag

    def clear(self):
        self.view.destroy()

    def refresh(self):
        self.new_event_date.set('')
        self.new_event_description.set('')
        self.new_event_name.set('')
        self.new_event_venue.set('')
        self.new_event_contact.set('')

        self.clear()
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='s')
        self.create_page()
        self.show_events()
