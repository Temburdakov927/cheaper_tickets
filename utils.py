import shelve

from telebot import types

from SQLighter import SQLighter
from config import shelve_name, database_name

db_dir = "Data_Base"
def count_rows():
    """
    Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.
    Потом из этого количества будем выбирать музыку.
    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(db_dir + shelve_name) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(db_dir + shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, user_answer,db_name = shelve_name):
    """
    Записываем значение в базу данных и запоминаем
    :param chat_id: id юзера, в редких случаях другой ключ
    :param user_answer: ответ пользователя (из телеграма)
    :param db_name: название базы данных
    """
    with shelve.open(db_dir +"/"+ db_name) as storage:
        storage[str(chat_id)] = user_answer


def finish_user_game(chat_id,db_name = shelve_name):
    """
    Заканчиваем сессию и обнуляем прогресс(не реализованно)
    :param chat_id: id юзера
    :param db_name: название базы данных
    """
    with shelve.open(db_dir + shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id, db_name=shelve_name):
    """
    Получаем значение базы данных(ответ) для текущего юзера
    :param chat_id: id юзера
    :param db_name: название базы данных
    :return: (str) Правильный ответ / None
    """
    with shelve.open(db_dir +"/"+ db_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def generate_markup(list_items):
    """
    Создаем кастомную клавиатуру для выбора ответа,
    :list_items Набор городов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup





