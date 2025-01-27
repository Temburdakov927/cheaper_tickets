from telebot import types
import config
import telebot

import parsing_city_Russia
from avia_db import print_db, data_from_db
import dbworker
import utils
from SQLighter import SQLighter
from new_attempt import best_price_year

bot = telebot.TeleBot(config.token)

#Предлагает пользователю варианты количества дней в путешествии
def choose_count_days(preparing_days):
    condition_choice = []
    for day in preparing_days:
        if preparing_days[day] < 3:
            choice = "Количество дней в путешествии от 1 до 3"
        elif 3 < preparing_days[day] < 5:
            choice = "Количество дней в путешествии от 3 до 5"
        elif 5 < preparing_days[day] < 10:
            choice = "Количество дней в путешествии от 5 до 10"
        else:
            choice = "Количество дней в путешествии больше 10"
        condition_choice.append(choice)
    return condition_choice


#Обнуляет текущий прогресс пользователя
@bot.message_handler(commands=['restart'])
def restart(message):
    bot.send_message(message.chat.id, 'Обнуляем ваш текущий процесс')
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, 'Вас обнулили!)')

#Обновляет всю базу данных, для всех отправлений, для всех городов
@bot.message_handler(commands=['update'])
def update_db(message):
    bot.send_message(message.chat.id, 'Обновляем базу данных,подождите,плиз')
    best_price_year()
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, 'Свежие данные уже здесь!)')

#Запуск бота, проверка текущего статуса пользователя
@bot.message_handler(commands=['start'])
def cmd_find(message):
    try:
        state = dbworker.get_current_state(message.chat.id)
    except KeyError:
        state = dbworker.get_current_state(message.chat.id).decode('ASCII')
    """
    Для начала надо проверить, завершен ли предыдущий диалог и какой статус у пользователя. 
   Его мы запрашиваем из базы. Если он не нулевой, то мы продолжаем сценарий с точки остановки и текущего статуса, статусы пока что проверяются не все, надо доработать
    """
    last_message = utils.get_answer_for_user(message.chat.id, config.last_choice_user)
    if state == config.States.S_ENTER_MONTH.value:
        bot.send_message(message.chat.id, "Мы остановились на выборе месяца. Выбери его из списка")

        check_month(last_message)
    elif state == config.States.S_ENTER_CITY.value:
        bot.send_message(message.chat.id, "Мы остановились на выборе города. Выбери его из списка")

        check_month(last_message)
    elif state == config.States.S_SET_PRICE.value:
        bot.send_message(message.chat.id, "Осталось лишь согласовать дату и купить билеты, давай сделаем это вместе!)")

        check_month(last_message)
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        # Подключаемся к БД
        db_worker = SQLighter(config.database_name)
        current_city = utils.get_answer_for_user(message.chat.id, config.choose_current_city_name)
        try:
            #Предлагаем пользователю выбрать предыдущий город отправления, если пользователя нет в нашей бд или он решил сменить город отправления, то он начинает с чистого листа
            markup = utils.generate_markup([f"Да, я полечу из {config.decode_iso_city[current_city]}", "Нет, я выберу другой город"])
            bot.send_message(message.chat.id, f'В последний раз вы вылетали из города {config.decode_iso_city[current_city]}, вы хотите снова полететь из этого города?)))',
                             reply_markup=markup)
            utils.set_user_game(message.chat.id, message, config.last_choice_user)
        except KeyError:
            markup = utils.generate_markup(
                ["Начать!"])
            bot.send_message(message.chat.id,
                             'Ты тут новенький, жми начать,тебе понравится!)',
                             reply_markup=markup)
        db_worker.close()
        dbworker.set_state(message.chat.id, config.States.S_ENTER_LAST_CITY.value)


#Предлагаем пользователю города, из которых он может полететь
@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id).decode(
    'ASCII')) == config.States.S_ENTER_LAST_CITY.value)
def check_current_city(message):
    if message.text == "Нет, я выберу другой город" or  message.text == "Начать!":
        city_now = data_from_db()
        local_feature = {}
        for city in city_now:
            if city in config.decode_iso_city.keys():
                local_feature[config.decode_iso_city[city]] = city
        local_feature = dict(sorted(local_feature.items()))
        markup = utils.generate_markup(local_feature.keys())
        bot.send_message(message.chat.id, 'Выбери город, откуда собираешься полететь:',
                         reply_markup=markup)
        dbworker.set_state(message.chat.id, config.States.S_ENTER_CURRENT_CITY.value)
    else:
        user_choice = utils.get_answer_for_user(message.chat.id, config.choose_current_city_name)
        message.text = config.decode_iso_city[user_choice]
        check_month(message)
        dbworker.set_state(message.chat.id, config.States.S_ENTER_MONTH.value)
    utils.set_user_game(message.chat.id, message, config.last_choice_user)


