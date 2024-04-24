from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo
import json

bot = Bot('7111234144:AAEM82iAmq7uJGruhIUL64NsEdFUvmhmjho')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Open web',
                                    web_app=WebAppInfo(url='https://github.com/TihMish/Bot_Cotiki/blob/main/site.html'
                                                       )))
    await message.answer("Hi, my friend!", reply_markup=markup)

@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f'Name: {res["name"]}. Email: {res["email"]}. Phone: {res["phone"]}.')

executor.start_polling(dp)