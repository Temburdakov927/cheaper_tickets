from vedis import Vedis
import config


# Запрашиваем из базы статус пользователя
def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError:
             #Если такого ключа/пользователя в базе не оказалось
            return config.States.S_START.value  #Значение по умолчанию-начало диалога

# Сохраняем текущий статус пользователя в базу
def set_state(user_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[str(user_id)] = value
            return True
        except:
            print('Проблемка с юзером!')
            # тут желательно как-то обработать ситуацию
            return False
