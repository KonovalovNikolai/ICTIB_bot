import logging

import eventlet
import requests
import base64
from bs4 import BeautifulSoup

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

URL_GOG_API = "https://www.googleapis.com/customsearch/v1/siterestrict?key=AIzaSyDVqmE1G8CdDMnqJHj5dMZGyQlEV3X3eXo&" \
              "cx=62963ebbd0c56def7&q=(inurl:p_per_id)%20AND%20(intext:{})"

# получение данных
def get_data(url):
    """
    Получение данных из формированного запроса API. Функция принимает url запроса.
    Функция универсальная, работает с VK и Google Custom Search.
    """
    timeout = eventlet.Timeout(10)
    try:
        feed = requests.get(url)
        return feed.json()
    except eventlet.timeout.Timeout:
        return None
    finally:
        timeout.cancel()

def get_lecturer(intext : str = ''):
    try:
        # Исправление запроса
        intext = intext.replace("+", "\+") # при вводе номере
        intext = intext.replace("@", "\@") # при вводе почты
        data = get_data(URL_GOG_API.format(intext))

        # Начало парсинга
        r = requests.get(data['items'][0]['link'])
        soup = BeautifulSoup(r.text, "html.parser")

        # Парсинг ФИО
        about_employee = soup.find('section', {'class': 'about_employee'})
        name = about_employee.find('h2').text.strip()

        # Поиск класса "text" и поиск в нём всех тегов <p>
        text = about_employee.find('div', 'text')
        tags_p = text.find_all('p')

        # Парсинг кафедры и звания
        department = ""
        for item in tags_p:
            try:
                if item.a['href'][0] == '/':
                    department = " ".join(item.text.replace('\n', '').split())
                    break
            except TypeError:
                pass

        # Парсинг номеров телефонов
        phone = text.find('span', 'phones').text
        if len(phone) != 0:
            phone = phone.replace(';', '')
            phone = phone.replace('\n', '')
            phone = phone.replace(' ', '')
            phone = phone.replace('+', ', +').strip()
            phone = phone.replace('д', ' д')
            phone = phone[2:]

        # Парсинг почт
        contacts = text.find("div", "contacts")
        mails = []
        if contacts.script is not None:
            for item in contacts.script.next_siblings:
                item = str(item).replace("\n", "")
                if (first_comma := item.find("'")) != -1:
                    second_comma = item.find("'", first_comma+1)
                    item = item[first_comma+1:second_comma]
                    item = str(base64.b64decode(item))
                    index = item.find('"', 19)
                    mails.append(item[26:index])

        # Формирование ответа
        mails = ", ".join(mails)
        answer = '{}\n{}\nТелефон: {}\nE-mail: {}\n<a href="{}">Источник</a>'.format(name, department, phone, mails, data['items'][0]['link'])
        while answer.find("\n\n") != -1:
            answer = answer.replace("\n\n", "\n")
        return answer
    except KeyError:
        return 'Преподаватель не найден.'

@bot.message_handler(func = lambda message: message.text == B.STAFF and
                    User(message).GetUserState() == S.NORMAL)
def enter_staff(message):
    user = User(message, bot)
    user.SendMessage(text='Введите сообщение для поиска персонала.\nУкажите в нём ФИО, почту или номер.',
                    raw=False,
                    state=S.SEARCH_STAFF)

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.SEARCH_STAFF)
def search_staff(message):
    user = User(message, bot)
    user.SendMessage(text = get_lecturer(message.text),
                    raw=False,
                    parse_mode='HTML')
    user.BackToMain()
