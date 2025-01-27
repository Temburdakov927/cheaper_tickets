import json
from datetime import datetime
from bs4 import BeautifulSoup

import utils
import config
from avia_db import insert_db
from config import months,session,URL

broken_data = {'data': {}, 'currency': 'rub', 'success': True}
fly_to = []
local_true_city = [key for key in config.decode_iso_city.keys()]
#alternativ_city =['SGC', 'SUZ', 'SCW', 'IKS', 'TOF', 'TVE', 'TJM', 'UFA', 'UCT', 'UUD', 'ULY', 'USK', 'UIK', 'OGZ', 'VVO', 'VLK', 'VOG', 'VGD', 'VKT', 'VOZ', 'YKS', 'UUS', 'DXB', 'PKV']


def update_db_id():
    current_id = utils.get_answer_for_user("Update_id", config.update_id_status)
    if current_id:
        utils.set_user_game("Update_id", current_id + 1, config.update_id_status)
    else:
        utils.set_user_game("Update_id", 1, config.update_id_status)
        current_id = utils.get_answer_for_user("Update_id", config.update_id_status)
    return current_id



def unique_city_month(current_city,travel_month,city_travel=''):
    date = f'2025-{months[travel_month]}'
    your_token_aviaseils = None #Вставь сюда свой токе из авиасейлс
    request = session.get(URL + f'?departure_date={date}&origin={current_city}&destination={city_travel}&calendar_type=departure_date&token={your_token_aviaseils}')
    soup = BeautifulSoup(request.text, 'html.parser')
    data = json.loads(str(soup))
    if data['success']:
        try:
            if len(data) > 0:
                call_aviaseils(data,date,current_city)
        except TypeError:
            print('No data in unique_city_month')
    else:
        local_true_city.remove(current_city)
    list_city = list(set([fly[0] for fly in fly_to]))
    return list_city


def best_price_year():
    for month in months:
        if int(datetime.now().month) <= int(months[month]):
            for current_city in local_true_city:
                unique_city_month(current_city,month,city_travel='')


def call_aviaseils(data, date, current_city):
    try:
        for day_arrive in data['data']:
            city = data['data'][f'{day_arrive}']['destination']
            if city != "":
                day_leave = data['data'][f'{day_arrive}']['departure_at']
                day_arrive2 = data['data'][f'{day_arrive}']['return_at']
                price_tick = data['data'][f'{day_arrive}']['price']
                city_travel = data['data'][f'{day_arrive}']['destination']
                days_travelled = calculate_count_days(day_leave,day_arrive2)
                current_id = update_db_id()
                insert_db(current_city, city_travel, date, day_leave, day_arrive2, days_travelled,price_tick,current_id)
    except TypeError:
        print('No data')


def calculate_count_days(day_leave, day_arrive):
    month_31 = ["01","03","05","07","08","10","12"]
    feb = "02"
    if day_leave[5:7] == day_arrive[5:7]:
        days_travelled = int(day_arrive[8:10]) - int(day_leave[8:10])+1
    elif day_leave[5:7] in month_31:
        days_travelled = int(day_arrive[8:10]) - int(day_leave[8:10]) + 32
    elif day_leave[5:7] == feb:
        days_travelled = int(day_arrive[8:10]) - int(day_leave[8:10]) + 29
    else:
        days_travelled = int(day_arrive[8:10]) - int(day_leave[8:10]) + 31
    return days_travelled
