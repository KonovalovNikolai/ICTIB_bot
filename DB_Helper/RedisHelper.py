import redis

def get_current_state(user_id):
    with redis.Redis() as db:
        return db.get(user_id).decode('utf-8')

def set_state(user_id, value):
    with redis.Redis() as db:
        db.set(user_id, value)

def delet_user(user_id):
    with redis.Redis() as db:
        db.delete(user_id)
        
def get_message(value):
    with redis.Redis(db=1) as db:
        return db.get(value).decode('utf-8')
