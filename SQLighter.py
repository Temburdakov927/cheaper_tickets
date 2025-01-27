import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM Users').fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM Users WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM Users').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

    def update(self,type_answer, answer,rownum):
        with self.connection:
            self.cursor.execute(f'UPDATE Users set {type_answer} = ? WHERE id = ?', (answer,rownum))
            self.connection.commit()



