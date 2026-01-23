import os
from dotenv import load_dotenv
import telebot

# загружаем переменные окружения
load_dotenv()

# получаем токен
TELEGRAM_TOKEN = os.environ.get('BOT_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("❌ Токен не найден! Проверьте файл .env")

# создаем объект бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.reply_to(message, f"Привет, {name}! 👋 Я твой первый Telegram-бот.")

# обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Я умею:\n"
        "/start — поздороваться\n"
        "/help — показать эту справку\n"
        "Напиши что-нибудь — я повторю!"
    )
    bot.reply_to(message, help_text)

# обработчик команды /caps
@bot.message_handler(commands=['caps'])
def send_caps(message):
    msg = message.text[6:].strip() # /caps сообщение
    bot.reply_to(message, msg.upper())

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_message = message.text.strip()
    if 'привет' == user_message.lower():
        bot.reply_to(message, "Привет! Рад тебя видеть! Чем могу помочь?\n/help — показать эту справку")
    else:
        bot.reply_to(message, user_message)

# запуск бота
if __name__ == '__main__':
    print("✅ Бот запущен! Нажмите Ctrl+C, чтобы остановить.")
    bot.infinity_polling()