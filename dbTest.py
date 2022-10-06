import asyncio

import DbUtils
from TicketEntity import TicketEntity, read_all_tickets
from UserEntity import UserEntity, read_all_users
from datetime import datetime

#tg_id, authorized, ticket_selected, user_id, name, stage, cur_ticket_num, last_sent_time


async def main_user():
    print("start")
    await DbUtils.create_tables()
    user1 = UserEntity()
    user2 = UserEntity()

    user1.set_tg_id("12345678")
    user2.set_tg_id("87654321")

    user1.set_authorized(True)
    user2.set_authorized(False)

    user1.set_ticket_selected(True)
    user2.set_ticket_selected(False)

    user1.set_user_id("12")

    user1.set_name("xd")
    user2.set_name("xd2")

    user1.set_stage("stage1")
    user2.set_stage("stage2")

    user1.set_selected_ticket_num("123-456")
    user2.set_selected_ticket_num("654-321")

    user1.set_last_sent_time(datetime.now())

    user1.set_name("test_update")
    await user1.update()
    await user2.update()

    info = await read_all_users()
    info1 = UserEntity()
    info1.set_tg_id("12345679")
    await info1.read_user()
    print("finish")


async def main_ticket():
    ticket1 = TicketEntity()
    ticket2 = TicketEntity()

    ticket1.set_ticket_num('123-456')
    ticket2.set_ticket_num('654-321')

    ticket1.set_owner_tg_id("12345678")
    ticket2.set_owner_tg_id("87654321")

    ticket1.set_ticket_id("12")

    ticket1.set_title("title1")
    ticket2.set_title("title2")

    ticket1.set_text("text1")
    ticket2.set_text("text2")

    ticket1.set_type_id(8)
    ticket2.set_type_id(9)

    #await ticket1.save()
    #await ticket2.save()

    print("save complete")

    ticket1.set_title("title3")

    await ticket1.update()

    print("update successful")

    ticket3 = TicketEntity()
    ticket3.set_ticket_num("123-456")
    await ticket3.read()

    print(ticket3.get_title())

    print(await read_all_tickets())


asyncio.run(main_ticket())
