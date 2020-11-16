import redis

class RedisHelper:
    def __init__(self):
        self.db_users_states = 0
        self.db_messages = 1
        self.db_vk = 3
        self.password = 'QzEcTb123789'

    def SetVKPost(self, vk, post):
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            db.hset(vk, 'Post', post)

    def GetVKPost(self, vk):
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            ret = db.hget(vk, 'Post')
            if (ret):
                return int(ret)
            else:
                self.SetVKPost(vk, 0)
                return 0

    def GetVKID(self, vk):
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            return int(db.hget(vk, 'ID'))

    def GetVKUsers(self, vk):
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            return db.hkeys(vk)

    def SetState(self, user_id, value: int):
        """
        Установить состояние value пользователю по id
        value: int
        """
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            db.hset(user_id, 'state', value)

    def SetQuestBrige(self, user_id, quest_id):
        """
        Записать в бд id вопроса по ключу id пользователя, отвечающего на вопрос
        Запись существует 1 час
        """
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            db.hset(user_id, 'brige', quest_id)

    def SetExpend(self, user_id, group = None, day=None):
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            if not group:
                if not db.hexists(user_id, 'expend_gp'):
                    db.hset(user_id, 'expend_gp', 'КТбо2-6')
                    db.hset(user_id, 'expend_day', 'Сегодня')
            else:
                db.hset(user_id, 'expend_gp', group)
            if(day):
                db.hset(user_id, 'expend_day', day)

    def GetState(self, user_id):
        """
        Проверить состояние пользователя по id
        Возвращает целое число
        Если пользователя нет в бд, то None
        """
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            ret = db.hget(user_id, 'state')
            if ret:
                return int(ret)
            else:
                return 0

    def GetMessage(self, value: str):
        """
        Взять из бд текст сообщения
        value: str
        """
        with redis.Redis(password=self.password, db=self.db_messages) as db:
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
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            quest = db.hget(user_id, 'brige')
            if quest:
                db.hdel(user_id, 'brige')
                return int(quest)
            else:
                return None

    def GetExpend(self, user_id):
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            res = [None, None]
            tmp = db.hget(user_id, 'expend_gp')
            if(tmp):
                res[0] = tmp.decode("utf-8")
            else:
                res[0] = 'КТбо2-6'
                db.hset(user_id, 'expend_gp', res[0])
            tmp = db.hget(user_id, 'expend_day')
            if(tmp):
                res[1] = tmp.decode("utf-8")
            else:
                res[1] = 'Сегодня'
                db.hset(user_id, 'expend_gp', res[1])
            return res

    def ChangeVK(self, user_id, vk):
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            if not db.hexists(vk, user_id):
                db.hset(vk, user_id, 1)
                return
            db.hdel(vk, user_id)

    def CheckUserVK(self, user_id):
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            vk = [0, 0, 0]
            for i in range(1, 4):
                vk[i - 1] = db.hexists("vk" + str(i), user_id)
            return vk

    def DeleteUser(self, user_id):
        # удалить пользователя из бд состояний по id
        with redis.Redis(password=self.password, db=self.db_users_states) as db:
            db.delete(user_id)
        # удаление подписок пользователя
        with redis.Redis(password=self.password, db=self.db_vk) as db:
            for i in db.keys('*'):
                db.hdel(i, user_id)
