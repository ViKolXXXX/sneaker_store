from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.sneaker_store_kb import create_inline_kb
from lexicon.lexicon_ru import LEXICON, SHOP_KB

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message, db):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in db.get_all_users():
        db.add_user(message.from_user.id)

# Этот хэндлер срабатывает на команду "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

# Этот хэндлер будет срабатывать на команду "/shop"
@router.message(Command(commands='shop'))
async def process_shop_command(message: Message):
    shop_kb = create_inline_kb(2, **SHOP_KB)
    await message.answer(
        text=LEXICON["main_menu"], reply_markup=shop_kb
    )


# Этот хэндлер будет срабатывать на кнопку "Корзина".
@router.callback_query(F.data == "cart")
async def process_shop_command(callback: CallbackQuery):
    await callback.message.edit_text("Вы открыли корзину!")
