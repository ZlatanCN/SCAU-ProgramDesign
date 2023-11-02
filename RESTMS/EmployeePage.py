from EmployeeMenuFrame import *


class EmployeePage:
    permission = None

    def __init__(self, window: Tk, permission):
        '''
        Initialize the EmployeePage
        :param window:
        :param permission:
        '''
        EmployeePage.permission = permission
        self.window = window
        self.window.title('员工操作')
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 600) // 2
        self.window.geometry(f"600x600+{x}+{y}")
        self.window.iconphoto(True, PhotoImage(file="Saloon.ico"))

        self.create_menu_bar()

        self.modify_frame = ModifyFrame(self.window, EmployeePage.permission)
        self.add_frame = AddFrame(self.window, EmployeePage.permission)
        self.delete_frame = DeleteFrame(self.window, EmployeePage.permission)
        self.search_frame = SearchFrame(self.window, EmployeePage.permission)

        self.food_search_frame = FoodSearchFrame(self.window)
        self.food_add_frame = FoodAddFrame(self.window)
        self.food_delete_frame = FoodDeleteFrame(self.window)
        self.food_modify_frame = FoodModifyFrame(self.window)

    def create_menu_bar(self):
        '''
        Create a menu bar
        :return:
        '''
        menu = Menu(self.window)

        menu.add_command(label='员工查找', command=self.show_search)
        menu.add_command(label='员工录入', command=self.show_add)
        menu.add_command(label='员工修改', command=self.show_modify)
        menu.add_command(label='员工删除', command=self.show_delete)

        menu.add_command(label='菜单查找', command=self.food_search)
        menu.add_command(label='菜单录入', command=self.food_add)
        menu.add_command(label='菜单修改', command=self.food_modify)
        menu.add_command(label='菜单删除', command=self.food_delete)

        self.window['menu'] = menu

    def show_modify(self):
        '''
        Show the modify frame
        :return:
        '''
        ModifyFrame.pack_forget_other(self)
        self.modify_frame.pack()

    def show_search(self):
        '''
        Show the search frame
        :return:
        '''
        SearchFrame.pack_forget_other(self)
        self.search_frame.pack()

    def show_add(self):
        '''
        Show the add frame
        :return:
        '''
        AddFrame.pack_forget_other(self)
        self.add_frame.pack()

    def show_delete(self):
        '''
        Show the delete frame
        :return:
        '''
        DeleteFrame.pack_forget_other(self)
        self.delete_frame.pack()

    def food_search(self):
        '''
        Show the food search frame
        :return:
        '''
        FoodSearchFrame.food_pack_forget_other(self)
        self.food_search_frame.pack()

    def food_add(self):
        '''
        Show the food add frame
        :return:
        '''
        FoodAddFrame.food_pack_forget_other(self)
        self.food_add_frame.pack()

    def food_modify(self):
        '''
        Show the food modify frame
        :return:
        '''
        FoodModifyFrame.food_pack_forget_other(self)
        self.food_modify_frame.pack()

    def food_delete(self):
        '''
        Show the food delete frame
        :return:
        '''
        FoodDeleteFrame.food_pack_forget_other(self)
        self.food_delete_frame.pack()


if __name__ == '__main__':
    window = Tk()
    EmployeePage(window, EmployeePage.permission)
    window.mainloop()
