from datetime import datetime
import maya

import DbUtils
from IdFinderThread import IdFinderThread
from TicketEntity import TicketEntity


class UserEntity:

    __INSERT_USER = """INSERT INTO 
    user(tg_id, authorized, ticket_selected, user_id, name, stage, cur_ticket_num, last_sent_time) 
    VALUES (:tg_id, :authorized, :ticket_selected, :user_id, :name, :stage, :cur_ticket_num, :last_sent_time);"""

    __UPDATE_USER = """UPDATE user SET  
    authorized = :authorized, 
    ticket_selected = :ticket_selected, 
    user_id = :user_id, 
    name = :name, 
    stage = :stage, 
    cur_ticket_num = :cur_ticket_num, 
    last_sent_time = :last_sent_time
    WHERE tg_id = :tg_id;"""

    __READ_USER_BY_TG_ID = """SELECT * FROM user WHERE tg_id = :tg_id;"""

    def __init__(self):
        self.__authorized = False
        self.__ticket_selected = False
        self.__user_id = ''
        self.__tg_id = ''
        self.__name = ''
        self.__stage = None
        self.__selected_ticket_num = ''
        self.__buf_ticket = TicketEntity()
        self.__tickets = {}
        self.__id_finder = IdFinderThread(tg_id='', f_name='', user_id='')
        self.__docs = []
        self.__collector = None
        self.__last_sent_time = None

    def set_authorized(self, authorized: bool) -> None:
        self.__authorized = authorized

    def is_authorized(self) -> bool:
        return self.__authorized

    def set_ticket_selected(self, selected: bool) -> None:
        self.__ticket_selected = selected

    def is_ticket_selected(self) -> bool:
        return self.__ticket_selected

    def set_user_id(self, user_id: str) -> None:
        self.__user_id = user_id

    def get_user_id(self) -> str:
        return self.__user_id

    def set_tg_id(self, tg_id: str) -> None:
        self.__tg_id = tg_id

    def get_tg_id(self) -> str:
        return self.__tg_id

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_stage(self, stage: str) -> None:
        self.__stage = stage

    def get_stage(self) -> str:
        return self.__stage

    def set_selected_ticket_num(self, num: str) -> None:
        self.__selected_ticket_num = num

    def get_selected_ticket_num(self) -> str:
        return self.__selected_ticket_num

    def set_buf_ticket(self, ticket: TicketEntity) -> None:
        self.__buf_ticket = ticket

    def get_buf_ticket(self) -> TicketEntity:
        return self.__buf_ticket

    def add_ticket(self, ticket: TicketEntity) -> None:
        if ticket.get_ticket_num() == "":
            raise AttributeError("ticket has not attribute \"ticket_num\"")
        self.__tickets.update({ticket.get_ticket_num(): ticket})

    def get_ticket_by_num(self, num: str) -> TicketEntity:
        return self.__tickets.get(num)

    def get_tickets(self) -> {}:
        return self.__tickets

    def set_id_finder(self, thread: IdFinderThread) -> None:
        self.__id_finder = thread

    def get_id_finder(self) -> IdFinderThread:
        return self.__id_finder

    def set_docs(self, docs: []) -> None:
        self.__docs = docs

    def get_docs(self) -> []:
        return self.__docs

    def set_collector(self, collector) -> None:
        self.__collector = collector

    def get_collector(self):
        return self.__collector

    def set_last_sent_time(self, time_value) -> None:
        self.__last_sent_time = time_value

    def get_last_sent_time(self) -> datetime:
        return self.__last_sent_time

    async def save(self) -> None:
        if not DbUtils.database.is_connected:
            await DbUtils.database.connect()
        values = {
            "tg_id": self.__tg_id,
            "authorized": self.__authorized,
            "ticket_selected": self.__ticket_selected,
            "user_id": self.__user_id,
            "name": self.__name,
            "stage": self.__stage,
            "cur_ticket_num": self.__selected_ticket_num,
            "last_sent_time": self.__last_sent_time
        }
        await DbUtils.database.execute(query=self.__INSERT_USER, values=values)

    async def update(self) -> None:
        if not DbUtils.database.is_connected:
            await DbUtils.database.connect()
        values = {
            "tg_id": self.__tg_id,
            "authorized": self.__authorized,
            "ticket_selected": self.__ticket_selected,
            "user_id": self.__user_id,
            "name": self.__name,
            "stage": self.__stage,
            "cur_ticket_num": self.__selected_ticket_num,
            "last_sent_time": self.__last_sent_time
        }
        await DbUtils.database.execute(query=self.__UPDATE_USER, values=values)

    async def read_user(self) -> None:
        if not DbUtils.database.is_connected:
            await DbUtils.database.connect()
        values = {
            "tg_id": self.__tg_id
        }
        result = await DbUtils.database.fetch_one(query=self.__READ_USER_BY_TG_ID, values=values)
        if result is None:
            raise Exception("no such user")
        self.__authorized = True if result[1] == 1 else False
        self.__ticket_selected = True if result[2] == 1 else False
        self.__user_id = result[3]
        self.__name = result[4]
        self.__stage = result[5]
        self.__selected_ticket_num = result[6]
        self.__last_sent_time = None if result[7] is None else maya.parse(result[7]).datetime()


READ_ALL_USERS = """SELECT * FROM user;"""


async def read_all_users() -> []:
    if not DbUtils.database.is_connected:
        await DbUtils.database.connect()
    data = await DbUtils.database.fetch_all(query=READ_ALL_USERS)
    users = []
    for user_data in data:
        user = UserEntity()
        user.set_authorized(True if user_data[1] == 1 else False)
        user.set_ticket_selected(True if user_data[2] == 1 else False)
        user.set_user_id(user_data[3])
        user.set_name(user_data[4])
        user.set_stage(user_data[5])
        user.set_selected_ticket_num(user_data[6])
        user.set_last_sent_time(None if user_data[7] is None else maya.parse(user_data[7]).datetime())
        users.append(user)
    return users
