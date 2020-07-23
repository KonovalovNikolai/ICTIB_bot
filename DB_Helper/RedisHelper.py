from Misc.states import States
import redis


def get_current_state(user_id):
    with redis.Redis() as db:
        try:
            return db.get(user_id).decode('utf-8')
        except:  # Если такого ключа почему-то не оказалось
            return States.S_START.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    with redis.Redis() as db:
        try:
            db.set(user_id, value)
            return True
        except:
            # тут желательно как-то обработать ситуацию
            return False

def delet_user(user_id):
    with redis.Redis() as db:
        try:
            db.delete(user_id)
            return True
        except:
            return False
        
def get_message(value):
    with redis.Redis(db=1) as db:
        try:
            return db.get(value).decode('utf-8')
        except:
            return 0