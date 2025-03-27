from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram import Router, F


fsm_router = Router(name=__name__)

#user_dict: dict[str, int | float] = {}


class Reg_Group(StatesGroup):

    latitude = State()  #широта
    longitude = State() #долгота
    #temperature = State() #температура
    #precipitation = State() #влажность
    #surface_pressure = State() #давление
    #wind_speed = State() #скорость ветра
    #wind_direction = State() #направление ветра
    #text = {'Reg_Group:latitude': 'Введите широту заново'}
    user_dict: dict[str, int | float] = {}

# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@fsm_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы вне машины состояний\n\n'
             'Чтобы перейти к прогнозу погоды - '
             'отправьте команду /weather'
    )

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@fsm_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к прогнозу погоды - '
             'отправьте команду /weather'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@fsm_router.message(Command(commands='назад'), StateFilter('*'))
async def of_process_cancel_command_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Reg_Group.latitude:
        await message.answer('Предыдущего шага нет. Нажмите "cancel" для выхода или продолжаййте вводить ваши координаты.')
        return
    previos = None
    for step in Reg_Group.__all_states__:
        if step.state == current_state:
            await state.set_state(previos)
            await message.answer(f'Вы вернулись к предыдущему шагу\n{Reg_Group.text[previos.state]}')
            return
        previos = step

@fsm_router.message(Command('weather'))
async def set_latitude(message: Message, state: FSMContext):
    await message.answer('Укажите широту: ')
    await state.set_state(Reg_Group.latitude)


@fsm_router.message(StateFilter(Reg_Group.latitude))
async def in_latitude(message: Message, state: FSMContext):
    await state.update_data(latitude=message.text)
    await message.answer("Отлично! Теперь укажите долготу:")
    await state.set_state(Reg_Group.longitude)



@fsm_router.message(StateFilter(Reg_Group.longitude))
async def set_longitude(message: Message, state: FSMContext):
    await state.update_data(longitude=message.text)
    Reg_Group.user_dict[message.from_user.id] = await state.get_data()
    data = await state.get_data()
    #await message.answer(str(data))
  
    Reg_Group.user_dict[message.from_user.id].update({
    "current": ["temperature_2m",
                 "is_day",
                   "precipitation",
                     "surface_pressure",
                       "wind_speed_10m",
                         "wind_direction_10m"],
    "forecast_days": 3,
    "hourly": "temperature_2m"}
  )
    await message.answer(str(data))

    await state.clear() 
    print(str(data))
#print(Reg_Group.__dict__)