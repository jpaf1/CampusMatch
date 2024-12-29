import telebot
from database import Database
from algorithm import PairingAlgorithm

bot = telebot.TeleBot('7994757091:AAHaZ-FjncULD9Q0F34Claq13iDy7E-jpGY')

db_facade = Database()

@bot.message_handler(commands = ['start']) # Ответ на команду /start
def start(chat):
    murkup = telebot.types.InlineKeyboardMarkup()
    murkup.add(telebot.types.InlineKeyboardButton('Начать нетворкаться', callback_data='choice'))
    murkup.add(telebot.types.InlineKeyboardButton('Тут будет сайт',callback_data='site')) #Todo кнопка, ведущая на сайт
    hi_str = 'Приветствую! Этот бот поможет тебе найти единомышленников среди студентов.'
    bot.send_message(chat.chat.id, hi_str, reply_markup=murkup)

@bot.callback_query_handler(func=lambda callback: callback.data == 'main')
@bot.message_handler(commands = ['main']) # Ответ на команду /main
def main(callback):
    murkup = telebot.types.InlineKeyboardMarkup()
    murkup.add(telebot.types.InlineKeyboardButton('Получить линк', callback_data='meeting'))
    main_str = ('CampusMatch - найди новых друзей🎓\n\n')
    bot.send_message(callback.message.chat.id, main_str, reply_markup=murkup)

@bot.callback_query_handler(func=lambda callback: callback.data == 'choice') #Ответ на кнопку "Начать нетворкаться"
def callback_start(callback):
    murkup = telebot.types.InlineKeyboardMarkup()
    murkup.add(telebot.types.InlineKeyboardButton('Получить линк', callback_data='meeting'))
    info_str = ('Отлично!\n\n'
                '· Каждую субботу ты сможешь получить линк нового друга 😁\n\n'
                '· Твоя задача - написать этому человеку и встрериться с ним на неделе 🤝\n\n')
    bot.send_message(callback.message.chat.id, info_str, reply_markup=murkup)

    #Добавление пользователя в базу данных
    user_id = callback.message.chat.id
    username = callback.message.chat.username
    db_facade.add_user(user_id, username)

@bot.callback_query_handler(func=lambda callback: callback.data == 'meeting') #Ответ на кнопку "Получить линк"
def callback_linc(callback):
    new_friend_id = db_facade.get_new_friend(callback.message.chat.id)
    if not new_friend_id:
        murkup = telebot.types.InlineKeyboardMarkup()
        murkup.add(telebot.types.InlineKeyboardButton('Попробовать снова', callback_data='meeting'))
        murkup.add(telebot.types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main'))
        info_str = (f'Достаточное киличество участников пока не набралось, или тебе стоит подождать до следующей субботы 😉')
        bot.send_message(callback.message.chat.id, info_str, reply_markup=murkup)
    else:
        murkup = telebot.types.InlineKeyboardMarkup()
        murkup.add(telebot.types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main'))
        info_str = (f'Новые знакомства и возможности ждут тебя!\n\n @{new_friend_id}')
        bot.send_message(callback.message.chat.id, info_str, reply_markup=murkup)

@bot.message_handler(commands = ['update']) # Ответ на команду /update
def update(chat):
    id = chat.from_user.id
    if id == 881088174:
        twice_user = int((chat.text).split()[1])
        PairingAlgorithm.match_users(twice_user)
        update_str = 'Список успешно обновлён'
        bot.send_message(chat.chat.id, update_str)
    else:
        not_update_str = 'Вы пытаетесь вызвать команду администратора'
        bot.send_message(chat.chat.id, not_update_str)

bot.polling(none_stop=True)