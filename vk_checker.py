import requests
import datetime
import re

import eventlet
from redis import Redis

from config import bot
from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import RedisHelper

# вариативная строка vk api
URL_API_VK = "https://api.vk.com/method/wall.get?owner_id=-{}&count=2"\
    "&extended=true&access_token=acccb6937601b1d05b2ed6e7b6c15ea3f3d1f37813008e8d83ca42a91ce2022a1e04e503499e970e01d9c&v=5.84"

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
def check_new_posts(VK):
    db = RedisHelper()
    DATA = get_data(URL_API_VK.format(db.GetVKID(VK)))
    for item in DATA['response']['items']:
        try:
            item['copy_history']
        except KeyError:
            if item['id'] > db.GetVKPost(VK):
                db.SetVKPost(VK, item['id'])

                users = db.GetVKUsers(VK)[3:]
                #print(users)

                text=''
                for line in item['text'].split('\n', maxsplit = 4)[:4]:
                    line = re.sub(r'\[\w+\|', '', line)
                    line = re.sub(r'\]\s', '', line)

                    text+=line + '\n'
                text += '<b>...</b>'

                for user in users:
                    user = int(user)
                    bot.send_message(chat_id=user,
                                    text= 'Обновление в группе "<a href="{}"><b>{}</b></a>".\n{}'.format(
                                            'https://vk.com/{}?w=wall-{}_{}'.format(DATA['response']['groups'][0]['screen_name'],
                                                            DATA['response']['groups'][0]['id'],
                                                            item['id']),
                                            DATA['response']['groups'][0]['name'],
                                            text),
                                    parse_mode='HTML')
                return

if __name__ == "__main__":
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S") ,'START')
    check_new_posts('vk1')
    check_new_posts('vk2')
    check_new_posts('vk3')
    print('DONE')
