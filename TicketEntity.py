import DbUtils


class TicketEntity:
    __INSERT_TICKET = """INSERT INTO 
        ticket(ticket_num, owner_tg_id, ticket_id, title, text, type_id) 
        VALUES (:ticket_num, :owner_tg_id, :ticket_id, :title, :text, :type_id);"""

    __UPDATE_TICKET = """UPDATE ticket SET   
        owner_tg_id = :owner_tg_id, 
        ticket_id = :ticket_id, 
        title = :title, 
        text = :text, 
        type_id = :type_id
        WHERE ticket_num = :ticket_num;"""

    __READ_TICKET_BY_TICKET_NUM = """SELECT * FROM ticket WHERE ticket_num = :ticket_num;"""

    def __init__(self):
        self.__ticket_num = ""
        self.__owner_tg_id = "0"
        self.__ticket_id = "0"
        self.__title = ""
        self.__text = ""
        self.__type_id = 9
        self.__last_answer = ""

    def set_owner_tg_id(self, tg_id: str) -> None:
        self.__owner_tg_id = tg_id

    def get_owner_tg_id(self) -> str:
        return self.__owner_tg_id

    def set_ticket_id(self, ticket_id: str) -> None:
        self.__ticket_id = ticket_id

    def get_ticket_id(self) -> str:
        return self.__ticket_id

    def set_ticket_num(self, ticket_num: str) -> None:
        self.__ticket_num = ticket_num

    def get_ticket_num(self) -> str:
        return self.__ticket_num

    def set_title(self, title: str) -> None:
        self.__title = title

    def get_title(self) -> str:
        return self.__title

    def set_text(self, text: str) -> None:
        self.__text = text

    def get_text(self) -> str:
        return self.__text

    def set_type_id(self, type_id: int) -> None:
        self.__type_id = type_id

    def get_type_id(self) -> int:
        return self.__type_id

    def set_last_answer(self, answer: str) -> None:
        self.__last_answer = answer

    def get_last_answer(self) -> str:
        return self.__last_answer

    async def save(self) -> None:
        if not DbUtils.database.is_connected:
            await DbUtils.database.connect()
        values = {
            "ticket_num": self.__ticket_num,
            "owner_tg_id": self.__owner_tg_id,
            "ticket_id": self.__ticket_id,
            "title": self.__title,
            "text": self.__text,
            "type_id": self.__type_id
        }
        await DbUtils.database.execute(query=self.__INSERT_TICKET, values=values)

    async def update(self) -> None:
        if not DbUtils.database.is_connected:
            await DbUtils.database.connect()
        values = {
            "ticket_num": self.__ticket_num,
            "owner_tg_id": self.__owner_tg_id,
            "ticket_id": self.__ticket_id,
            "title": self.__title,
            "text": self.__text,
            "type_id": self.__type_id
        }
        await DbUtils.database.execute(query=self.__UPDATE_TICKET, values=values)

    async def read(self) -> None:
        if not DbUtils.database.is_connected:
            await DbUtils.database.connect()
        values = {
            "ticket_num": self.__ticket_num
        }
        result = await DbUtils.database.fetch_one(query=self.__READ_TICKET_BY_TICKET_NUM, values=values)
        if result is None:
            raise Exception("no such ticket")
        self.__owner_tg_id = result[1]
        self.__ticket_id = result[2]
        self.__title = result[3]
        self.__text = result[4]
        self.__type_id = result[5]


READ_ALL_TICKETS = """SELECT * FROM ticket;"""


async def read_all_tickets() -> []:
    if not DbUtils.database.is_connected:
        await DbUtils.database.connect()
    data = await DbUtils.database.fetch_all(query=READ_ALL_TICKETS)
    tickets = []
    for ticket_data in data:
        ticket = TicketEntity()
        ticket.set_ticket_num(ticket_data[0])
        ticket.set_owner_tg_id(ticket_data[1])
        ticket.set_ticket_id(ticket_data[2])
        ticket.set_title(ticket_data[3])
        ticket.set_text(ticket_data[4])
        ticket.set_type_id(ticket_data[5])
        tickets.append(ticket)
    return tickets


