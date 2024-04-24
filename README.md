# Bot_Cotiki

Создание telegram бота

Подключение его к сайту и бд

# Создание таблцы бд
@bot.message_handler(commands=['start'])

# Регистрация имени
def user_name(message):

# Регистрация пароля
def user_pass(message):

# Переход в ЛМС с проектом
@bot.message_handler(commands=['site', 'website'])

# Приветствие и получение id
@bot.message_handler(content_types=["hi", "Hello", "Hi", "hello"])

# Кнопочки для дальнейшей разработки
def on_click(message):

# Вызов данных бд таблицы (Имени и пароля), Осуществление удаления фотографии и замены текста
@bot.callback_query_handler(func=lambda call: True)

# Ввод суммы
@bot.message_handler(commands=['money'])

# Подсчёт валют для покупки вещичек для котика
def my_currency(message):

# Погода
@bot.message_handler(commands=["weather"])

# Обработка погоды в городе
@bot.message_handler(content_types=["text"])

# Обработка фотографии
@bot.message_handler(content_types=['photo'])
