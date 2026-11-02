# Portfolio Bot

Telegram-бот с мини-приложением (TMA) — интерактивное портфолио разработчика.
Сам бот и приложение являются демонстрацией навыков автора.

## Стек
- **Bot:** Python 3.11+, aiogram 3, python-dotenv
- **Mini App:** чистый HTML/CSS/JS, без сборки

## Запуск
1. `pip install -r requirements.txt`
2. Заполнить `.env` (BOT_TOKEN, WEBAPP_URL, CONTACT_URL)
3. `python bot.py`

## Мини-приложение
Хостится на GitHub Pages из папки `webapp/`. Ссылку вписать в `.env`.
