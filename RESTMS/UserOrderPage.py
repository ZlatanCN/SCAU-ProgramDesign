from tkinter import *
from tkinter.ttk import Treeview, Style

import BarFoodDB
from MyQRCode import MyQRCode

class UserOrderPage(Frame):
    columns = ('name', 'price')

    def __init__(self, window: Tk):
        '''
        Initialize the UserOrderPage
        :param window:
        '''
        self.window = window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 1250) // 2
        y = (screen_height - 750) // 2
        self.window.geometry(f"1250x750+{x}+{y}")
        self.window.title('点菜')
        self.window.iconphoto(True, PhotoImage(file="Saloon.ico"))
        self.checkout = IntVar()
        self.create_image_list()
        Frame.__init__(self, window)
        self.create_labels()
        self.create_buttons()
        self.show_data()
        self.init_bill()

    def create_image_list(self):
        '''
        Create a list to store the images
        :return:
        '''
        self.quick_meal_images = []
        self.dish_images = []
        self.staple_images = []
        self.soup_images = []
        self.snack_images = []
        self.dessert_images = []
        self.drink_images = []

    def show_data(self):
        '''
        Show the data
        :return:
        '''
        self.show_quick_meal()
        self.show_dish()
        self.show_staple()
        self.show_soup()
        self.show_snack()
        self.show_dessert()
        self.show_drink()

    def create_labels(self):
        '''
        Create labels
        :return:
        '''
        # First row
        Label(text='简餐').grid(row=0, column=0)
        Label(text='            ').grid(row=1, column=1)
        Label(text='菜品').grid(row=0, column=2)
        Label(text='            ').grid(row=1, column=3)
        Label(text='小吃').grid(row=0, column=4)
        Label(text='            ').grid(row=1, column=5)
        Label(text='饮品').grid(row=0, column=6)

        # Second row
        Label(text='主食').grid(row=3, column=0)
        Label(text='            ').grid(row=2, column=1)
        Label(text='汤类').grid(row=3, column=2)
        Label(text='            ').grid(row=2, column=3)
        Label(text='甜品').grid(row=3, column=4)
        Label(text='            ').grid(row=2, column=5)
        Label(text='账单').grid(row=3, column=6)
        Label(text='    总计:').grid(row=3, column=7)
        Label(textvariable=self.checkout).grid(row=3, column=8)

    def create_buttons(self):
        '''
        Create buttons
        :return:
        '''
        Button(text='付款', command=self.pay_for_me).grid(row=4, column=7, padx=15)
        Button(text='退出', command=self.window.quit).grid(row=4, column=9, padx=15)
        Button(text='清空', command=self.delete_rows_of_bill).grid(row=4, column=8)

    def insert_data(self, images, tree, category):
        '''
        Insert data into the treeview
        :param images:
        :param tree:
        :param category:
        :return:
        '''
        i = 1
        while i <= BarFoodDB.get_last_id():
            if BarFoodDB.id_is_exist(i) and BarFoodDB.get_category_use_id(i) == category:
                img = PhotoImage(file=BarFoodDB.get_img_use_id(i))
                images.append(img)
                tree.insert('', 'end', image=img, value=(
                    BarFoodDB.display_name_use_id(i),
                    BarFoodDB.display_price_use_id(i)
                ))
            i += 1

    def init_treeview(self, tree, row, col):
        '''
        Initialize the treeview
        :param tree:
        :param row:
        :param col:
        :return:
        '''
        tree.grid(row=row, column=col)

        tree.heading('#0', text='图片', anchor='center')
        tree.column('#0', width=75, anchor='center')

        tree.heading('#1', text='名字', anchor='center')
        tree.column('#1', width=100, anchor='center')

        tree.heading('#2', text='价格', anchor='center')
        tree.column('#2', width=50, anchor='center')

        style = Style(self.window)
        style.configure('Treeview', rowheight=50)

    def init_bill(self):
        '''
        Initialize the bill
        :return:
        '''
        self.bill_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6, show='headings')
        self.bill_tree.grid(row=4, column=6)

        self.bill_tree.heading('name', text='名字')
        self.bill_tree.column('name', width=100, anchor='center')

        self.bill_tree.heading('price', text='价格')
        self.bill_tree.column('price', width=100, anchor='center')

        def delete_the_row(event):
            for item in self.bill_tree.selection():
                item_text = self.bill_tree.item(item, "values")
                self.bill_tree.delete(item)
                self.checkout.set(self.checkout.get() - int(item_text[1]))

        self.bill_tree.bind('<ButtonRelease-1>', delete_the_row)

    def delete_rows_of_bill(self):
        '''
        Delete all the rows of the bill
        :return:
        '''
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
        self.checkout.set(0)

    def pay_for_me(self):
        '''
        Pay for the meal
        :return:
        '''
        MyQRCode(Toplevel(self.window))

    def show_quick_meal(self):
        '''
        Show the quick meal
        :return:
        '''
        self.quick_meal_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.quick_meal_tree, 1, 0)
        self.insert_data(self.quick_meal_images, self.quick_meal_tree, '简餐')

        def insert_to_bill(event):
            for item in self.quick_meal_tree.selection():
                item_text = self.quick_meal_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.quick_meal_tree.bind('<ButtonRelease-1>', insert_to_bill)

    def show_dish(self):
        '''
        Show the dish
        :return:
        '''
        self.dish_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.dish_tree, 1, 2)
        self.insert_data(self.dish_images, self.dish_tree, '菜品')

        def insert_to_bill(event):
            for item in self.dish_tree.selection():
                item_text = self.dish_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.dish_tree.bind('<ButtonRelease-1>', insert_to_bill)

    def show_staple(self):
        '''
        Show the staple
        :return:
        '''
        self.staple_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.staple_tree, 4, 0)
        self.insert_data(self.staple_images, self.staple_tree, '主食')

        def insert_to_bill(event):
            for item in self.staple_tree.selection():
                item_text = self.staple_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.staple_tree.bind('<ButtonRelease-1>', insert_to_bill)

    def show_soup(self):
        '''
        Show the soup
        :return:
        '''
        self.soup_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.soup_tree, 4, 2)
        self.insert_data(self.soup_images, self.soup_tree, '汤类')

        def insert_to_bill(event):
            for item in self.soup_tree.selection():
                item_text = self.soup_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.soup_tree.bind('<ButtonRelease-1>', insert_to_bill)

    def show_snack(self):
        '''
        Show the snack
        :return:
        '''
        self.snack_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.snack_tree, 1, 4)
        self.insert_data(self.snack_images, self.snack_tree, '小吃')

        def insert_to_bill(event):
            for item in self.snack_tree.selection():
                item_text = self.snack_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.snack_tree.bind('<ButtonRelease-1>', insert_to_bill)

    def show_dessert(self):
        '''
        Show the dessert
        :return:
        '''
        self.dessert_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.dessert_tree, 4, 4)
        self.insert_data(self.dessert_images, self.dessert_tree, '甜品')

        def insert_to_bill(event):
            for item in self.dessert_tree.selection():
                item_text = self.dessert_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.dessert_tree.bind('<ButtonRelease-1>', insert_to_bill)

    def show_drink(self):
        '''
        Show the drink
        :return:
        '''
        self.drink_tree = Treeview(self.window, columns=UserOrderPage.columns, height=6)
        self.init_treeview(self.drink_tree, 1, 6)
        self.insert_data(self.drink_images, self.drink_tree, '饮品')

        def insert_to_bill(event):
            for item in self.drink_tree.selection():
                item_text = self.drink_tree.item(item, "values")
                print(item_text[0], item_text[1])
                self.bill_tree.insert('', 'end', value=(
                    item_text[0],
                    item_text[1]
                ))
                self.checkout.set(self.checkout.get() + int(item_text[1]))

        self.drink_tree.bind('<ButtonRelease-1>', insert_to_bill)


if __name__ == '__main__':
    window = Tk()
    UserOrderPage(window)
    window.mainloop()
