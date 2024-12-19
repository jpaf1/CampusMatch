import telebot
import database
import algorithm
import schedule


bot = telebot.TeleBot('7994757091:AAHaZ-FjncULD9Q0F34Claq13iDy7E-jpGY')

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
    main_str = ('CampusMatch - связи решают всё 💵🎓\n\n')
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
    id = callback.message.chat.id
    username = callback.message.chat.username
    database.add_user(id,username)

@bot.callback_query_handler(func=lambda callback: callback.data == 'meeting') #Ответ на кнопку "Получить линк"
def callback_linc(callback):
    linc = database.get_new_friend(callback.message.chat.id)
    if linc == 0:
        murkup = telebot.types.InlineKeyboardMarkup()
        murkup.add(telebot.types.InlineKeyboardButton('Попробовать снова', callback_data='meeting'))
        murkup.add(telebot.types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main'))
        info_str = (f'Достаточное киличество участников пока не набралось')
        bot.send_message(callback.message.chat.id, info_str, reply_markup=murkup)
    else:
        murkup = telebot.types.InlineKeyboardMarkup()
        murkup.add(telebot.types.InlineKeyboardButton('Вернуться в главное меню', callback_data='main'))
        info_str = (f'Новые знакомства и возможности ждут тебя!\n\n @{linc}')
        bot.send_message(callback.message.chat.id, info_str, reply_markup=murkup)

#schedule.every().saturday.at("00:01").do(algorithm.alg())

bot.polling(none_stop=True)