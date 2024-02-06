import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from db import create_database, add_user_wallet, get_user_wallets, delete_user_wallet

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
dp = Dispatcher()


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
    wallet_address = wallet_info[0] # Получаем адрес кошелька.

    if await add_user_wallet(user_id, wallet_address): # Создаём или получаем объект.
        await message.answer(f"Криптокошелёк с адресом '{wallet_info[0]}' был успешно добавлен.")
    else:
        await message.answer(f"Криптокошелёк с адресом '{wallet_info[0]}' уже существует.")


@dp.message(Command("wallets"))
async def wallets(message: types.Message):
    """Функция для отображение кошельков пользователя."""

    user_id = message.from_user.id # Получаем ID пользователя.
    wallets = await get_user_wallets(user_id) # Получаем кошельки пользователя.

    if not wallets:
        await message.answer("У вас пока нет ни одного криптокошелька.")
        return

    text = "Ваши кошельки: \n"
    for wallet in wallets: # Перебираем кошельки пользователя.
        text += f"{wallet.wallet_address} \n"

    await message.answer(text)


@dp.message(Command("delete_wallet"))
async def delete_wallet(message: types.Message):
    """Функция для удаления кошелька."""

    user_id = message.from_user.id # Получаем ID пользователя.
    args = message.text.split()[1:] # Разбираем сообщение.

    if not args:
        await message.answer("Вы не указали адрес кошелька для удаления.")
        return

    wallet_address = args[0] # Получаем адрес кошелька.

    deleted = await delete_user_wallet(user_id, wallet_address) # Пытаемся удалить кошелёк.

    if deleted:
        await message.answer(f"Криптокошелёк с адресом '{wallet_address}' был успешно удалён.")
    else:
        await message.answer(f"Криптокошелёк с адресом '{wallet_address}' не найден.")


async def main() -> None:
    """Функция запускает бота."""

    bot = Bot(TOKEN)
    await create_database()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    print('Бот начал работу.')
    asyncio.run(main())
