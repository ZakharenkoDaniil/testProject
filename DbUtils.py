import asyncio
import json
import aiosqlite

from databases import Database

database = Database("sqlite:///C://Users//zakha//PycharmProjects//aiogramTest//bot.db")


CREATE_USER_TABLE_QUERY_IF_NOT_EXISTS = """CREATE TABLE IF NOT EXISTS user(
   tg_id VARCHAR (20) PRIMARY KEY UNIQUE NOT NULL,
   authorized BOOLEAN NOT NULL DEFAULT True,
   ticket_selected BOOLEAN NOT NULL,
   user_id VARCHAR (20),
   name VARCHAR (50) NOT NULL,
   stage VARCHAR (20) NOT NULL,
   cur_ticket_num VARCHAR (20),
   last_sent_time TIME
   );
"""

CREATE_TICKET_TABLE_QUERY_IF_NOT_EXISTS = """CREATE TABLE IF NOT EXISTS ticket(
   ticket_num VARCHAR (20) PRIMARY KEY NOT NULL,
   owner_tg_id VARCHAR(20) NOT NULL,
   ticket_id VARCHAR (20),
   title VARCHAR (50),
   text TEXT,
   type_id INTEGER
   );
"""


async def create_tables() -> None:
    await database.connect()
    create_user_table_task = database.execute(query=CREATE_USER_TABLE_QUERY_IF_NOT_EXISTS)
    create_ticket_table_task = database.execute(query=CREATE_TICKET_TABLE_QUERY_IF_NOT_EXISTS)
    await asyncio.gather(create_user_table_task, create_ticket_table_task)
