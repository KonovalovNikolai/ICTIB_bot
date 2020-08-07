from enum import Enum

MAINMENU = '0' #ГЛАВНОЕ МЕНЮ

START_GREETINGS = '1' # ПЕРЕД НАЧАЛОМ РАБОТЫ МНЕ НУЖНО УЗНАТЬ О ВАС НЕМНОГО ИНФОРМАЦИИ. ДАВАЙТЕ ОПРЕДЕЛИМ, К КАКОЙ ГРУППЕ ПОЛЬЗОВАТЕЛЕЙ ВЫ ОТНОСИТЕСЬ
START_STUDENT = '2' #ХОРОШО! ИДЁМ ДАЛЕЕ.\NТЕПЕРЬ ВВЕДИ ШИФР СВОЕЙ ГРУППЫ. НАПРИМЕР, КТБО1-6.
START_TEACHER = '3' #ОТЛИЧНО! ПРОДОЛЖИМ.\NТЕПЕРЬ ВВЕДИ СВОЮ ФАМИЛИЮ И ИНИЦИАЛЫ. НАПРИМЕР, ИВАНОВ И. И.\N ЭТО УПРОСТИТ ВАМ И МНЕ РАБОТУ. ЕСЛИ ВЫ НЕКОРЕКТНО ВВЕЛИ ДАННЫЕ, ТО НЕКОТОРЫЕ ФУНКЦИИ БУДУТ НЕ ДОСТУПНЫ. НО НИЧЕГО СТРАШНОГО, ВЫ СМОЖЕТЕ ИЗМЕНИТЬ ИХ В НАСТРОЙКАХ.
START_ABITUR = '4' #ЗАПИСАЛ, ЭТОГО ДОСТАТОЧНО
START_THANKS = '5' #СПАСИБО! <3
    
CLEAR_СONFIRMATION = '6' #ВЫ ДЕЙСТВИТЕЛЬНО ХОТИТЕ, ЧТО БЫ Я ЗАБЫЛ ВСЮ ИНФОРМАЦИЮ О ВАС?
CLEAR_BYE = '7' #ДО СВИДАНИЯ! ЧТОБЫ ЗАНОВА НАЧАТЬ РАБОТУ СО МНОЙ, ВВЕДИТЕ КОМАНДУ /START
CLEAR_CANCEL = '8' #ПРИЯТНО ЭТО СЛЫШАТЬ! :)

TIMETABLE_TODAY = '9' #СЕГОДНЯ {}.\NВЫБЕРИТЕ ДЕНЬ НЕДЕЛИ.
TIMETABLE_NOCONECTION = '10' #ПРОСТИТЕ, В ДАННЫЙ МОМЕНТ НЕЛЬЗЯ ПОЛУЧИТЬ РАСПИСАНИЕ. :(
TIMETABLE_WRONGGROUP = '11'
TIMETABLE_NOTABLE = '12' #ЧТО-ТО ПОШЛО НЕ ТАК ИЛИ НА ЭТОТ ДЕНЬ РАСПИСАНИЯ НЕТ.

ERROR_WRONG_INPUT = '13' #НЕКОРРЕКТНЫЙ ВВОД.\NПОВТОРИТЕ ПОПЫТКУ.
ERROR_WRONG_CHOICE = '14' #ВЫБЕРИ ЧТО-ТО ИЗ ПРЕДЛОЖЕННОГО!
ERROR_SOMTING_WRONG = '15' #ЧТО-ТО ПОШЛО НЕ ТАК
