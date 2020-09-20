import redis

A = {
    "0": "🏠 Главное меню.",
    "1": "Перед началом работы мне нужно узнать о вас немного информации. Давайте определим, к какой группе пользователей вы относитесь",
    "2": "Хорошо! Идём далее.\nТеперь введи шифр своей группы. Например, КТбо1-6.",
    "3": "Отлично! Продолжим.\nТеперь введи свои инициалы. Например, Иванов И. И.\n Это упростит вам и мне работу. Если вы некоректно ввели данные, то некоторые функции будут не доступны. Но ничего страшного, вы сможете изменить их в настройках.",
    "4": "Записал, этого достаточно",
    "5": "Спасибо! <3",
    "6": "Вы действительно хотите, что бы я забыл всю информацию о вас?",
    "7": "До свидания! Чтобы занова начать работу со мной, введите команду /start",
    "8": "Приятно это слышать! :)",
    "9": "Сегодня {}.\nВыберите день недели.",
    "10": "Простите, в данный момент нельзя получить расписание.",
    "11": "Не удалось получить расписание. Возможно, указаны некоректные данные.",
    "12": "На этот день расписания нет.",
    "13": "Некорректный ввод.\nПовторите попытку.",
    "14": "Выбери что-то из предложенного!",
    "15": "Что-то пошло не так ~_~",
    "16": "У вас уже есть заданный вопрос:\n<i>Вопрос №{}\n{}</i>",
    "17": 'Всё, что вы хотели знать об институте, но боялись спросить.\n Теперь абитуриенты могут задавать вопросы студентам, при этом сохраняя анонимность. Просто напишите мне ваш вопрос, а я найду студента, который ответит на ваш вопрос. Пожалуйста, соблюдайте правила приличия, задавая вопрос. Также убедитесь, что ответа на ваш вопрос нет в разделе "Частые вопросы".',
    "18": "Я записал ваш вопрос. Скоро на него ответят.",
    "19": "Вопросов пока нет.",
    "20": "Ответ отправлен.",
    "21": "На ваш вопрос ответили!",
    "22": "Меню настроек",
    "23": "Разработчик: @liz_zard",
    "24": "БОТ",
    "25": "Выберите тип пользователя.",
    "26": "Введите вашу группу. Например, КТбо1-6.",
    "27": "Введите ваше ФИО. Например, Иванов И. И.",
    "28": "Авто расписание включено.",
    "29": "Авто расписание выключено.",
    "30": "Интерфейс обновлён.",
    "31": "Вопрос №{}\n<i>{}</i>",
    "32": "Введите ваш ответ.",
    "33": "Вопрос удалён.",
    "34": "Вопрос №{}\n<i>{}</i>",
    "35": "Корпус «Г».",
    "36": "Корпус «Д».",
    "37": "Корпус «И».",
    "38": "Корпус «А».\nЦентр Довузовской Подготовки.",
    "39": "Корпус «Е»",
    "40": "Корпус «К»",
    "41": "Корпус «В»",
    "42": "Корпус «Б»",
    "43": "cock",
    "44": "cock",
    "45": "cock",
    "46": "cock",
    "47": "cock",
    "48": "cock",
    "49": "cock",
    "50": "cock",
    "51": "Выбирете корпус.",
    "52": "В воскресенье нет пар.",
    "53": "Подписки на официальные группы института.\n❌: так отмеченны неотслеживаемые группы.\n✔️: а так - отслеживаемые.",
}

with redis.Redis(db=1) as r:
    for i in A.keys():
        r.set(i, A[i])
