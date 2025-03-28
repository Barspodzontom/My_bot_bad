import asyncio as _asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

from handlers import command_insult_handlers, other_handlers, fsm_weather
from keyboards.set_menu import set_main_menu


# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await set_main_menu(bot)
    # Регистриуем роутеры в диспетчере
    dp.include_router(fsm_weather.fsm_router)
    dp.include_routers(other_handlers.router)
    dp.include_routers(command_insult_handlers.router)

    #await bot.delete_my_commands()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
try:
    _asyncio.run(main())
except KeyboardInterrupt:
    logger.info('Stopping bot')
