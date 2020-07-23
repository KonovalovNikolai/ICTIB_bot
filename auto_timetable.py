from config import bot
from Serega.Timetable import GetTimetable
from DB_Helper.SQLHelper import SQLHelper

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
                    res = GetTimetable(group, True)
                    if res:
                        for user in users:
                            print(user, users)
                            bot.send_message(chat_id = user[0],
                                            text = res)

teachers = db_worker.Execute("SELECT id, gp FROM user WHERE auto = 1 AND type = 'teach'")
for teacher in teachers:
    res = GetTimetable(teacher[1], True)
    if res:
        bot.send_message(chat_id = teacher[0],
                        text = res)

db_worker.close()
                    