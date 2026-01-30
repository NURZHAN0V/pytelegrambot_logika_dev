import os
from dotenv import load_dotenv
import telebot
from telebot import types
import json

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.environ.get('BOT_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("❌ Токен не найден! Проверьте файл .env")

# Создаём объект бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)
last_photo_file_id = None
last_video_file_id = None
notes = {}
NOTES_FILE = "notes.json"


os.makedirs("images", exist_ok=True)
os.makedirs("videos", exist_ok=True)
os.makedirs("notes", exist_ok=True)


def save_notes(chat_id, notes):
    path = f'notes/{chat_id}'
    os.makedirs(path, exist_ok=True)

    # Получаем все файлы с расширением .json
    json_files = [
        f for f in os.listdir(path)
        if f.endswith('.json') and f[:-5].isdigit()  # проверяем, что имя до .json — число
    ]

    if json_files:
        # Извлекаем числа и находим максимум
        ids = [int(f[:-5]) for f in json_files]
        next_id = max(ids) + 1
    else:
        next_id = 1

    filepath = os.path.join(path, f'{next_id}.json')
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def load_notes():
    global notes
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        notes = {}


@bot.message_handler(commands=['note'])
def add_note(message):
    chat_id = str(message.chat.id)
    text = message.text[6:].strip()  # убираем "/note "

    if not text:
        bot.reply_to(message, "❌ Напишите текст после /note\nПример: /note Купить молоко")
        return

    if chat_id not in notes:
        notes[chat_id] = []

    notes[chat_id].append(text)
    print(notes[chat_id])  # для отладки

    # ✅ Передаём именно список заметок этого чата
    save_notes(chat_id, notes[chat_id])

    bot.reply_to(message, f"✅ Записал: {text}")
    

@bot.message_handler(commands=['notes'])
def list_notes(message):
    load_notes()
    chat_id = str(message.chat.id)
    if chat_id not in notes or not notes[chat_id]:
        bot.reply_to(message, "📭 У вас пока нет заметок.")
        return

    note_list = "\n".join(f"{i+1}. {note}" for i, note in enumerate(notes[chat_id]))
    bot.reply_to(message, f"📝 Ваши заметки:\n{note_list}")


@bot.message_handler(commands=['save'])
def force_save(message):
    save_notes()
    bot.reply_to(message, "💾 Все заметки сохранены!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global last_photo_file_id
    file_id = message.photo[-1].file_id
    last_photo_file_id = file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"images/{file_id}.jpg", 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, "✅ Изображение сохранено")


@bot.message_handler(content_types=['video'])
def handle_video(message):
    global last_video_file_id
    file_id = message.video.file_id
    last_video_file_id = file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"videos/{file_id}.mp4", 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, "✅ Видео сохранено")


# Функция для отображения главного меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("О нас")
    btn2 = types.KeyboardButton("Отправить фото")
    btn3 = types.KeyboardButton("Мои заметки")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.reply_to(message, f"Привет, {name}! 👋 Я твой первый Telegram-бот.")
    show_main_menu(message)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "Я умею:\n"
        "/start — поздороваться\n"
        "/help — показать эту справку\n"
        "/caps — преобразовать текст в ВЕРХНИЙ РЕГИСТР\n"
        "Напиши что-нибудь — я повторю!"
    )
    bot.reply_to(message, help_text)


# Обработчик команды /caps (правильная версия)
@bot.message_handler(commands=['caps'])
def send_caps(message):
    msg = message.text[6:].strip()  # Пропускаем "/caps " (6 символов)
    if msg:
        bot.reply_to(message, msg.upper())
    else:
        bot.reply_to(message, "Пожалуйста, введите текст после /caps")


# Эхо-режим: обработка любого текста, не попавшего под другие команды
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_message = message.text.strip()
    if 'привет' in user_message.lower():
        bot.reply_to(
            message,
            "Привет! Рад тебя видеть! Чем могу помочь?\n/help — показать эту справку"
        )
    else:
        bot.reply_to(message, user_message)


# Обработчик кнопки "О нас"
@bot.message_handler(func=lambda message: message.text == "О нас")
def about_us(message):
    bot.send_message(
        message.chat.id,
        "🤖 Я — учебный бот, созданный студентами!\n"
        "Цель: научиться программировать и делать полезные вещи."
    )


# Запуск бота
if __name__ == '__main__':
    print("✅ Бот запущен! Нажмите Ctrl+C, чтобы остановить.")
    bot.infinity_polling()
