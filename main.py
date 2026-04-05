import telebot # Тут була велика "I"
import json
from telebot import types

bot = telebot.TeleBot('8640349178:AAFnf9a5Evsyy00vnuL5Yld7zwSg5clmdIo')

# --- ФУНКЦІЇ ДЛЯ JSON (краще тримати їх зверху) ---
def load_data():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- ОБРОБНИКИ КОМАНД ---
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Привіт! Я твій перший ШІ-помічник.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Я поки що вчуся, не катуй мене! XD")

# --- ГОЛОВНИЙ ОБРОБНИК ТЕКСТУ (ОДИН НА ВСІ ВИПАДКИ) ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    # 1. ЗАПИСУЄМО В JSON (це спрацює на будь-яке повідомлення)
    users = load_data()
    user_id = str(message.from_user.id)
    
    if user_id not in users:
        users[user_id] = {"name": message.from_user.first_name, "actions": 0}
        bot.send_message(message.chat.id, f"Привіт, {message.from_user.first_name}! Я тебе запам'ятав.")
    
    users[user_id]["actions"] += 1
    save_data(users)
    
    # 2. ВІДПОВІДАЄМО НА ПИТАННЯ (Логіка if/elif)
    text = message.text.lower()
    
    if text == "привіт":
        bot.send_message(message.chat.id, "Привіт-привіт! Я вже працюю!")
    elif text == "ти хто?":
        bot.send_message(message.chat.id, "Я бот, якого створив Deras!")
    elif text == "статистика":
        count = users[user_id]["actions"]
        bot.send_message(message.chat.id, f"Ти написав мені вже {count} повідомлень!")
# ... твій код ...

    elif text == "меню":
        markup = types.InlineKeyboardMarkup()
        # ТУТ ВАЖЛИВО: посилання має бути https. 
        # Поки у тебе немає сайту, можна протестувати через будь-який https сайт,
        # але твій HTML файл запрацює тільки коли ти його закинеш на хостинг.
        web_app = types.WebAppInfo(url="https://deras23ua.github.io/my-bot-GUI/Gui.html")
        button = types.InlineKeyboardButton(text="Відкрити GUI 🚀", web_app=web_app)
        markup.add(button)
        
        bot.send_message(message.chat.id, "Натисни на кнопку, щоб відкрити меню:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Я тебе не розумію, але запис у базу зробив! XD")
 # Не забудь цей імпорт в самому верху!

@bot.message_handler(content_types=['web_app_data'])
def get_web_app_data(message):
    data = message.web_app_data.data # Отримуємо те, що відправила функція sendData
    
    if data == "language_menu":
        bot.send_message(message.chat.id, "Виберіть мову в меню додатка або напишіть її тут.")
    
    elif data == "back_to_main":
        bot.send_message(message.chat.id, "Повертаємось у головне меню!")
        
    elif data == "set_ua":
        bot.send_message(message.chat.id, "Мову змінено на Українську! 🇺🇦")
        # Тут можна оновити дані в users.json
        users = load_data()
        users[str(message.from_user.id)]["lang"] = "ua"
        save_data(users)

    else:
        bot.send_message(message.chat.id, f"Отримано команду: {data}")
        
# --- ЗАПУСК ---
print("Бот запущений і база працює...")
bot.polling(none_stop=True)