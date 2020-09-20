import redis


# Модуль для работы с Redis
# db = 0 - состояния пользователь
# db = 1 - текст сообщений
# db = 2 - переход для отправки ответа
class RedisHelper:
    def __init__(self):
        self.db_users_states = 0
        self.db_messages = 1
        self.db_quests = 2
        self.db_vk = 3
        self.password = None

    def SetState(self, user_id, value: int):
        """
        Установить состояние value пользователю по id
        value: int
        """
        with redis.Redis(db=self.db_users_states) as db:
            db.set(user_id, value)

    def SetQuestBrige(self, user_id, quest_id):
        """
        Записать в бд id вопроса по ключу id пользователя, отвечающего на вопрос
        Запись существует 1 час
        """
        with redis.Redis(db=self.db_quests) as db:
            db.set(user_id, quest_id)
            db.expire(user_id, 3600)

    def GetState(self, user_id):
        """
        Проверить состояние пользователя по id
        Возвращает целое число
        Если пользователя нет в бд, то None
        """
        with redis.Redis(db=self.db_users_states) as db:
            ret = db.get(user_id)
            if ret:
                return int(ret)
            else:
                return 0

    def GetMessage(self, value: str):
        """
        Взять из бд текст сообщения
        value: str
        """
        with redis.Redis(db=self.db_messages) as db:
            ret = db.get(value)
            if ret:
                return ret.decode("utf-8")
            else:
                return "ERROR: Не удалось получить текст сообщения"

    def GetQuestBrige(self, user_id):
        """
        Взять id вопроса по id пользователя
        Удаляет запись
        """
        with redis.Redis(db=self.db_quests) as db:
            quest = db.get(user_id)
            if quest:
                db.delete(user_id)
                return int(quest)
            else:
                return None

    def ChangeVK(self, user_id, vk):
        with redis.Redis(db=self.db_vk) as db:
            if not db.hexists(vk, user_id):
                db.hset(vk, user_id, 1)
                return
            db.hdel(vk, user_id)

    def CheckUserVK(self, user_id):
        with redis.Redis(db=self.db_vk) as db:
            vk = [0, 0, 0]
            for i in range(1, 4):
                vk[i - 1] = db.hexists("vk" + str(i), user_id)
            return vk

    def DeleteUser(self, user_id):
        """
        Удалить пользователя из бд состояний по id
        """
        with redis.Redis(db=self.db_users_states) as db:
            db.delete(user_id)
        with redis.Redis(db=self.db_quests) as db:
            db.delete(user_id)
        with redis.Redis(db=self.db_vk) as db:
            for i in db.keys('*'):
                db.hdel(i, user_id)
