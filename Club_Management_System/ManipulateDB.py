import shutil
import sqlite3
import pandas as pd

conn = sqlite3.connect('clubs_and_members.db')
c = conn.cursor()

def is_user_in_exist(username, password):
    c.execute('SELECT * FROM Login WHERE Username = ? AND Password = ?', (username, password))
    return c.fetchone() is not None

def get_clubs():
    c.execute('SELECT * FROM Clubs')
    return c.fetchall()

def search_club(club_name):
    c.execute('SELECT * FROM Clubs WHERE ClubName = ?', (club_name,))
    club = c.fetchone()
    return club is not None, club

def send_application(name, contact, grade, major, class_, club_to_join):
    c.execute('INSERT INTO Applications (Club, Name, Contact, Grade, Major, Class) '
              'VALUES (?, ?, ?, ?, ?, ?)', (club_to_join, name, contact, grade, major, class_))
    conn.commit()

def name_is_in_club(name, club_name):
    c.execute('SELECT * FROM Members '
              'WHERE Name = ? '
              'AND Club = ?', (name, club_name))
    return c.fetchone() is not None

def is_application_exist(club_name, name, contact, grade, major, class_):
    c.execute('SELECT * FROM Applications '
              'WHERE Club = ? '
              'AND Name = ? '
              'AND Contact = ? '
              'AND Grade = ? '
              'AND Major = ? '
              'AND Class = ?', (club_name, name, contact, grade, major, class_))
    return c.fetchone() is not None

def get_club_by_usr_and_pwd(username, password):
    name = get_name_by_usr_and_pwd(username, password)
    c.execute('SELECT Club FROM Members WHERE Name = ?', (name,))
    return [club[0] for club in c.fetchall()]

def get_events(club):
    if isinstance(club, list):
        query = 'SELECT * FROM Events WHERE ' + ' OR '.join(['Club = ?' for _ in club])
        c.execute(query, club)
    else:
        c.execute('SELECT * FROM Events WHERE Club = ?', (club,))
    return c.fetchall()

def search_event(event_name):
    c.execute('SELECT * FROM Events WHERE Name = ?', (event_name,))
    event = c.fetchone()
    return event is not None, event

def get_event_ids(club_name):
    query = 'SELECT EventID FROM Events WHERE ' + ' OR '.join(['Club = ?' for _ in club_name])
    c.execute(query, club_name)
    return [id[0] for id in c.fetchall()]

def has_registered(event_id, clubs, name):
    for club in clubs:
        c.execute('SELECT * FROM Registrations WHERE EventID = ? AND Club = ? AND Name = ?', (event_id, club, name))
        if c.fetchone() is not None:
            return True
    return False

def get_name_by_usr_and_pwd(username, password):
    c.execute('SELECT Name FROM Members NATURAL JOIN Login WHERE Username = ? AND Password = ?', (username, password))
    return c.fetchone()[0]

def register_event(event_id, clubs, name):
    print(event_id, clubs, name)
    for club in clubs:
        c.execute('SELECT * '
                  'FROM Registrations '
                  'WHERE Club = ? '
                  'AND Name = ? '
                  'AND EventID = ?', (club, name, event_id))
        if c.fetchone() is None:
            academic_info = get_academic_info(name, club)
            c.execute('INSERT INTO Registrations (EventID, Club, Name, Grade, Major, Class) '
                      'VALUES (?, ?, ?, ?, ?, ?)',
                      (event_id, club, name) + academic_info)
            break
    conn.commit()


def get_academic_info(name, club):
    c.execute('SELECT Grade, Major, Class FROM Members WHERE Name = ? AND Club = ?', (name, club))
    return c.fetchone()

def get_fee(name, club):
    grade, major, class_ = get_academic_info(name, club[0])
    c.execute('SELECT FeeToPay '
              'FROM Members '
              'WHERE Name = ? '
              'AND Grade = ? '
              'AND Major = ? '
              'AND Class = ?', (name, grade, major, class_))
    return sum([fee[0] for fee in c.fetchall()])

