import sqlite3

database_name = "user_database.db"

class SQLHelper:
    # При создании класса подключаемся к БД
    def __init__(self):
        # Подключаемся к БД
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    # Если пользователь пишет /start
    # Проверить, если пользователь в БД
    # проверяем по id чата
    def IsInBD(self, chat_id):
        sql = "SELECT * FROM user WHERE id=?"  # SQL запрос
        self.cursor.execute(sql, [chat_id])  # проверям записан ли уже пользователь
        if self.cursor.fetchone():
            return True
        return False

    # Добавить нового пользователя в БД
    def AddUser(self, user):
        sql = "INSERT INTO user VALUES (?,?,?,?)"
        self.cursor.execute(sql, user)  # Запись в БД
        self.connection.commit()  # обновление таблицы БД

    # Получить все данные пользователя по id
    def TakeInfo(self, chat_id):
        sql = "SELECT * FROM user WHERE id=?"  # SQL запрос
        self.cursor.execute(sql, [chat_id])
        return self.cursor.fetchone()

    def UpdateAuto(self, chat_id):
        sql = "SELECT auto FROM user WHERE id=?"
        self.cursor.execute(sql, [chat_id])
        
        if self.cursor.fetchone()[0] == 0:
            sql = "UPDATE user SET auto = 1 WHERE id=?"
            self.cursor.execute(sql, [chat_id])
            self.connection.commit()
            return "Авто расписание включено."
        else:
            sql = "UPDATE user SET auto = 0 WHERE id=?"
            self.cursor.execute(sql, [chat_id])
            self.connection.commit()
            return "Авто расписание выключено."

    #выполнить sql запрос
    def Execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def DeleteUser(self, chat_id):
        sql = "DELETE FROM user WHERE id=?"
        self.cursor.execute(sql, [chat_id])
        self.connection.commit()  # обновление таблицы БД

    # Не забудь закрыть БД!
    def close(self):
        # Закрываем текущее соединение с БД
        self.cursor.close()
        self.connection.close()