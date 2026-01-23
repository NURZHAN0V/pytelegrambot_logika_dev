# pytelegrambot

Учебный проект: создание Telegram-ботов на Python с библиотекой pyTelegramBotAPI. Пошаговые задания для занятий.

---

## Требования

- Python 3.7+
- Токен бота от [@BotFather](https://t.me/BotFather)

---

## Быстрый старт

1. Клонируйте репозиторий и перейдите в папку проекта.
2. Создайте виртуальное окружение и активируйте его:
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
3. Установите зависимости:
   ```powershell
   pip install -r requirements.txt
   ```
4. Создайте файл `.env` с переменной `BOT_TOKEN=ваш_токен`.
5. Соберите бота по инструкции и запустите:
   ```powershell
   python main.py
   ```

Полное пошаговое руководство — в [tasks/day-1.md](tasks/day-1.md).

---

## Структура проекта

```
pytelegrambot/
├── .env              # токен (создать вручную, в .gitignore)
├── main.py           # код бота (создать по заданиям)
├── requirements.txt  # зависимости (создать по заданиям)
├── notes.json        # заметки (создаётся ботом, в .gitignore)
├── images/           # загруженные фото (создаётся ботом, в .gitignore)
├── tasks/
│   ├── day-1.md      # День 1: от нуля до команд, кнопок, фото и заметок
│   └── images/       # иллюстрации к заданиям
└── README.md
```

---

## tasks/day-1.md — День 1

Руководство «Первый бот за 2 часа»:

- Настройка проекта, `.env`, venv, `requirements.txt`
- Команды: `/start`, `/help`, `/caps`, эхо с условием
- Кнопки (`ReplyKeyboardMarkup`), обработчик «О нас»
- Приём и сохранение фото в `images/`
- Заметки: `/note`, `/notes`, сохранение в `notes.json`, `/save`
- Задание: бот-опросник `/quiz`

Рассчитано на начинающих (14+).

---

## Зависимости

В `requirements.txt` после выполнения Дня 1:

- `python-dotenv` — загрузка переменных из `.env`
- `pyTelegramBotAPI` — работа с Telegram Bot API