def pay_fee(name, club):
    grade, major, class_ = get_academic_info(name, club[0])
    c.execute("UPDATE Members "
              "SET FeeToPay = 0 "
              "WHERE Name = ? "
              "AND Grade = ? "
              "AND Major = ? "
              "AND Class = ?", (name, grade, major, class_))
    conn.commit()

def get_my_events(name):
    query = "SELECT Events.EventID, Events.Club, Events.Name, Description, Venue, Date, Contact " \
            "FROM Registrations, Events " \
            "WHERE Events.EventID = Registrations.EventID " \
            "AND Registrations.Name = ?"
    c.execute(query, (name,))
    return c.fetchall()

def is_my_event_exist(event_id, name):
    c.execute('SELECT * FROM Registrations WHERE EventID = ? AND Name = ?', (event_id, name))
    return c.fetchone() is not None

def get_event_date(event_id):
    c.execute('SELECT Date FROM Events WHERE EventID = ?', (event_id,))
    return c.fetchone()[0]

def check_in(name, event_id):
    query = "DELETE FROM Registrations WHERE EventID = ? AND Name = ?"
    c.execute(query, (event_id, name))
    conn.commit()

def clean_expired_events():
    c.execute("DELETE FROM Events WHERE Date < strftime('%Y-%m-%d', 'now')")
    c.execute("DELETE FROM Registrations WHERE EventID NOT IN (SELECT EventID FROM Events)")
    conn.commit()

def get_dominant_club(name, role):
    c.execute('SELECT Club FROM Members WHERE Name = ? AND Role = ?', (name, role))
    return c.fetchone()[0]

def get_club_info(club_name):
    c.execute('SELECT Type, Principal, College, Advisor, Contact, Description FROM Clubs WHERE ClubName = ?', (club_name,))
    return c.fetchone()

def update_club_info(new_info:dict, club):
    for key, value in new_info.items():
        if value != '':
            c.execute('UPDATE Clubs SET ' + key + ' = ? WHERE ClubName = ?', (value, club))
    conn.commit()

def publish_event(new_event:dict, club):
    c.execute('INSERT INTO Events (Club, Name, Description, Venue, Date, Contact) '
              'VALUES (?, ?, ?, ?, ?, ?)', (club, new_event["EventName"], new_event["Description"], new_event["Venue"], new_event["Date"], new_event["Contact"]))
    conn.commit()

def get_members_by_club(club):
    c.execute('SELECT MemberID, Name, Contact, Role, Grade, Major, Class, FeeToPay FROM Members WHERE Club = ?', (club,))
    return c.fetchall()

def update_member_info(new_info:dict, id):
    for key, value in new_info.items():
        c.execute('UPDATE Members SET ' + key + ' = ? WHERE MemberID = ?', (value, id))
    conn.commit()

def get_user_and_pwd(id):
    c.execute('SELECT Username, Password FROM Login WHERE MemberID = ?', (id,))
    return c.fetchone()

def delete_member(id):
    c.execute('DELETE FROM Members WHERE MemberID = ?', (id,))
    conn.commit()

def get_applications(club):
    c.execute('SELECT Name, Contact, Grade, Major, Class, Username, Password '
              'FROM Applications '
              'WHERE Club = ?', (club,))
    return c.fetchall()

