import redis

PASS = 'QzEcTb123789'
#Модуль для работы с Redis
#db = 0 - состояния пользователь
#db = 1 - текст сообщений
#db = 2 - переход для отправки ответа

def get_current_state(user_id):
    '''
    Проверить состояние пользователя по id
    Возвращает целое число
    Если пользователя нет в бд, то None
    '''
    with redis.Redis(password= PASS) as db:
        ret = db.get(user_id)
        if (ret):
            return int(ret)
        else:
            return 0

def set_state(user_id, value: int):
    '''
    Установить состояние value пользователю по id
    value: int
    '''
    with redis.Redis(password= PASS) as db:
        db.set(user_id, value)

def delet_user(user_id):
    '''
    Удалить пользователя из бд состояний по id
    '''
    with redis.Redis(password= PASS) as db:
        db.delete(user_id)
    with redis.Redis(db = 2, password= PASS) as db:
        db.delete(user_id)
        
def get_message(value: str):
    '''
    Взять из бд текст сообщения
    value: str
    '''
    with redis.Redis(db=1, password= PASS) as db:
        ret = db.get(value)
        if ret:
            return ret.decode('utf-8')
        else:
            return 'ERROR: Не удалось получить текст сообщения'

def brige_to_quest(user_id, quest_id):
    '''
    Записать в бд id вопроса по ключу id пользователя, отвечабщего на вопрос
    Запись существует 1 час
    '''
    with redis.Redis(db = 2, password= PASS) as db:
        db.set(user_id, quest_id)
        db.expire(user_id, 3600)

def get_quest_id(user_id):
    '''
    Взять id вопроса по id пользователя
    Удаляет запись
    '''
    with redis.Redis(db = 2, password= PASS) as db:
        quest = db.get(user_id)
        if quest:
            db.delete(user_id)
            return int(quest)
        else:
            return None
