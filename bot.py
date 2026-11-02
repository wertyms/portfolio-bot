# -*- coding: utf-8 -*-
"""
Портфолио-бот: Telegram-бот с мини-приложением.
Сам бот и приложение — это и есть первое демо работ автора.
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    BotCommand,
    MenuButtonCommands,
)

# ---------------------------------------------------------------- настройки

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()
CONTACT_URL = os.getenv("CONTACT_URL", "https://t.me/username")

# Поменяй на своё — эти строки видит клиент
NAME = "Максим"             # как тебя называть
NICKNAME = "@max_avito_PT"  # твой ник в Telegram (для красоты в текстах)


# ---------------------------------------------------------------- клавиатуры

def main_keyboard() -> InlineKeyboardMarkup:
    """Главное меню бота."""
    rows = []

    # Кнопка мини-приложения работает, только если ссылка уже задана
    if WEBAPP_URL:
        rows.append([
            InlineKeyboardButton(
                text="🚀 Открыть портфолио",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ])

    rows.append([
        InlineKeyboardButton(text="👤 Обо мне", callback_data="about"),
        InlineKeyboardButton(text="🛠 Что я делаю", callback_data="services"),
    ])
    rows.append([
        InlineKeyboardButton(text="📩 Связаться", callback_data="contact"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
            [InlineKeyboardButton(text="📩 Связаться", callback_data="contact")],
        ]
    )


# ---------------------------------------------------------------- тексты

WELCOME = (
    f"Привет! 👋\n\n"
    f"Этот бот и приложение, которое сейчас откроется, я написал сам "
    f"с нуля — Python, JavaScript, Telegram API.\n\n"
    f"То есть <b>ты уже смотришь на пример моей работы</b>. "
    f"Никаких картинок-заглушек: всё, что нажимается и работает, — мой код.\n\n"
    f"Жми кнопку и смотри 👇"
)

ABOUT = (
    f"<b>👤 Обо мне</b>\n\n"
    f"Я {NAME} — начинающий разработчик ({NICKNAME}).\n\n"
    f"Делаю:\n"
    f"• Telegram-ботов — от простых до мини-приложений\n"
    f"• Мини-приложения (TMA) — сайты внутри Telegram\n"
    f"• Сайты и лендинги — быстрые, аккуратные\n"
    f"• ИИ-помощников — боты с подключённой нейросетью\n\n"
    f"Пишу на Python и JavaScript. Люблю чистый код "
    f"и показываю заказчику результат на каждом этапе — "
    f"ты всегда видишь, за что платишь."
)

SERVICES = (
    f"<b>🛠 Что я делаю и во сколько это примерно обойдётся</b>\n\n"
    f"1️⃣ <b>Telegram-бот</b> — анкеты, кнопки, база данных\n"
    f"от 1 500 ₽ · 1-3 дня\n\n"
    f"2️⃣ <b>Мини-приложение в Telegram</b> — как это, которое перед тобой\n"
    f"от 1 500 ₽ · 3-6 дней\n\n"
    f"3️⃣ <b>Сайт / лендинг</b> — визитка, портфолио, страница услуги\n"
    f"от 2 000 ₽ · 2-4 дня\n\n"
    f"4️⃣ <b>ИИ-помощник</b> — бот, который отвечает клиентам сам\n"
    f"от 2 000 ₽ · 2-5 дней\n\n"
    f"Точная цена — после того, как расскажешь задачу. "
    f"Это бесплатно и ни к чему не обязывает 😉"
)

CONTACT = (
    f"<b>📩 Связаться со мной</b>\n\n"
    f"Просто нажми кнопку ниже и напиши — отвечаю обычно "
    f"в течение часа.\n\n"
    f"Расскажи в двух словах:\n"
    f"• что нужно (бот / сайт / приложение)\n"
    f"• зачем и для кого\n"
    f"• к какому сроку\n\n"
    f"Дальше я предложу варианты и назову цену."
)


# ---------------------------------------------------------------- хендлеры

dp = Dispatcher()
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME, reply_markup=main_keyboard())


@dp.callback_query(F.data == "about")
async def show_about(call: CallbackQuery) -> None:
    await call.message.edit_text(ABOUT, reply_markup=back_keyboard())
    await call.answer()


@dp.callback_query(F.data == "services")
async def show_services(call: CallbackQuery) -> None:
    await call.message.edit_text(SERVICES, reply_markup=back_keyboard())
    await call.answer()


@dp.callback_query(F.data == "contact")
async def show_contact(call: CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Написать в Telegram", url=CONTACT_URL)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
    await call.message.edit_text(CONTENT := CONTACT, reply_markup=kb)
    await call.answer()


@dp.callback_query(F.data == "back")
async def go_back(call: CallbackQuery) -> None:
    await call.message.edit_text(WELCOME, reply_markup=main_keyboard())
    await call.answer()


# ---------------------------------------------------------------- запуск

async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    if not BOT_TOKEN:
        raise SystemExit("Нет токена: заполни файл .env (BOT_TOKEN=...)")
    if not WEBAPP_URL:
        logging.warning(
            "WEBAPP_URL пуст — кнопки мини-приложения не будет. "
            "Загрузи webapp/index.html на GitHub Pages и впиши ссылку в .env"
        )
    await bot.delete_webhook(drop_pending_updates=True)

    # Подсказки-кнопки над полем ввода (меню команд)
    await bot.set_my_commands([
        BotCommand(command="start", description="🚀 Открыть портфолио"),
    ])
    # Кнопка "Меню" слева от поля ввода
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
