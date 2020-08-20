import requests
import datetime

import eventlet
from redis import Redis

from config import bot
from DB_Helper.SQLHelper import SQLHelper

PASS = 'QzEcTb123789'

# id групп
ID_G = [48632629, 47535294, 177747188]
# вариативная строка vk api
URL_API_VK = "https://api.vk.com/method/wall.get?owner_id=-{}&count=2" \
    "&extended=true&access_token=95a418be15cb20104dc5ce66b8782ed988c1" \
    "fac44bc56bcb7fe6427a526960da3136b285d20e57be8b14f&v=5.84"

def Get(num):
    with Redis(db=3, password= PASS) as db:
        ret = db.get(num)
        if (ret):
            return int(ret)
        else:
            Set(num, 0)
            return 0

def Set(num, value):
    with Redis(db=3, password= PASS) as db:
        db.set(num, value)

# получение данных
def get_data(URL):
    timeout = eventlet.Timeout(10)
    try:
        feed = requests.get(URL)
        return feed.json()
    except eventlet.timeout.Timeout:
        return None
    finally:
        timeout.cancel()

# проверка на новый пост
# вводим номер группы
def check_new_posts(NUM):
    DATA = get_data(URL_API_VK.format(ID_G[NUM - 1]))
    for item in DATA['response']['items']:
        try:
            item['copy_history']
        except KeyError:
            if item['id'] > Get(NUM):
                Set(NUM, item['id'])

                db = SQLHelper()
                users = db.Execute('SELECT id FROM user WHERE vk{} = 1'.format(NUM))
                db.close()

                text=''
                for line in item['text'].split('\n', maxsplit = 3)[:3]:
                    text+=line + '\n'
                text += '...'
                print(users)
                for user in users:
                    bot.send_message(chat_id=user[0],
                                    text= 'Обновление в группе "<a href="{}">{}</a>".\n{}'.format(
                                            'https://vk.com/{}?w=wall-{}_{}'.format(DATA['response']['groups'][0]['screen_name'],
                                                            DATA['response']['groups'][0]['id'],
                                                            item['id']),
                                            DATA['response']['groups'][0]['name'],
                                            text),
                                    parse_mode='HTML')
                return

if __name__ == "__main__":
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") ,'START')
    check_new_posts(1)
    check_new_posts(2)
    check_new_posts(3)
    print('DONE')