#Предлагаем пользователю месяца, в которые он может полететь из выбранного им города
@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id).decode(
    'ASCII')) == config.States.S_ENTER_CURRENT_CITY.value)
def check_month(message):
    try:
        message.text = config.decode_city_iso[message.text]
    except KeyError:
        message.text = config.decode_iso_city[message.text]

    utils.set_user_game(message.chat.id, message.text, config.choose_current_city_name)
    months_db = data_from_db("SELECT month FROM Users WHERE current_city = ?",message.text)
    current_months = {}
    months_db = [int(month[5:]) for month in months_db]
    months_db.sort()
    months_db = ["0"+str(month) for month in months_db if month < 10]
    print(months_db)
    for month in months_db:
        if month in config.reverse_months.keys():
            current_months[config.reverse_months[month]] = month
    markup = utils.generate_markup(current_months.keys())
    bot.send_message(message.chat.id, 'Выберите месяц вылета:',
                     reply_markup=markup)
    utils.set_user_game(message.chat.id, message, config.last_choice_user)
    dbworker.set_state(message.chat.id, config.States.S_ENTER_MONTH.value)

#Предлагаем пользователю города, в которые он может полететь из выбранного им города в выбранный им месяц
@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id).decode(
    'ASCII')) == config.States.S_ENTER_MONTH.value)

def check_answer(message):
    try:
        message.text = config.decode_month[message.text]
    except KeyError:
        message.text = config.code_month[message.text]
    utils.set_user_game(message.chat.id, message.text, config.choose_month_name)

    cities_for_users = []
    choose_current_city_name = utils.get_answer_for_user(message.chat.id, config.choose_current_city_name)
    date = f'2025-{config.months[message.text]}'
    cities = data_from_db("SELECT city FROM Users WHERE current_city = ? and month = ?",choose_current_city_name, date)
    for city in cities:
        try:
            cities_for_users.append(config.decode_iso_city[city])
        except KeyError:
            continue
    cities_for_users.sort()
    markup = utils.generate_markup(cities_for_users)
    bot.send_message(message.chat.id, 'Выберите город в который собираетесь полететь:',
                     reply_markup=markup)

    utils.set_user_game(message.chat.id, message, config.last_choice_user)
    dbworker.set_state(message.chat.id, config.States.S_ENTER_CITY.value)

#Предлагаем пользователю выбрать количество дней в путешествии
@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id).decode(
    'ASCII')) == config.States.S_ENTER_CITY.value)

def check_date(message):
    from avia_db import request_db
    try:
        message.text = config.decode_city_iso[message.text]
    except KeyError:
        message.text = config.decode_iso_city[message.text]

    utils.set_user_game(message.chat.id, message.text, config.choose_city_name)
    choose_current_city_name = utils.get_answer_for_user(message.chat.id, config.choose_current_city_name)
    choose_city = utils.get_answer_for_user(message.chat.id, config.choose_city_name)
    choose_month = utils.get_answer_for_user(message.chat.id, config.choose_month_name)
    date = f'2025-{config.months[choose_month]}'
    preparing_price,preparing_days = request_db(choose_city, date,choose_current_city_name)
    utils.set_user_game(message.chat.id, preparing_price, config.preparing_date)

    condition_choice = choose_count_days(preparing_days)
    utils.set_user_game(message.chat.id, condition_choice, config.condition_choice_date)
    condition_choice_unique = list(set(sorted(condition_choice)))
    markup = utils.generate_markup(condition_choice_unique)
    bot.send_message(message.chat.id, 'На сколько дней собираетесь лететь?:',
                     reply_markup=markup)
    utils.set_user_game(message.chat.id, message, config.last_choice_user)
    dbworker.set_state(message.chat.id, config.States.S_ENTER_DAYS.value)
@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id).decode(
    'ASCII')) == config.States.S_ENTER_DAYS.value)

