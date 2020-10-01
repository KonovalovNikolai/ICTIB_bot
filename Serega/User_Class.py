from requests import ConnectionError
import logging
import time

import sqlite3
import redis

from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import RedisHelper
from Handlers.Markups import (
    main_markup_abiturient_kb,
    main_markup_stud_kb,
    main_markup_teach_kb,
)
from telebot import TeleBot
from telebot.types import Message
from Misc import M, U, B, S


class User:
    def __init__(self, message: Message = None, bot: TeleBot = None):
        self.logger = logging.getLogger("Bot.User_Class")
        self.bot = bot
        if message:
            self.id = message.chat.id
            self.message_id = message.message_id
        else:
            self.id = None
        self.group = None
        self.type = None
        self.db: SQLHelper = None

    def SetDB(self):
        '''
        Создать подключение к бд, если его ещё нет
        '''
        if not self.db:
            self.db = SQLHelper()

    def SetQuestBrige(self, quest_id):
        '''
        Создать мост для вопроса
        '''
        RedisHelper().SetQuestBrige(self.id, quest_id)

    def SetState(self, state: int):
        '''
        Изменить состояние пользователя
        '''
        RedisHelper().SetState(self.id, state)

    def SetExpend(self, group = None, day = None):
        '''
        Установить параметры расширенного поиска
        '''
        RedisHelper().SetExpend(self.id, group, day)

    def GetExpend(self):
        '''
        Получить параметры расширенного поиска
        '''
        return RedisHelper().GetExpend(self.id)

    def GetUserInfo(self):
        '''
        Записать в поля класса параметры пользователя
        '''
        self.SetDB()
        info = self.db.TakeInfo(self.id)
        if info != None:
            _, self.type, self.group, *_ = info

    def GetUserQuest(self):
        '''
        Получить вопрос пользователя
        '''
        self.SetDB()
        return self.db.TakeQuest(self.id)

    def GetQuestById(self, message_id):
        '''
        Получить вопрос по id вопроса
        '''
        self.SetDB()
        quest = self.db.TakeQuestById(message_id)
        self.db.ReplaceQuest(quest[0])
        return quest

    def GetUserState(self):
        '''
        Получить состояние пользователя
        '''
        return RedisHelper().GetState(self.id)

    def GetQuestBrige(self):
        '''
        Получить мост
        '''
        return RedisHelper().GetQuestBrige(self.id)

    def GetRandomQuest(self):
        '''
        Получить случайный вопрос
        '''
        self.SetDB()
        return self.db.TakeRandomQuest()

    def GetMessage(self, value: str):
        '''
        Получить текст сообщения по его коду
        '''
        return RedisHelper().GetMessage(value)

    def GetFirstQuest(self):
        '''
        Получить первый в бд вопрос
        '''
        self.SetDB()
        return self.db.TakeFirsQuest()

    def GetUserVK(self):
        '''
        Получить подписки пользователя
        '''
        return RedisHelper().CheckUserVK(self.id)

    def AddUser(self, user_type, user_group):
        '''
        Добавить пользователя в бд
        '''
        self.SetDB()
        self.db.AddUser((self.id, user_type, user_group))

    def AddQuest(self, message_text):
        '''
        Добавть вопрос в бд
        '''
        self.SetDB()
        self.db.AddQuest(self.id, self.message_id, message_text)

    def UpdateAuto(self):
        '''
        Изменить параметр auto пользователя
        '''
        self.SetDB()
        return self.db.UpdateAuto(self.id)

    def UpdateVK(self, vk):
        '''
        Изменить подписки подписки пользователя
        '''
        RedisHelper().ChangeVK(self.id, vk)

    def BackToMain(self, text=M.MAINMENU, raw = True):
        """
        Функция для возврата пользователя в главное меню учитывая его тип.
        chat_id - id пользователя.
        text - текст сообщения для отправки.
        по умолчанию выводит "🏠 Главное меню."
        """
        # Берём из бд тип пользователя
        self.GetUserInfo()

        # Отправляем текст сообщения
        if self.type == U.STUDENT:
            self.SendMessage(
                text=text, reply_markup=main_markup_stud_kb, state=S.NORMAL, raw=raw
            )

            self.logger.error(
                 f'User {self.id} returned to main menu as student.'
            )

        elif self.type == U.TEACH:
            self.SendMessage(
                text=text, reply_markup=main_markup_teach_kb, state=S.NORMAL, raw=raw
            )
            self.logger.error(
                f'User {self.id} returned to main menu as teacher.'
            )

        elif self.type == U.ABITUR:
            self.SendMessage(
                text=text, reply_markup=main_markup_abiturient_kb, state=S.NORMAL, raw=raw
            )
            self.logger.error(
                f'User {self.id} returned to main menu as abiturient.'
            )

    def SendMessage(self, text, raw=True, reply_to_message_id=None, form: list = None, reply_markup=None, parse_mode=None, state=None):
        if raw:
            text = self.GetMessage(text)
            if form:
                text = text.format(*form)
        try:
            self.bot.send_message(
                chat_id=self.id,
                text=text,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except ConnectionError:
            # time.sleep(SLEEPTIME)
            self.bot.send_message(
                chat_id=self.id,
                text=text,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        if state != None:
            self.SetState(state)

    def SendMessageToAnotherUser( self, chat_id, text, raw=True, reply_to_message_id=None, form: list = None, reply_markup=None, parse_mode=None):
        if raw:
            text = self.GetMessage(text)
            if form:
                text = text.format(*form)
        try:
            self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except ConnectionError:
            # time.sleep(SLEEPTIME)
            self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )

    def SendLocation(self, building, reply_markup=None):
        try:
            self.bot.send_location(
                chat_id=self.id,
                latitude=building[1],
                longitude=building[2],
                reply_markup=reply_markup,
            )
        except ConnectionError:
            self.bot.send_location(
                chat_id=self.id,
                latitude=building[1],
                longitude=building[2],
                reply_markup=reply_markup,
            )

    def EditMessageText(self, text, reply_markup=None, parse_mode=None, form: list = None):
        text = self.GetMessage(text)
        if form:
            text = text.format(*form)
        self.bot.edit_message_text(
            chat_id=self.id,
            text=text,
            message_id=self.message_id,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )

    def EditMessageReplyMarkup(self, reply_markup=None):
        self.bot.edit_message_reply_markup(
            chat_id=self.id, message_id=self.message_id, reply_markup=reply_markup
        )

    def DeleteQuest(self):
        self.SetDB()
        self.db.DeleteQuest(self.id)

    def DeleteUserSQL(self):
        self.SetDB()
        self.db.DeleteUser(self.id)

    def DeleteUserRedis(self):
        RedisHelper().DeleteUser(self.id)

    def DeleteUser(self):
        self.DeleteUserSQL()
        self.DeleteUserRedis()

    def __del__(self):
        del self.db