def add_member(info, club):
    # print(info[:5])
    c.execute('INSERT INTO Members (Name, Contact, Grade, Major, Class, Club, Role) '
              'VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(info[:5]) + (club,) + ('社员',))
    c.execute('Insert INTO Login (Username, Password) '
                'VALUES (?, ?)', (info[5], info[6]))
    conn.commit()

def delete_application(info, club):
    print(info)
    c.execute('DELETE FROM Applications '
              'WHERE Club = ? '
              'AND Name = ? '
              'AND Contact = ? '
              'AND Grade = ? '
              'AND Major = ? '
              'AND Class = ?', (club, ) + tuple(info[:5]))
    conn.commit()

def update_event_info(new_info:dict):
    for key, value in new_info.items():
        c.execute('UPDATE Events SET ' + key + ' = ? WHERE EventID = ?', (value, new_info['EventId']))
    conn.commit()

def delete_event(event_id):
    c.execute('DELETE FROM Events WHERE EventID = ?', (event_id,))
    conn.commit()

def get_approvals():
    c.execute('SELECT * FROM Approvals')
    return c.fetchall()

def approve_club(info):
    c.execute('INSERT INTO Clubs (ClubName, Type, Principal, College, Advisor, Contact, Description) '
              'VALUES (?, ?, ?, ?, ?, ?, ?)', info[1:8])
    c.execute('INSERT INTO Login (Username, Password) VALUES (?, ?)', (info[8], info[9]))
    c.execute('INSERT INTO Members (Name, Contact, Club, Role) VALUES (?, ?, ?, ?)', (info[3], info[6], info[1], '社长'))
    c.execute('DELETE FROM Approvals WHERE ApprovalID = ?', (info[0],))
    conn.commit()

def reject_club(info):
    c.execute('DELETE FROM Approvals WHERE ApprovalID = ?', (info[0],))
    conn.commit()

def export_club_info(folder_path):
    df = pd.read_sql_query('SELECT * FROM Clubs', conn)
    df.to_excel(folder_path + '/club_info.xlsx', index=False)

def export_member_info(folder_path):
    df = pd.read_sql_query('SELECT * FROM Members', conn)
    df.to_excel(folder_path + '/member_info.xlsx', index=False)

def backup_db(folder_path):
    shutil.copy('clubs_and_members.db', folder_path + '/clubs_and_members_backup.db')

def restore_db(file_path):
    shutil.copy(file_path, 'clubs_and_members.db')

def get_club_size():
    clubs = pd.read_sql_query('SELECT * FROM Members', conn)
    clubs_count = clubs.groupby('Club')[['Club']].count()
    clubs_count.rename(columns={'Club':'Count'}, inplace=True)
    clubs_sorted = clubs_count.sort_values(by='Count', ascending=True)
    return clubs_sorted

def get_club_college_and_type():
    clubs = pd.read_sql_query('SELECT * FROM Clubs', conn)
    clubs = clubs.groupby(['College', 'Type'])[['College']].count()
    clubs.rename(columns={'College':'Count'}, inplace=True)
    clubs = clubs.reset_index()
    return clubs

def get_club_college():
    clubs = pd.read_sql_query('SELECT * FROM Clubs', conn)
    clubs = clubs.groupby('College')[['College']].count()
    clubs.rename(columns={'College':'Count'}, inplace=True)
    return clubs

def get_grade_distribution():
    members = pd.read_sql_query('SELECT * FROM Members', conn)
    members = members.groupby('Grade')[['Grade']].count()
    members.rename(columns={'Grade':'Count'}, inplace=True)
    return members

def get_role_by_usr_and_pwd(username, password):
    c.execute('SELECT Role FROM Members NATURAL JOIN Login WHERE Username = ? AND Password = ?', (username, password))
    return c.fetchone()[0]

def add_approval(info:dict):
    # print(info.values())
    c.execute('INSERT INTO Approvals (ClubName, Type, Principal, College, Advisor, Contact, Description, Username, Password) '
              'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(info.values()))
    conn.commit()

def publish_fee(club, fee):
    c.execute('UPDATE Members SET FeeToPay = ? WHERE Club = ?', (fee, club))
    conn.commit()

def add_user(info:dict):
    c.execute('INSERT INTO Applications (Club, Name, Contact, Grade, Major, Class, Username, Password) '
              'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (info['Club'],
               info['Name'],
               info['Contact'],
               info['Grade'],
               info['Major'],
               info['Class'],
               info['Username'],
               info['Password']))
    conn.commit()

def get_club_list():
    c.execute('SELECT DISTINCT ClubName FROM Clubs')
    return c.fetchall()

def is_club_exist(club_name):
    c.execute('SELECT * FROM Clubs WHERE ClubName = ?', (club_name,))
    return c.fetchone() is not None

if __name__ == '__main__':
    a = 1