import sqlite3

from config import database_name, date_create, time_create

# Устанавливаем соединение с базой данных
connection = None
cursor = None


def open():
    global connection, cursor
    connection = sqlite3.connect(database_name, check_same_thread=False)
    cursor = connection.cursor()


def close():
    cursor.close()
    connection.close()

months = []
cities = []
# Создаем таблицу Users

open()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
current_city TEXT NOT NULL,
city TEXT NOT NULL,
month TEXT NOT NULL,
date_leaved text,
date_arrived text,
days_travelled integer,
price INTEGER NOT NULL,
date_create text,
time_create text,
id_updated INTEGER
)''')
close()


def insert_db(current_city,city,month,day_leave,day_arrive,days_travelled,price_tick,id_updated):
    print(type(current_city))
    open()
    cursor.execute('INSERT INTO Users (current_city,city, month, date_leaved,date_arrived,days_travelled,price,date_create,time_create,id_updated) VALUES (?,?,?, ?,?,?,?,?,?,?)',
                   (current_city,city, month, day_leave, day_arrive,days_travelled,price_tick,date_create, time_create,id_updated))
    connection.commit()
    close()

# Выводим нашу базу данных
def print_db():
    open()
    #cursor.execute('DELETE FROM Users')
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for user in users:
        print(user)
    close()




def request_db(choose_city, choose_month,current_city):
    open()
    cursor.execute("SELECT * FROM Users WHERE city=? and month=? and current_city = ?",(choose_city, choose_month,current_city))
    from_db = cursor.fetchall()
    preparing_price,preparing_days = find_needful_time(from_db)
    close()
    return preparing_price,preparing_days

def find_needful_time(users):
    needful_id_db = users[-1][-1]
    needful_date = users[-1][8]
    needful_time = users[-1][9]
    preparing_date = []
    prices = {}
    count_days ={}
    for user in users:
        if user[-1] == needful_id_db:
            date_leave = user[4]
            date_arrive = user[5]
            days_travel = user[6]
            price = user[7]
            travel_dates = date_leave[0:10] + '\t' + date_arrive[0:10]
            prices[travel_dates] = price
            count_days[travel_dates] = days_travel
    return prices,count_days



#в этой функции мы извлекаем нужные данные из готовой базы данных
def data_from_db(query='',*param):  # choose_data):
    open()
    if param:
        cursor.execute(query,param)
    else:
        cursor.execute('''SELECT current_city FROM Users''')
    users = cursor.fetchall()
    needful_data = [town for city in users for town in city if town != 'Нет информации']
    close()
    return list(set(needful_data))

