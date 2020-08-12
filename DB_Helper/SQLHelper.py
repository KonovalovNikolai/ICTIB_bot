import sqlite3

#Модуль для работы с SQLite

DATABASE_NAME = "database.db"

class SQLHelper:
    def __init__(self):
        '''
        Инициализация класса.
        Создаётся подключение к бд и курсор для исполнения запросов.
        '''
        self.connection = sqlite3.connect(database = DATABASE_NAME, timeout= 5)
        self.cursor = self.connection.cursor()

    def IsInBD(self, chat_id):
        '''
        Проверка записи пользователя в бд по id.
        Если пользователь записан, то True,
        Иначе False
        '''
        sql = "SELECT * FROM user WHERE id=?"
        self.cursor.execute(sql, [chat_id])
        if self.cursor.fetchone():
            return True
        return False

    def AddUser(self, user):
        '''
        Добавление пользователя в бд.
        user  - параметры пользователя.
        user = [chat_id, type, group, auto]
        '''
        sql = "INSERT INTO user VALUES (?,?,?,?)"
        self.cursor.execute(sql, user)  # Запись в БД
        self.connection.commit()  # обновление таблицы БД

    def TakeInfo(self, chat_id):
        '''
        Взять все данные пользователя по id.
        Возвращает массив данных пользователя.
        '''
        sql = "SELECT * FROM user WHERE id=?"  # SQL запрос
        self.cursor.execute(sql, [chat_id])
        return self.cursor.fetchone()

    def UpdateAuto(self, chat_id):
        '''
        Изменить параметр "auto" пользователя по id.
        Возвращает True, если параметр был включён,
        False - если выключен.
        '''
        sql = "SELECT auto FROM user WHERE id=?"
        self.cursor.execute(sql, [chat_id])
        
        if self.cursor.fetchone()[0] == 0:
            sql = "UPDATE user SET auto = 1 WHERE id=?"
            self.cursor.execute(sql, [chat_id])
            self.connection.commit()
            return True
        else:
            sql = "UPDATE user SET auto = 0 WHERE id=?"
            self.cursor.execute(sql, [chat_id])
            self.connection.commit()
            return False 
    def AddQuest(self, chat_id, message_id, text):
        '''
        Записать вопрос пользователя в бд.\n
        chat_id - id пользователя;\n
        message_id - id сообщения;\n
        text - текст вопроса.
        '''
        sql = "INSERT INTO questions VALUES (?,?,?)"
        self.cursor.execute(sql, [chat_id, message_id, text])
        self.connection.commit()

    def TakeQuest(self, chat_id):
        '''
        Взять вопрос по id пользователя.
        Возвращает все поля записи.
        '''
        sql = 'SELECT * FROM questions WHERE user_id=?'
        self.cursor.execute(sql, [chat_id])

        return self.cursor.fetchone()
    
    def TakeQuestWithId(self, message_id):
        '''
        Взять вопрос по id сообщения.
        Возвращает все поля записи.
        '''
        sql = 'SELECT * FROM questions WHERE question_id=?'
        self.cursor.execute(sql, [message_id])

        return self.cursor.fetchone()

    def TakeFirsQuest(self):
        '''
        Взять первый в бд вопрос.
        Возвращает все поля записи.
        '''
        sql = 'SELECT question_id, message FROM questions ORDER BY ROWID ASC LIMIT 1'
        self.cursor.execute(sql)

        return self.cursor.fetchone()
    
    def TakeRandomQuest(self):
        '''
        Взять случайный вопрос.
        Возвращает все поля записи.
        '''
        sql = 'SELECT question_id, message FROM questions ORDER BY random() LIMIT 1'
        self.cursor.execute(sql)

        return self.cursor.fetchone()

    def DeleteQuest(self, chat_id):
        '''
        Удалить вопрос по id пользователя
        '''
        sql = 'DELETE FROM questions WHERE user_id=?'
        self.cursor.execute(sql, [chat_id])
        self.connection.commit()


    #выполнить sql запрос
    def Execute(self, sql):
        '''
        Выполнить переданный sql запрос.
        (Для тех случаев, когда лень было создавать ещё одну функцию)
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def DeleteUser(self, chat_id):
        '''
        Удалить все записи пользователя по id.
        '''
        sql1 = 'DELETE FROM user WHERE id=?'
        sql2 = 'DELETE FROM tt_alerts WHERE user_id=?'
        sql3 = 'DELETE FROM questions WHERE user_id=?'
        self.cursor.execute(sql1, [chat_id])
        self.cursor.execute(sql2, [chat_id])
        self.cursor.execute(sql3, [chat_id])
        self.connection.commit()  # обновление таблицы БД

    # Не забудь закрыть БД!
    def close(self):
        '''
        Закрыть курсор и соединение с бд.
        '''
        self.cursor.close()
        self.connection.close()