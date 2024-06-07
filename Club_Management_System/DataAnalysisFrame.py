from tkinter import *
from tkinter.ttk import Button, Style
import plotly.express as px

import ManipulateDB


class DataAnalysisFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.view = Frame()
        self.view.place(relx=0.5, rely=0.5, anchor='center')
        self.style = Style()
        self.create_page()

    def create_page(self):
        button_font = ("Helvetica", 12)

        Button(self.view, text='社团规模', style='TButton', command=self.show_club_size)\
            .pack(side='left', padx=10, pady=30)
        Button(self.view, text='社团类型', style='TButton', command=self.show_club_type)\
            .pack(side='left', padx=10, pady=30)
        Button(self.view, text='社团所属学院', style='TButton', command=self.show_club_college)\
            .pack(side='left', padx=10, pady=30)
        Button(self.view, text='年级分布', style='TButton', command=self.show_grade_distribution)\
            .pack(side='left', padx=10, pady=30)

        self.style.configure('TButton', font=button_font)

    def show_club_size(self):
        clubs = ManipulateDB.get_club_size()
        fig = px.bar(clubs, orientation='h')
        fig.update_layout(xaxis_title='Number of Members',
                          yaxis_title='Club',
                          font=dict(size=18),
                          yaxis=dict(tickfont=dict(size=10)))
        fig.show()

    def show_club_type(self):
        clubs = ManipulateDB.get_club_college_and_type()
        fig = px.sunburst(clubs,
                          path=['Type', 'College'],
                          values='Count',
                          color='Count',
                          color_continuous_scale='dense')
        fig.show()

    def show_club_college(self):
        clubs = ManipulateDB.get_club_college()
        fig = px.pie(clubs, values='Count', names=clubs.index, title='社团所属学院')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(title='Club College', font=dict(size=18))
        fig.show()

    def show_grade_distribution(self):
        clubs = ManipulateDB.get_grade_distribution()
        fig = px.bar(clubs)
        fig.update_layout(xaxis_title='Grade', yaxis_title='Number of Members', font=dict(size=18), xaxis=dict(dtick=1))
        fig.show()

    def clear(self):
        self.view.destroy()
