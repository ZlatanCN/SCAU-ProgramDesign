import sqlite3

conn = sqlite3.connect('employees.db')


def is_employee(name, pwd):
    '''
    Check if the employee is in the database
    :param name:
    :param pwd:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT username, password FROM login_info")
    flag = False
    for row in cursor:
        if row[0] == name and row[1] == pwd:
            flag = True
            break
    return flag


def get_permission(name, pwd):
    '''
    Get the permission of the employee
    :param name:
    :param pwd:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT username, password, permission FROM login_info")
    for row in cursor:
        if row[0] == name and row[1] == pwd:
            return row[2]


def get_permission_use_id(id):
    '''
    Get the permission of the employee
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id, permission FROM login_info")
    for row in cursor:
        if row[0] == id:
            return row[1]


def id_is_exist(self, id):
    '''
    Check if the id is in the database
    :param self:
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute("SELECT id FROM basic_info")
    for row in cursor:
        if row[0] == id:
            return True
    return False


def show_search_data(self):
    '''
    Show the search data
    :param self:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
        SELECT basic.id, basic.name, job, salary, address, phone_number
        FROM basic_info AS basic, job_info AS job
        WHERE basic.id = job.id AND
            basic.name = job.name
        ORDER BY basic.id
    ''')
    for row in cursor:
        self.tree_view.insert('', index='end', value=(
            row[0], row[1], row[2], row[3], row[4], row[5]
        ))


def show_login_info(self):
    '''
    Show the login information
    :param self:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
       SELECT basic.id, basic.name, username, password, permission
       FROM basic_info AS basic, login_info AS login
       WHERE basic.id = login.id
       ORDER BY basic.id
       ''')
    for row in cursor:
        self.tree_view.insert('', index='end', value=(
            row[0], row[1], row[2], row[3], row[4]
        ))


def add_employee(info):
    '''
    Add an employee to the database
    :param info:
    :return:
    '''
    c = conn.cursor()

    c.execute('''
        INSERT INTO basic_info (id, name, address, phone_number) 
        VALUES (?, ?, ?, ?)
        ''', (info['id'], info['name'], info['address'], info['phone_number']))

    c.execute('''
        INSERT INTO login_info (id, username, password, permission) 
        VALUES (?, ?, ?, ?)
        ''', (info['id'], info['username'], info['password'], info['permission']))

    c.execute('''
        INSERT INTO job_info (id, name, job, salary) 
        VALUES (?, ?, ?, ?)
        ''', (info['id'], info['name'], info['job'], info['salary']))

    conn.commit()


def show_all_data(self, id):
    '''
    Show all the data of the employee
    :param self:
    :param id:
    :return:
    '''
    c = conn.cursor()
    cursor = c.execute('''
           SELECT basic.id, basic.name, job, salary, address, phone_number, username, password, permission
           FROM basic_info AS basic, job_info AS job, login_info AS login
           WHERE basic.id = job.id AND
               basic.name = job.name AND 
               basic.id = login.id
           ORDER BY basic.id
       ''')
    for row in cursor:
        if row[0] == id:
            self.tree_view.insert('', index='end', value=(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
            ))
            break


def delete_one_row(employee_to_delete):
    '''
    Delete an employee from the database
    :param employee_to_delete:
    :return:
    '''
    c = conn.cursor()

    c.execute("DELETE FROM basic_info WHERE id = ?", (employee_to_delete,))

    c.execute("DELETE FROM login_info WHERE id = ?", (employee_to_delete,))

    c.execute("DELETE FROM job_info WHERE id = ?", (employee_to_delete,))

    conn.commit()


def all_data_in_dict(self, id):
    '''
    Get all the data of the employee in a dictionary
    :param self:
    :param id:
    :return:
    '''
    info = {}
    c = conn.cursor()
    cursor = c.execute('''
              SELECT basic.id, basic.name, job, salary, address, phone_number, username, password, permission
              FROM basic_info AS basic, job_info AS job, login_info AS login
              WHERE basic.id = job.id AND
                  basic.name = job.name AND 
                  basic.id = login.id
              ORDER BY basic.id
          ''')
    for row in cursor:
        if row[0] == id:
            info['id'] = row[0]
            info['name'] = row[1]
            info['job'] = row[2]
            info['salary'] = row[3]
            info['address'] = row[4]
            info['phone_number'] = row[5]
            info['username'] = row[6]
            info['password'] = row[7]
            info['permission'] = row[8]
            break
    return info


def update_all_data(the_id, updated_info: dict):
    '''
    Update the data of the employee
    :param the_id:
    :param updated_info:
    :return:
    '''
    c = conn.cursor()

    c.execute("UPDATE basic_info SET name = ? WHERE id = ?", (updated_info['name'], the_id))
    c.execute("UPDATE basic_info SET address = ? WHERE id = ?", (updated_info['address'], the_id))
    c.execute("UPDATE basic_info SET phone_number = ? WHERE id = ?", (updated_info['phone_number'], the_id))

    c.execute("UPDATE login_info SET username = ? WHERE id = ?", (updated_info['username'], the_id))
    c.execute("UPDATE login_info SET password = ? WHERE id = ?", (updated_info['password'], the_id))
    c.execute("UPDATE login_info SET permission = ? WHERE id = ?", (updated_info['permission'], the_id))

    c.execute("UPDATE job_info SET name = ? WHERE id = ?", (updated_info['name'], the_id))
    c.execute("UPDATE job_info SET job = ? WHERE id = ?", (updated_info['job'], the_id))
    c.execute("UPDATE job_info SET salary = ? WHERE id = ?", (updated_info['salary'], the_id))

    conn.commit()
