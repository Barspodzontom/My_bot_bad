from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from dop_prog.insult import insultik

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


#Этот хэндлер срабатывает на неизвестную команду или сообщение
@router.message()
async def process_unknown_command(message: Message):
    try:
        await message.reply(joke())
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])
