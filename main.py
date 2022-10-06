import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType

BOT_TOKEN = '5766288724:AAEp6KuWH62XEHFHf_NtKXWo2YQNcWmtSh0'

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class FSMachine(StatesGroup):
    stage1 = State()
    stage2 = State()
    stage3 = State()


@dp.message_handler(commands=['start'], state='*')
async def cm_start(message: types.Message, state: FSMContext):
    await FSMachine.stage1.set()
    await bot.send_message(chat_id=message.from_user.id, text='/next_state - переход в следующее состояние'
                                                              '\n/state_name - вывести название состояния')


@dp.message_handler(commands=['next_state'], state=FSMachine.stage1)
async def cm_set_state_2(message: types.Message, state: FSMContext):
    await FSMachine.stage2.set()
    await bot.send_message(chat_id=message.from_user.id, text='состояние #2 установлено\n'
                                                              '/next_state - переход в следующее состояние\n'
                                                              '/state_name - вывести название состояния')


@dp.message_handler(commands=['next_state'], state=FSMachine.stage2)
async def cm_set_state_3(message: types.Message, state: FSMContext):
    await FSMachine.stage3.set()
    await bot.send_message(chat_id=message.from_user.id, text='состояние #3 установлено\n'
                                                              '/next_state - переход в следующее состояние\n'
                                                              '/state_name - вывести название состояния')


@dp.message_handler(commands=['state_name'], state=None)
async def cm_get_state_name(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='state name is \'None\'')


@dp.message_handler(commands=['state_name'], state=FSMachine.stage1)
async def cm_get_state_name(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='state name is \'state1\'')


@dp.message_handler(commands=['state_name'], state=FSMachine.stage2)
async def cm_get_state_name(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='state name is \'state2\'')


@dp.message_handler(commands=['state_name'], state=FSMachine.stage3)
async def cm_get_state_name(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='state name is \'state3\'')


@dp.message_handler(content_types=["document", "photo"], state='*')
async def get_document(message: types.Message, state: FSMContext):
    print("check")
    path = "./downloaded_files/"
    if message.content_type == ContentType.PHOTO:
        print("photo")
        file = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_id = file.file_id
        file_name = file.file_path
        await bot.download_file_by_id(file_id=file_id, destination=path+file_name)
    elif message.content_type == ContentType.DOCUMENT:
        print("document")
        file_id = message.document.file_id
        path += message.document.file_name
        await bot.download_file_by_id(file_id=file_id, destination=path)
        print(file_id+" "+message.document.file_name)
        #await bot.download_file(file_info, path)


async def main():
    await dp.start_polling(timeout=20)


if __name__ == '__main__':
    asyncio.run(main())
