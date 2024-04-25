from datetime import datetime, time

import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter

# Подключение к боту
bot = telebot.TeleBot('7111234144:AAEM82iAmq7uJGruhIUL64NsEdFUvmhmjho')
name = ''
API = "9fbad35bd5b70d3238c5f55b332ef163"
geonames_url = 'http://download.geonames.org/export/dump/'
basename = 'cities15000'
filename = basename + '.zip'
time_sp = {"санкт-петербург": 0, "калининград": -1, "киров": 0, "самара": 1, "саратов": 1,
           "екатеринбург": 2, "омск": 3, "красноярск": 4, "барнаул": 4, "новосибирск": 4, "иркутск": 5, "чита": 6,
           "владивосток": 7, "магадан": 8, "южно-сахалинск": 8, "анадырь": 9, "петропавловск-камчатский": 9}
currency = CurrencyConverter()
amount = 0


# Создание таблцы бд
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('botbd.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users '
                '(id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Hi, we need to reg you! Enter your name")
    bot.register_next_step_handler(message, user_name)


# Регистрация имени
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Enter your password")
    bot.register_next_step_handler(message, user_pass)


# Регистрация пароля
def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('botbd.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Users', callback_data='users'))
    bot.send_message(message.chat.id, "Registration was successful", reply_markup=markup)


# Вызов данных бд таблицы (Имени и пароля), Осуществление удаления фотографии и замены текста
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        values = call.data.split('/')
        try:
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f"Have a look: {round(res, 3)}. You can re-enter the amount")
            bot.register_next_step_handler(call.message, summa)
        except IndexError:
            if call.data == "edit":
                bot.edit_message_text('Not cat', call.message.chat.id, call.message.message_id)
            elif call.data == "delete":
                bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            elif call.data == "stop":
                bot.send_message(call.message.chat.id, f'Stop reade')
                bot.register_next_step_handler(start)
            elif call.data == 'else':
                bot.send_message(call.message.chat.id, f'Enter 2 words with "/"')
                bot.register_callback_query_handler(call.message, my_currency)
            else:
                conn = sqlite3.connect('botbd.sql')
                cur = conn.cursor()

                cur.execute('SELECT * FROM users')
                users = cur.fetchall()

                info = ""
                for i in users:
                    info += f"Name: {i[1]}, password: {i[2]}\n"

                cur.close()
                conn.close()

                bot.send_message(call.message.chat.id, info)
    except AttributeError:
        if call.data == "edit":
            bot.edit_message_text('Not cat', call.message.chat.id, call.message.message_id)
        elif call.data == "delete":
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "stop":
            bot.send_message(call.message.chat.id, f'Stop reade')
        elif call.data == 'else':
            bot.send_message(call.message.chat.id, f'Enter 2 words with "/"')
            bot.register_callback_query_handler(call.message, my_currency)


@bot.message_handler(commands=['money'])
def money(message):
    bot.send_message(message.chat.id, "Hi, enter the amount")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Error, not money. Enter the amount")
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("USD/EUR", callback_data='USD/EUR')
        btn2 = types.InlineKeyboardButton("EUR/USD", callback_data='EUR/USD')
        btn3 = types.InlineKeyboardButton("USD/GBP", callback_data='USD/GBP')
        btn4 = types.InlineKeyboardButton("Other", callback_data='else')
        btn5 = types.InlineKeyboardButton("Stop", callback_data='stop')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Choose money", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Error, money <= 0. Enter the amount")
        bot.register_next_step_handler(message, summa)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Have a look: {round(res, 3)}. You can re-enter the amount")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f"Error. You need re-enter value")
        bot.register_next_step_handler(message, my_currency)


# Обработка фотографии
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Go to site', url="https://tihmish.github.io/pr/site.html")
    btn2 = types.InlineKeyboardButton('Delete photo', callback_data="delete")
    btn3 = types.InlineKeyboardButton('Edit', callback_data="edit")
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.reply_to(message, 'So beautiful cat!', reply_markup=markup)


# Погода
@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Hi, write your city")


# Переход в ЛМС с проектом
@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://lms.yandex.ru/courses/1054/groups/8709/lessons/5979')


# Кнопочки для дальнейшей разработки
def on_click(message):
    if message.text == "Go to site":
        bot.send_message(message.chat.id, "Web is open")
    elif message.text == "Delete photo":
        bot.send_message(message.chat.id, "Del")
    elif message.text == "Edit":
        bot.send_message(message.chat.id, "Edit")


# Помощь и отзывы
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')


# Обработка погоды в городе
@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    weath = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if weath.status_code == 200:
        data = json.loads(weath.text)
        bot.reply_to(message, f'Now temperature: {data["main"]["temp"]}°C')
        t = datetime.now()
        hour = t.hour
        min = t.min
        for key in time_sp:
            if key == city:
                print(key)
                hour += time_sp[key]
        if hour > 24:
            hour -= 24
        image = ['ras.jpg', 'den.jpg', 'zac.jpg', 'noc.jpg']
        if 5 <= hour <= 12:
            print(1)
            file = open('./' + image[0], "rb")
        elif 12 < hour <= 18:
            print(2)
            file = open('./' + image[1], "rb")
        elif 18 < hour <= 20:
            print(3)
            file = open('./' + image[2], "rb")
        else:
            print(4)
            file = open('./' + image[3], "rb")
        bot.send_photo(message.chat.id, file)
    else:
        try:
            city = message.text.upper().split('/')
            bot.register_next_step_handler(message, my_currency)
        except Exception:
            bot.reply_to(message, f'Bad city')


# Приветствие и получение id
@bot.message_handler()
def info(message):
    if message.text.lower() == "hi":
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Go to site')
        btn2 = types.KeyboardButton('Delete photo')
        btn3 = types.KeyboardButton('Edit')
        markup.row(btn1)
        markup.row(btn2, btn3)
        file = open('./cotic.jpg', 'rb')
        bot.send_message(message.chat.id, f'Hi!, {message.from_user.first_name} '
                                          f'{message.from_user.last_name if message.from_user.last_name is not None else ""}')
        bot.send_photo(message.chat.id, file, reply_markup=markup)
        # bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name} {message.from_user.last_name
        # if message.from_user.last_name is not None else ""}', reply_markup=markup)
        bot.register_next_step_handler(message, on_click)

    elif message.text.lower() == "id":
        print(message.from_user.id)
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.infinity_polling()
