from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import get_message
from config import bot
from Misc.message import Message
import requests
import logging
import arrow
import json
import datetime

logger = logging.getLogger('Bot.TimeTable')

lesson = {
    1 : 'с 08:00 до 09:35',
    2 : 'с 09:50 до 11:25',
    3 : 'с 11:55 до 13:30',
    4 : 'с 13:45 до 15:20',
    5 : 'с 15:50 до 17:25',
    6 : 'с 17:40 до 19:15',
    7 : 'с 19:30 до 21:05'
}

url = 'http://165.22.28.187/schedule-api/'

def GetTodayDate(day):
    if(type(day) == int):
        return arrow.utcnow().shift(days = day, hours = 3).format("D MMMM, dddd", locale = "ru")
    else:
        return day.format("D MMMM, dddd", locale = "ru")

def GetTimetable(name, day):
    #Обратиться к серверу для получения расписания
    try:
        response = requests.get(url + '?query=' + name)
    except:
        logger.error("Failed to connect to resource: %s" % name)
        return get_message(Message.M_TimeTable_NoConection.value)

    timetable = json.loads(response.text)
    
    #Проверка не пустое ли расписание
    if 'result' in timetable:
        logger.error("No timetable for this group: %s" % name)
        return get_message(Message.M_TimeTable_WrongGroup.value)

    #date = arrow.get(datetime.datetime(2020, 2, 12), 'US/Pacific').shift(weekday = day, hours = 3)
    date = arrow.utcnow().shift(weekday = day, hours = 3)

    flag = False
    table = timetable['table']['table'][day + 2]
    number = table[0]
    if(date.format("D  MMMM", locale="ru") in number):
        flag = True

    if(flag == False):   
        week = timetable['table']['week'] + 1
        if(week in timetable['weeks']):
            response = requests.get(url + '?group=' + timetable['table']['group'] + "&week=" + str(week))
            
            timetable = json.loads(response.text)

            table = timetable['table']['table'][day + 2]
            number = table[0]
            if(date.format("D  MMMM", locale="ru") in number):
                flag = True
        else:
            logger.error("No timetable for this day: %s" % day)
            return get_message(Message.M_TimeTable_NoTable.value)
    
    if(flag):
        text = ''
        j = 1
        for i in range(1, 7):
            if table[i] != '':
                text += "{}: {}\n {}\n\n".format(j, table[i], lesson[i])
                j += 1
                
        logger.error("Timetable was created: %s" % name)
        if j > 1:
            return 'Расписание на {}.\n\n{}'.format(GetTodayDate(date), text)
        else:
            return 'Расписание на {}.\nЗанятий нет\n'.format(GetTodayDate(date))
    else:
        return get_message(Message.M_TimeTable_NoTable.value)