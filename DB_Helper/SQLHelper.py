import sqlite3

database_name = "database.db"

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

    #Включить/отключить автораспсиание пользователя
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

    def CheckUserQuest(self, chat_id):
        sql = "SELECT * FROM questions WHERE user_id=?"  # SQL запрос
        self.cursor.execute(sql, [chat_id])  # проверям записан ли уже пользователь
        if self.cursor.fetchone():
            return True
        return False
    
    def AddQuest(self, chat_id, message_id, text):
        sql = "INSERT INTO questions VALUES (?,?,?)"
        self.cursor.execute(sql, [chat_id, message_id, text])
        self.connection.commit()

    def TakeQuest(self, chat_id):
        sql = 'SELECT question_id, message FROM questions WHERE user_id=?'
        self.cursor.execute(sql, [chat_id])
        self.connection.commit()
        quest = self.cursor.fetchone()

        if(quest):
            return 'Вопрос №{}\n{}'.format(*quest)
        else:
            return None

    def DeleteQuest(self, chat_id):
        sql = 'DELETE FROM questions WHERE user_id=?'
        self.cursor.execute(sql, [chat_id])
        self.connection.commit()


    #выполнить sql запрос
    def Execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def DeleteUser(self, chat_id):
        sql1 = 'DELETE FROM user WHERE id=?'
        sql2 = 'DELETE FROM tt_alerts WHERE user_id=?'
        sql3 = 'DELETE FROM questions WHERE user_id=?'
        self.cursor.execute(sql1, [chat_id])
        self.cursor.execute(sql2, [chat_id])
        self.cursor.execute(sql3, [chat_id])
        self.connection.commit()  # обновление таблицы БД

    # Не забудь закрыть БД!
    def close(self):
        # Закрываем текущее соединение с БД
        self.cursor.close()
        self.connection.close()