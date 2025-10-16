import types
from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from database.db import Database
from keyboards.sneaker_store_kb import create_inline_kb
from lexicon.lexicon_ru import LEXICON, ADMIN_PANEL_KB, SHOP_KB

router = Router()


# Этот хэндлер будет срабатывать на кнопку "Админ-панель"
@router.callback_query(F.data == 'admin_panel')
async def process_admin_panel(callback: CallbackQuery):
    admin_panel_kb = create_inline_kb(2, **ADMIN_PANEL_KB)
    await callback.message.edit_text(
        text=LEXICON["admin_panel"],
        reply_markup=admin_panel_kb
    )

# Этот хэндлер будет срабатывать на кнопку "Назад"
@router.callback_query(F.data == 'back_to_shop')
async def process_back_to_shop(callback: CallbackQuery):
    shop_kb = create_inline_kb(2, **SHOP_KB)
    await callback.message.edit_text(
        text=LEXICON["main_menu"],
        reply_markup=shop_kb
    )

# Этот хэндлер будет срабатывать на кнопку "➕ Добавить категорию"
@router.callback_query(F.data == 'add_category')
async def process_add_category(callback: CallbackQuery):
    add_category_cancel_kb = create_inline_kb(2, 'add_category_cancel_kb')
    await callback.message.edit_text(
        text=LEXICON['add_category'],
        reply_markup=add_category_cancel_kb
    )

# Этот хэндлер будет срабатывать на кнопку "Отмена" при добавлении категории
@router.callback_query(F.data == 'add_category_cancel_kb')
async def process_add_category_cancel(callback: CallbackQuery):
    admin_panel_kb = create_inline_kb(2, **ADMIN_PANEL_KB)
    await callback.message.edit_text(
        text=LEXICON["admin_panel"],
        reply_markup=admin_panel_kb
    )

# Этот хэндлер будет срабатывать на сохранении новой категории
# добавлять категорию в базу данных
@router.message()
async def process_save_category(message: Message, db:Database):
    category_name = message.text.strip()

    all_categories_name = [row[1] for row in db.get_all_categories()]
    # Проверка на существование категории
    if category_name in all_categories_name:
        await message.answer("Такая категория уже существует!",
                             reply_markup=create_inline_kb(2, **ADMIN_PANEL_KB)
                             )
        return
    # Сохранение категории
    if db.add_category(category_name):
        await message.answer(
            f"Категория '{category_name}' успешно добавлена! ✅",
            reply_markup=create_inline_kb(2, **ADMIN_PANEL_KB)
        )
    else:
        await message.answer("Произошла ошибка при добавлении категории.")

# Этот хэндлер будет срабатывать на сохранении товара
@router.callback_query(F.data == 'add_product')
async def process_save_product(callback: CallbackQuery, db:Database):
   pass

