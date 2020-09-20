import arrow
import json
import datetime
import requests

from config import bot
from DB_Helper.SQLHelper import SQLHelper

url = 'http://165.22.28.187/schedule-api/' #Основа для запросов

lesson = {
    1 : 'с 08:00 до 09:35',
    2 : 'с 09:50 до 11:25',
    3 : 'с 11:55 до 13:30',
    4 : 'с 13:45 до 15:20',
    5 : 'с 15:50 до 17:25',
    6 : 'с 17:40 до 19:15',
    7 : 'с 19:30 до 21:05'
}

def GetTimetable(name, day=None, weekday=None):
    """
    Парсинг расписания.
    Обращаемся к ictis.online по группе, получаем json ответ
    Если ответ содержит поле "result", то расписания для такой группы нет
        (группы впринципе нет)
    Проверяем соответствующие дни недели на совпадение дат
    Если в текущей недели нет данного дня, то проверяем следующую неделю
    name - группа пользователя
    day - номер дня недели, начиная с нуля (понедельник)
    """
    #Обратиться к серверу для получения расписания
    try:
        response = requests.get(url + '?query=' + name)
    except:
        #Если не получилось обратиться к серверу, то он не доступен
        return None

    timetable = json.loads(response.text) #загружаем ответ в типы Python
    if 'choices' in timetable:
        response = requests.get(url + '?query=' + timetable['choices'][0]['name'])
        timetable = json.loads(response.text) #загружаем ответ в типы Python

    #Проверка не пустое ли расписание
    if 'result' in timetable:
        return None

    #date = arrow.get(datetime.datetime(2020, 2, 12), 'US/Pacific').shift(weekday = day, hours = 3)
    if(day):
        date = arrow.utcnow().shift(days = day, hours = 3) #Дата занятий
    else:
        date = arrow.utcnow().shift(weekday = weekday, hours = 3) #Дата занятий

    day = date.weekday()

    if(day == 6):
        return 'None'


    flag = False
    #Проверяем совпадение дат
    table = timetable['table']['table'][day + 2]
    number = table[0]
    if(date.format("D  MMMM", locale="ru") in number):
        #Даты совпали
        flag = True

    #Если даты не совпали, то проверяем следующую неделю
    if(not flag):
        #Проверяем, есть ли на следующую неделю расписание
        week = timetable['table']['week'] + 1
        #Если есть, то делаем новый запрос
        if(week in timetable['weeks']):
            response = requests.get(url + '?group=' + timetable['table']['group'] + "&week=" + str(week)) #запрос
            timetable = json.loads(response.text) #переводим

            #Проверка дат
            table = timetable['table']['table'][day + 2]
            number = table[0]
            if(date.format("D  MMMM", locale="ru") in number):
                #Даты совпали
                flag = True
        else:
            #Нет расписания на следующую неделю
            return None

    #Если даты совпали, то парсим расписание
    if(flag):
        text = ''
        j = 1
        for i in range(1, 8):
            if table[i] != '':
                text += "{}: {}\n {}\n\n".format(j, table[i], lesson[i])
                j += 1

        if j > 1:
            return 'Расписание на {}.\n\n{}'.format(date.format("D MMMM, dddd", locale = "ru"), text)
        else:
            return None
    else:
        #Если не совпадали, то расписание на этот день нет
        return None

group_base = 'КТ{}{}{}-{}'
group_type1 = ['б', 'с', 'м', 'а']
group_type2 = ['о', 'з']

db_worker = SQLHelper()

for i in group_type1:
    for j in group_type2:
        for x in range(1, 6):
            for z in range(1, 13):
                group = group_base.format(i, j, x, z)
                users = db_worker.Execute("SELECT id FROM user WHERE auto = 1 AND gp='" + group + "'")
                if users != []:
                    res = GetTimetable(name = group, day = 0)
                    if res:
                        for user in users:
                            bot.send_message(chat_id = user[0],
                                            text = res)

teachers = db_worker.Execute("SELECT id, gp FROM user WHERE auto = 1 AND type = 'teach'")
for teacher in teachers:
    res = GetTimetable(teacher[1], True)
    if res:
        bot.send_message(chat_id = teacher[0],
                        text = res)
