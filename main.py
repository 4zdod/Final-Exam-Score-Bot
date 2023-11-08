import telebot
import sys
from telebot import types

bot = telebot.TeleBot('')

midterm = 0
endterm = 0

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('🏫 Final Exam Score')
    btn3 = types.KeyboardButton('Start')
    markup.add(btn2, btn3)

    bot.clear_step_handler(message)
    bot.send_message(message.chat.id, 'Привет, я Final Exam Score Bot!', reply_markup=markup)

@bot.message_handler()
def buttons(message):
        if message.text == '🏫 Final Exam Score':
            bot.send_message(message.chat.id, '1️⃣ Пожалуйста, введите свою оценку за Register Midterm:')
            bot.register_next_step_handler(message, get_midterm)

        elif message.text == 'Start':
            start(message)

@bot.message_handler()
def start_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('🏫 Final Exam Score')
    btn3 = types.KeyboardButton('Start')
    markup.add(btn2, btn3)

    bot.clear_step_handler(message)
    bot.send_message(message.chat.id, 'Привет, я Final Exam Score Bot!', reply_markup=markup)
    bot.send_message(message.chat.id, '1️⃣ Пожалуйста, введите свою оценку за Register Midterm:')
    bot.register_next_step_handler(message, get_midterm)

@bot.message_handler()
def get_midterm(message):
        global midterm
        try:
            midterm = float(message.text)

            if midterm < 25 and midterm > 0:
                bot.send_message(message.chat.id, "❌Ваша оценка ниже 25% на Register Mid-Term. По правилам оценивания это Retake!")
                stick = open('sticker.webp', 'rb')
                bot.send_sticker(message.chat.id, stick)
                kb = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text='Попробовать еще раз✅', callback_data='btn1')
                kb.add(btn)
                bot.send_message(message.chat.id, 'Нажмите сюда для еще одного подсчета', reply_markup=kb)

            if midterm < 0 or midterm > 100:
                bot.send_message(message.chat.id, "❌Вы неправильно ввели оценку, введите значение от 0 до 100")

                kb = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text='Попробовать еще раз✅', callback_data='btn1')
                kb.add(btn)
                bot.send_message(message.chat.id, 'Нажмите сюда, для еще одного подсчета', reply_markup=kb)

            if midterm >= 25 and midterm <= 100:
                bot.send_message(message.chat.id, '✅ Оценка за Register Mid-Term принята.')
                bot.send_message(message.chat.id, '2️⃣ Пожалуйста, введите свою оценку за Register End-Term:')
                bot.register_next_step_handler(message, get_endterm)

            with open("bd.txt", "a") as f:
                print(f'User:{message.from_user.first_name} {message.from_user.last_name}, Username:{message.from_user.username}, Midterm grade:{midterm}', file=f)

            if not message.text.isdigit() and not message.text(type) == float:
                    raise ValueError()
        except ValueError:
            bot.send_message(message.chat.id, "Вы неправильно ввели оценку!")
            bot.register_next_step_handler(message, get_midterm)

@bot.message_handler()
def get_endterm(message):
        global endterm, midterm
        try:
            endterm = float(message.text)
            term = ((midterm + endterm) / 2)

            if endterm < 25 and endterm > 0:
                bot.send_message(message.chat.id, "Ваша оценка ниже 25% на Register Endterm. По правилам оценивания это Retake!")
                stick = open('sticker.webp', 'rb')
                bot.send_sticker(message.chat.id, stick)
                kb = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text='Попробовать еще раз✅', callback_data='btn1')
                kb.add(btn)
                bot.send_message(message.chat.id, 'Нажмите сюда для еще одного подсчета', reply_markup=kb)

            if endterm < 0 or endterm > 100:
                bot.send_message(message.chat.id, "❌Вы неправильно ввели оценку, введите значение от 0 до 100")
                kb = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text='Попробовать еще раз✅', callback_data='btn1')
                kb.add(btn)
                bot.send_message(message.chat.id, 'Нажмите сюда, для еще одного подсчета', reply_markup=kb)

            if endterm >= 25 and endterm <= 100 and term >= 50:
                get_total(message)

            if term < 50 and midterm >= 25 and endterm >= 25:
                bot.send_message(message.chat.id, "❌Ваша оценка за Register Term ниже 50%. По правилам оценивания это Retake!")
                stick = open('sticker.webp', 'rb')
                bot.send_sticker(message.chat.id, stick)
                kb = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text='Попробовать еще раз✅', callback_data='btn1')
                kb.add(btn)
                bot.send_message(message.chat.id, 'Нажмите сюда для еще одного подсчета', reply_markup=kb)

            with open("bd.txt", "a") as f:
                print(f'User:{message.from_user.first_name} {message.from_user.last_name}, Username:{message.from_user.username}, Endterm grade:{endterm}', file=f)

            if not message.text.isdigit() and not message.text(type) == float:
                raise ValueError()
        except ValueError:
            bot.send_message(message.chat.id, "❌Вы неправильно ввели оценку, введите повторно!")
            bot.register_next_step_handler(message, get_endterm)

@bot.message_handler()
def get_total(message):
    if midterm * 0.3 + endterm * 0.3 >= 50:
        vishka_grade = round((90 - (midterm * 0.3 + endterm * 0.3))/0.4, 2)
        vishka = f'🔵 Для получения повышенной стипендии (>90) {vishka_grade} % на файнале!'
    elif midterm * 0.3 + endterm * 0.3 < 50:
        vishka = '🔵 Для получения повышенной стипендии (>90) Heвозможно получить!'

    if midterm * 0.3 + endterm * 0.3 >= 30 and midterm * 0.3 + endterm * 0.3 <= 50:
        stepuha_grade = round((70 - (midterm * 0.3 + endterm * 0.3))/0.4, 2)
        stepuha = f'🔴 Для сохранения стипендии (>70) {stepuha_grade}% на файнале!'
    elif midterm * 0.3 + endterm * 0.3 >= 50:
        stepuha = '🔴 Для сохранения стипендии (>70) 50% на файнале!'
    elif midterm * 0.3 + endterm * 0.3 < 30:
        stepuha = '🔴 Для сохранения стипендии (>70) Heвозможно получить!'

    if midterm * 0.3 + endterm * 0.3 >= 15 and midterm * 0.3 + endterm * 0.3 <= 30:
        letnik_grade = round((50 - (midterm * 0.3 + endterm * 0.3)) / 0.4, 2)
        letnik = f'⚫ Чтобы не получить ретейк или пересдачу (>50) {letnik_grade}% на файнале!'
    elif midterm * 0.3 + endterm * 0.3 >= 30:
        letnik = '⚫ Чтобы не получить ретейк или пересдачу (>50) 50% на файнале!'
    elif midterm * 0.3 + endterm * 0.3 < 15:
        letnik = '⚫ Чтобы не получить ретейк или пересдачу (>50) Ой, у вас летник!'

    totalscore_grade = round((midterm * 0.3 + endterm * 0.3 + 40), 2)
    totalscore = f'⚪ Если вы получите 100% на файнале, ваш тотал будет {totalscore_grade}%!'

    bot.send_message(message.chat.id, letnik)
    bot.send_message(message.chat.id, stepuha)
    bot.send_message(message.chat.id, vishka)
    bot.send_message(message.chat.id, totalscore)

    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Попробовать еще раз✅', callback_data='btn1')
    kb.add(btn)
    bot.send_message(message.chat.id, '            👇            ', reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def inline_handler(call):
    if call.data == 'btn1':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_2(call.message)

while True:
    try:
        bot.polling()
    except:
        continue

