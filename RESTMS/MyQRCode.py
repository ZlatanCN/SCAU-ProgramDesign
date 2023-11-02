from tkinter import *
from PIL import Image, ImageTk

class MyQRCode(Frame):
    def __init__(self, window: Tk):
        '''
        Initialize the MyQRCode
        :param window:
        '''
        Frame.__init__(self, window)
        self.window = window
        self.window.title('付款')
        self.window.iconphoto(True, PhotoImage(file="Saloon.ico"))
        self.my_qr_code()

    def my_qr_code(self):
        '''
        Create a QR code
        :return:
        '''
        self.image = Image.open("my_qr_code.png")
        self.qr_code = ImageTk.PhotoImage(self.image)
        self.label = Label(self.window, image=self.qr_code)
        self.label.pack()


if __name__ == '__main__':
    window = Tk()
    MyQRCode(window)
    window.mainloop()