#Предлагаем пользователю выбрать более удобные даты из списка(бывают списки из одного элемента)
def check_days(message):
    condition_choice = utils.get_answer_for_user(message.chat.id, config.condition_choice_date)
    preparing_price = utils.get_answer_for_user(message.chat.id, config.preparing_date)
    days_leave_arrive = [day for day in preparing_price.keys()]
    condition_choice_dict = dict(zip(condition_choice,days_leave_arrive))
    days_leave_arrive_user = [condition_choice_dict[count_days] for count_days in condition_choice_dict if count_days == message.text]
    markup = utils.generate_markup(days_leave_arrive_user)
    bot.send_message(message.chat.id, f'Дата вылета:\t Дата возвращения:',
                     reply_markup=markup)
    for item in days_leave_arrive_user:
        bot.send_message(message.chat.id, text = item)
    utils.set_user_game(message.chat.id, message, config.last_choice_user)
    dbworker.set_state(message.chat.id, config.States.S_SET_PRICE.value)

#Подгружаем всю информацию из базы данных, полученную от пользователя
@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id).decode(
    'ASCII')) == config.States.S_SET_PRICE.value)
def print_ticket(message):
    answer = message.text
    utils.set_user_game(message.chat.id, answer, config.choose_date)
    preparing_date = utils.get_answer_for_user(message.chat.id, config.preparing_date)
    leave, arrive = answer.split(' ')[0], answer.split(' ')[1]
    price = preparing_date[leave+"\t"+arrive]
    utils.set_user_game(message.chat.id, price, config.current_price_ticket)

    utils.set_user_game(message.chat.id, leave, config.choose_leave_date)
    utils.set_user_game(message.chat.id, arrive, config.choose_arrive_date)
    leave = utils.get_answer_for_user(message.chat.id, config.choose_leave_date)
    arrive = utils.get_answer_for_user(message.chat.id, config.choose_arrive_date)
    choose_city_iso = utils.get_answer_for_user(message.chat.id, config.choose_city_name)
    choose_month = utils.get_answer_for_user(message.chat.id, config.choose_month_name)
    choose_city = config.decode_iso_city[choose_city_iso]
    choose_current_city_name = utils.get_answer_for_user(message.chat.id, config.choose_current_city_name)
    price = utils.get_answer_for_user(message.chat.id, config.current_price_ticket)

    # Уберем клавиатуру с вариантами ответа.
    keyboard_hider = types.ReplyKeyboardRemove()
    leave_url = leave[8:] + leave[5:7]
    arrive_url = arrive[8:] + arrive[5:7]
    #Пробуем подгрузить фото города, в который пользователь летит, если не получается отправляем информацию без фото
    try:
        bot.send_photo(message.chat.id, photo=utils.get_answer_for_user(choose_city,parsing_city_Russia.all_city_photos),caption=f'Если я тебя правильно понял,то ты намылился в город {choose_city} 👻,\n'
                                          f'🗓️🛫прекрасный выбор, напомню дату вылета:\t {leave} 🛫🗓️\n'
                                          f'🗓️🛬Дата возвращения:\t {arrive} 🛬🗓️\n'
                                          f'🤑Ну и то,зачем я был создан,цена: \t {price} 🤑\n'
                                          f'Ссылочка на твой билетик:\n'
                                          f'https://www.aviasales.ru/search/{choose_current_city_name}{leave_url}{choose_city_iso}{arrive_url}1\n'
                                          f'🏃‍➡️🧳 Ты пока покупай билеты, а я побежал собирать чемоданы🏃‍➡️🧳',
                         reply_markup=keyboard_hider)
    except:
        bot.send_message(message.chat.id, f'Если я тебя правильно понял,то ты намылился в город {choose_city} 👻,\n'
                                      f'🗓️🛫прекрасный выбор, напомню дату вылета:\t {leave} 🛫🗓️\n'
                                      f'🗓️🛬Дата возвращения:\t {arrive} 🛬🗓️\n'
                                      f'🤑Ну и то,зачем я был создан,цена: \t {price} 🤑\n'
                                      f'Ссылочка на твой билетик:\n'
                                      f'https://www.aviasales.ru/search/{choose_current_city_name}{leave_url}{choose_city_iso}{arrive_url}1\n'
                                      f'🏃‍➡️🧳 Ты пока покупай билеты, а я побежал собирать чемоданы🏃‍➡️🧳',
                     reply_markup=keyboard_hider)
    utils.set_user_game(message.chat.id, message, config.last_choice_user)
    # Устанавливаем начальный статус для пользователя
    dbworker.set_state(message.chat.id, config.States.S_START.value)




if __name__ == '__main__':
    bot.infinity_polling()