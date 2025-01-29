import os
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from dotenv import load_dotenv

load_dotenv() # Загрузка переменных из .env
STATISTICS_FILE = 'statistics.json' # Путь к файлу статистики

# Загрузка статистики из файла
def load_statistics():
    if os.path.exists(STATISTICS_FILE):
        with open(STATISTICS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

# Сохранение статистики в файл
def save_statistics(statistics):
    if os.path.exists(STATISTICS_FILE):
        with open(STATISTICS_FILE, 'w', encoding='utf-8') as file:
            json.dump(statistics, file, indent=4, ensure_ascii=False)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'),  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcom(message: types.Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nЯ буду повторять за тобой.')

# Обработчик команды /stats
@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = str(message.from_user.id)
    statistics = load_statistics() # Загрузка статистики из файла

    if user_id in statistics:
        await message.answer(f"Вы отправили {statistics[user_id]['messages_count']} сообщений.")
    else:
        await message.answer('Вы ещё не отправляли сообщений.')

# Обработчик текстовых сообщений
@dp.message()
async def send_echo(message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    text = message.text
    try:
        statistics = load_statistics()
    except json.JSONDecodeError as e:
        statistics = {}

    # Обновление статистики
    if user_id not in statistics:
        statistics[user_id] = {"username": username, "messages_count": 0}
    statistics[user_id]["messages_count"] += 1
    save_statistics(statistics)

    # Фильтр сообщений
    if "привет" in text.lower():
        await message.answer("Приветствую! Чем могу помочь?")
    elif "как дела?" in text.lower():
        await message.answer('Извините, я пока не умею отвечать на такие вопросы.')
    elif "помощь" in text.lower():
        await message.answer("Я эхо-бот, умею повторять сообщения и имею команду /stats для проверки количества отправленных сообщений.")
    else:
        await message.answer(text)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())