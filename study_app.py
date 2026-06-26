

import telebot
from telebot import types
import wikipediaapi
import g4f



wiki=wikipediaapi.Wikipedia(
    user_agent='JarvisBot/1.0',
    language='ru'
)

token = '8964269268:AAG4Iz-udvQftl-sdMH2MOYfCYIuuLC0o9k'
bot = telebot.TeleBot(token)

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Джарвис, помощь')
    markup.add(item)
    return markup



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я твой голосовой ассистент Джарвис. Напиши "Джарвис, помощь", чтобы узнать, что я умею.',
        reply_markup=get_main_keyboard()
    )

@bot.message_handler(func=lambda message: message.text=='Джарвис, помощь')
def help_message(message):
    help_text=(
    'Нажми на нужную кнопку снизу: \n'
    '- Джарвис, включи музыку\n'
         '- Джарвис, скинь фотку\n'
         '- Джарвис, я хочу задать вопрос\n'

        )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1=types.KeyboardButton('Джарвис, включи музыку')
    b2=types.KeyboardButton("Джарвис, скинь фотку")
    b3=types.KeyboardButton("Джарвис, я хочу задать вопрос")
    markup.add(b1,b2,b3)

    bot.send_message(message.chat.id, text=help_text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_button(message):
    if message.text== 'Джарвис, включи музыку':
        try:
            with open('avengers.mp3', 'rb') as audio:
                bot.send_audio(message.chat.id, audio, 'Слушаюсь, сэр! Включаю мстителей: ')
        except FileNotFoundError:
            bot.send_message(message.chat.id,'Сэр, произошла ошибка: файл `avengers.mp3` не найден')

    elif message.text=='Джарвис, скинь фотку':
        try:
            with open('Джарвис2.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id,photo)
        except FileNotFoundError:
                bot.send_photo(message.chat.id,photo, 'Простите сэр, я не смог найти этот файл в базе данных')

    elif message.text=='Джарвис, я хочу задать вопрос':
        msg=bot.send_message(message.chat.id, 'Слушаю вас, сэр! Какой у вас вопрос? : ')
        bot.register_next_step_handler(msg, ask_jarvis_ai)

def ask_jarvis_ai(message):
    user_query = message.text
    status_msg = bot.send_message(message.chat.id, 'Анализирую базу данных....')

    try:

        formatted_messages = [
            {'role': 'system', 'content': 'Ты-Джарвис, искусственный интеллект и личный ассистент. Отвечай вежливо, называй пользователя   ф"Сэр"'},
            {'role': 'user', 'content': user_query}
        ]


        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=formatted_messages
        )

        bot.delete_message(message.chat.id, status_msg.message_id)

        sent_msg = bot.send_message(message.chat.id,response)
        bot.register_next_step_handler(sent_msg, ask_jarvis_ai)

    except Exception as e:
        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except:
            pass
        sent_msg = bot.send_message(message.chat.id,
                                    'Сэр, возникли временные неполадки при обращении к ИИ-модулю. Пожалуйста, повторите запрос позже.')
        bot.register_next_step_handler(sent_msg, ask_jarvis_ai)
        print(f'Ошибка библиотеки g4f: {e}')

bot.infinity_polling()






