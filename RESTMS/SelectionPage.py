from tkinter import *
from PIL import ImageTk, Image
from EmployeeLoginPage import EmployeeLoginPage
from UserOrderPage import UserOrderPage


class SelectionPage:
    def __init__(self, window: Tk):
        '''
        Initialize the SelectionPage
        :param window:
        '''
        self.window = window
        self.screenwidth = self.window.winfo_screenwidth()
        self.screenheight = self.window.winfo_screenheight()
        self.window.geometry("1920x1080")
        self.window.title('欢迎光临星之果实餐吧~~!')
        self.window.iconphoto(True, PhotoImage(file="Saloon.ico"))

        # Create a page frame
        self.page = Frame(self.window)
        self.page.grid(row=0, column=0, sticky='nsew')

        # Set the background image
        self.background_image = ImageTk.PhotoImage(Image.open("background.png"))
        self.background_label = Label(self.page, image=self.background_image)
        self.background_label.grid(row=0, column=0, sticky='nsew')

        # Create a button for the customer side
        self.customer = Button(self.background_label, text='用户端', width=10, height=3, command=self.turn_to_user_page,
                               bg='DeepSkyBlue', fg='white', font=('华文中宋', 20, 'bold'))
        self.customer.grid(row=0, column=0, padx=245, pady=337)

        # Create a button for the employee side
        self.employee = Button(self.background_label, text='员工端', width=10, height=3, command=self.turn_to_login_page,
                               bg='DeepSkyBlue', fg='white', font=('华文中宋', 20, 'bold'))
        self.employee.grid(row=0, column=1, padx=445, pady=100)

    def turn_to_login_page(self):
        '''
        Destroy the current page frame and navigate to the employee login page
        :return:
        '''
        # Destroy the current page frame and navigate to the employee login page
        self.page.destroy()
        EmployeeLoginPage(self.window)

    def turn_to_user_page(self):
        '''
        Destroy the current page frame and navigate to the user order page
        :return:
        '''
        # Destroy the current page frame and navigate to the user order page
        self.page.destroy()
        UserOrderPage(self.window)


if __name__ == '__main__':
    window = Tk()
    SelectionPage(window)
    window.mainloop()
