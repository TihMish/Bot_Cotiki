from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('7111234144:AAEM82iAmq7uJGruhIUL64NsEdFUvmhmjho')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Open web',
                                    web_app=WebAppInfo(url='https://github.com/TihMish/Bot_Cotiki/blob/main/site.html'
                                                       )))
    await message.answer("Hi, my friend!", reply_markup=markup)

executor.start_polling(dp)