import os
import asyncio
import uuid

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
dp = Dispatcher()

user_wallets = {}


@dp.message(CommandStart())
async def start(message: types.Message):
    """Обработчик команды /start."""

    await message.answer("Здравствуйте! Для регистрации необходимо добавить свой криптокошелек в сети TRON. \n"
                         "Пример: /add_wallet адрес_кошелька")


@dp.message(Command("add_wallet"))
async def add_wallet(message: types.Message):
    """Функция которая отвечает за добавление кошельков пользователя."""
    wallet_info = message.text.split()[1:] # Разбираем сообщение.

    # Проверяем, что сообщение содержит кошелёк. (Надо будет добавить проверку форматов)
    if not wallet_info:
        await message.answer("Неверный формат сообщения.\n"
                             "Используйте: /add_wallet адрес_кошелька")
        return

    # Проверяем, что пользователь передал только один кошелёк за раз.
    if len(wallet_info) != 1:
        await message.answer("Неверное количество аргументов. За раз можно добавить только один кошелёк. \n"
                             "Используйте: /add_wallet адрес_кошелька")
        return

    user_id = message.from_user.id # Получаем ID юзера.

    # Если юзер не был ранее зарегистрирован.
    if user_id not in user_wallets:
        user_wallets[user_id] = {}

    # Проверяет все адреса кошельков и если такой кошелёк уже был добавлен any() выдаёт False.
    if any(wallet_info[0] == wallet_data for wallet_data in user_wallets[user_id].values()):
        await message.answer(f"Кошелек с адресом '{wallet_info[0]}' уже был добавлен.")
        return

    # Генерируем уникальный идентификатор кошелька
    wallet_id = str(uuid.uuid4())[:8]

    user_wallets[user_id][wallet_id] = wallet_info[0] # Добавляем все данные в словарь.

    await message.answer(f"Крипто кошелёк с адресом '{wallet_info[0]}' был успешно добавлен. ID кошелька: {wallet_id}")


@dp.message(Command("wallets"))
async def wallets(message: types.Message):
    """Функция для отображение кошельков пользователя."""
    user_id = message.from_user.id # Получаем ID пользователя.
    wallets = user_wallets.get(user_id) # Получаем кошельки пользователя.

    if not wallets:
        await message.answer("У вас пока нет ни одного криптокошелька.")
        return

    text = "Ваши кошельки: \n"
    for id, address in wallets.items(): # Перебираем кошельки пользователя.
        text += f"{id} - {address} \n"

    await message.answer(text)


@dp.message(Command("delete_wallet"))
async def delete_wallet(message: types.Message):
    """Функция для удаления кошелька."""
    user_id = message.from_user.id # Получаем ID пользователя.
    wallets = user_wallets.get(user_id) # Получаем кошельки пользователя.

    if not wallets:
        await message.answer("У вас пока нет ни одного криптокошелька.")
        return


    args = message.text.split()[1:]

    if not args:
        await message.answer("Вы не указали ID для удаления кошелька.")
        return

    wallet_id = args[0]
    
    if wallet_id not in wallets:
        await message.answer(f"Кошелек с ID {wallet_id} не найден.")
        return
    
    wallet_on_delete = user_wallets[user_id][wallet_id] # Получаем кошелёк.

    # Удаляем кошелек с указанным ID
    del user_wallets[user_id][wallet_id]

    # Отправляем сообщение об успешном удалении кошелька
    await message.answer(f"Криптокошелёк ({wallet_on_delete}) был успешно удалён.") 


async def main() -> None:
    """Функция запускает бота."""
    bot = Bot(TOKEN)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    print('Бот начал работу.')
    asyncio.run(main())
