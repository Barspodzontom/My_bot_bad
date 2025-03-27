from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_1 = InlineKeyboardButton(
    text='погода',
    callback_data='погода'
)

keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])