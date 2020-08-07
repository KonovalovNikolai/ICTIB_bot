from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import get_message
from Misc import message as M
import requests
import logging
import arrow
import json
import datetime

logger = logging.getLogger('Bot.TimeTable')

#Словарь номер занятия - время проведения
lesson = {
    1 : 'с 08:00 до 09:35',
    2 : 'с 09:50 до 11:25',
    3 : 'с 11:55 до 13:30',
    4 : 'с 13:45 до 15:20',
    5 : 'с 15:50 до 17:25',
    6 : 'с 17:40 до 19:15',
    7 : 'с 19:30 до 21:05'
}

url = 'http://165.22.28.187/schedule-api/' #Основа для запросов

def GetTodayDate(day):
    """
    Возвращает дату в формате: "Число Название месяца, день недели"
    Например: 26 июля, воскресенье
    day - номер дня недели, начиная с нуля (понедельник)  
    """
    return arrow.utcnow().shift(days = day, hours = 3).format("D MMMM, dddd", locale = "ru")

def GetTimetable(name, day):
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
        logger.error("Failed to connect to resource: %s" % name)
        return get_message(M.TIMETABLE_NOCONECTION) #Сообщение о неудачном подключении

    timetable = json.loads(response.text) #загружаем ответ в типы Python
    
    #Проверка не пустое ли расписание
    if 'result' in timetable:
        logger.error("No timetable for this group: %s" % name)
        return get_message(M.TIMETABLE_WRONGGROUP)

    #date = arrow.get(datetime.datetime(2020, 2, 12), 'US/Pacific').shift(weekday = day, hours = 3)
    date = arrow.utcnow().shift(weekday = day, hours = 3) #Дата занятий

    #Проверяем совпадение дат
    flag = False
    table = timetable['table']['table'][day + 2]
    number = table[0]
    if(date.format("D  MMMM", locale="ru") in number):
        #Даты совпали
        flag = True

    #Если даты не совпали, то проверяем следующую неделю
    if(flag == False):
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
            logger.error("No timetable for this day: %s" % day)
            return get_message(M.TIMETABLE_NOTABLE)
    
    #Если даты совпали, то парсим расписание
    if(flag):
        text = ''
        j = 1
        for i in range(1, 7):
            if table[i] != '':
                text += "{}: {}\n {}\n\n".format(j, table[i], lesson[i])
                j += 1
                
        logger.error("Timetable was created: %s" % name)
        
        if j > 1:
            return 'Расписание на {}.\n\n{}'.format(date.format("D MMMM, dddd", locale = "ru"), text)
        else:
            return 'Расписание на {}.\nЗанятий нет\n'.format(date.format("D MMMM, dddd", locale = "ru"))
    else:
        #Если не совпадали, то расписание на этот день нет
        return get_message(M.TIMETABLE_NOTABLE)