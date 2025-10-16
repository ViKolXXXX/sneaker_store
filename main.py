# Нужно написать бота для магазина кроссовок.
# Сторона юзера:
# Выбор категории, выбор товара, добавление в корзину. После выбора товара из списка открывается карточка с фото, ценой
# и размерами. На категории и товаре пагинация.
# Сторона админа:
# Добавление категорий и товаров.

import asyncio
import logging
from database.db import Database
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from keyboards.menu_commands import set_main_menu
from handlers import user, admin

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Задаём базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Инициализируем объект хранилища
    db = Database(config.db.name)
    logger.info(f"База данных '{config.db.name}' инициализирована.")

    # Помещаем нужные объекты в workflow_data диспетчера
    dp.workflow_data.update(db=db)

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры
    logger.info('Подключаем роутеры')
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())