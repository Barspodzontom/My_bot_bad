from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.weather_button import keyboard
from dop_prog.weather import meteo


# Инициализируем роутер уровня модуля
router = Router()

@router.message(Command('pogoda'))
async def process_weather(message: Message):
    await message.answer(
        text='Узнай погоду!',
        reply_markup=keyboard
    )

@router.callback_query(F.data == 'погода')
async def process_weather(callback: CallbackQuery):
    await callback.message.edit_text(
        text=meteo(),
        reply_markup=callback.message.reply_markup,
    )
    await callback.answer(text='Ознакомься с погодой!',
        show_alert=True,
        reply_markup=None)
