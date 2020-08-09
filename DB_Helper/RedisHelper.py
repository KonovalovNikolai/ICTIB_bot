import redis

def get_current_state(user_id):
    with redis.Redis() as db:
        return int(db.get(user_id))

def set_state(user_id, value):
    with redis.Redis() as db:
        db.set(user_id, value)

def delet_user(user_id):
    with redis.Redis() as db:
        db.delete(user_id)
        
def get_message(value):
    with redis.Redis(db=1) as db:
        return db.get(value).decode('utf-8')

def brige_to_quest(user_id, quest_id):
    with redis.Redis(db = 2) as db:
        db.set(user_id, quest_id)
        db.expire(user_id, 3600)

def get_quest_id(user_id):
    with redis.Redis(db = 2) as db:
        return int(db.get(user_id))
