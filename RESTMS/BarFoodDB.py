import sqlite3

conn = sqlite3.connect('bar_food.db')


def food_image_address():
    '''
    Get the image address of the food
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
        SELECT image_address
        FROM food
        ORDER BY id
    ''')
    images = []
    for row in cursor:
        images.append(row[0])
    return images


def display_name_use_id(id):
    '''
    Get the name of the food
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
        SELECT id, name
        FROM food
        ORDER BY id
    ''')
    for row in cursor:
        if row[0] == id:
            return row[1]


def display_price_use_id(id):
    '''
    Get the price of the food
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
        SELECT id, price
        FROM food
        ORDER BY id
    ''')
    for row in cursor:
        if row[0] == id:
            return row[1]


def display_category_use_id(id):
    '''
    Get the category of the food
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
        SELECT id, category
        FROM food
        ORDER BY id
    ''')
    for row in cursor:
        if row[0] == id:
            return row[1]


def name_is_exist(name):
    '''
    Check if the name is exist
    :param name:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
        SELECT name
        FROM food
    ''')
    for row in cursor:
        if row[0] == name:
            return True
    return False


def add_food(info:dict):
    '''
    Add a new food to the database
    :param info:
    :return:
    '''
    c = conn.cursor()

    c.execute('''
        INSERT INTO food (name, price, category, image_address) 
        VALUES (?, ?, ?, ?)
        ''', (info['name'], info['price'], info['category'], info['image_address']))

    conn.commit()


def all_info(name):
    '''
    Get all the information of the food
    :param name:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id, name, price, category, image_address FROM food")
    for row in cursor:
        if row[1] == name:
            info = {'id': row[0],
                    'name': row[1],
                    'price': row[2],
                    'category': row[3],
                    'image_address': row[4]}
            return info


def update_all_data(updated_info):
    '''
    Update the information of the food
    :param updated_info:
    :return:
    '''
    c = conn.cursor()

    c.execute("UPDATE food SET name = ? WHERE id = ?", (updated_info['name'], updated_info['id']))

    c.execute("UPDATE food SET price = ? WHERE id = ?", (updated_info['price'], updated_info['id']))

    c.execute("UPDATE food SET category = ? WHERE id = ?", (updated_info['category'], updated_info['id']))

    c.execute("UPDATE food SET image_address = ? WHERE id = ?", (updated_info['image_address'], updated_info['id']))

    conn.commit()


def display_id_use_name(food_name):
    '''
    Get the id of the food
    :param food_name:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id, name FROM food")
    for row in cursor:
        if row[1] == food_name:
            return row[0]


def delete_one_row(food_id):
    '''
    Delete an employee from the database
    :param food_id:
    :return:
    '''
    c = conn.cursor()

    last_id = get_last_id()
    print(last_id)
    c.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'food' AND seq = ? AND rowid = 2",
              (last_id - 2, last_id))

    c.execute("DELETE FROM food WHERE id = ?", (food_id,))

    conn.commit()


def id_is_exist(id):
    '''
    Check if the id is exist
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id FROM food")
    for row in cursor:
        if row[0] == id:
            return True
    return False


def get_last_id():
    '''
    Get the last id of the food
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id FROM food ORDER BY id")
    for row in cursor:
        last_id = row[0]
    # print(last_id)
    return last_id


def get_category_use_id(id):
    '''
    Get the category of the food
    :param id:
    :return:
    '''
    if id == 0:
        return ''
    else:
        c = conn.cursor()
        cursor = c.execute("SELECT id, category FROM food ORDER BY id")
        for row in cursor:
            if row[0] == id:
                return row[1]


def get_img_use_id(id):
    '''
    Get the image address of the food
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id, image_address FROM food ORDER BY id")
    for row in cursor:
        if row[0] == id:
            return row[1]


def all_quick_meal():
    '''
    Get all the quick meal
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT name, price FROM food WHERE category = '' ORDER BY id")