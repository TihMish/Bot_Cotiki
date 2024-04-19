import telebot
import webbrowser
from telebot import types
import sqlite3

# Подключение к боту
bot = telebot.TeleBot('7111234144:AAEM82iAmq7uJGruhIUL64NsEdFUvmhmjho')
name = ''


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
    if call.data == "delete":
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
    elif call.data == "edit":
        bot.edit_message_text('Not cat', call.message.chat.id, call.message.message_id)
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


# Обработка фотографии
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Go to site', url="https://google.com")
    btn2 = types.InlineKeyboardButton('Delete photo', callback_data="delete")
    btn3 = types.InlineKeyboardButton('Edit', callback_data="edit")
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.reply_to(message, 'So beautiful cat!', reply_markup=markup)


# Переход в ЛМС с проектом
@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://lms.yandex.ru/courses/1054/groups/8709/lessons/5979')


# Помощь и отзывы
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')


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


# Кнопочки для дальнейшей разработки
def on_click(message):
    if message.text == "Go to site":
        bot.send_message(message.chat.id, "Web is open")
    elif message.text == "Delete photo":
        bot.send_message(message.chat.id, "Del")
    elif message.text == "Edit":
        bot.send_message(message.chat.id, "Edit")


bot.infinity_polling()
