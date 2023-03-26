# import logging

from aiogram import types, Dispatcher

from keyboards.inline_client_kb import register_button, user_purpose
from keyboards.inline_executor_kb import executor_purpose

from database.DML.db_executor import new_executor, is_user_executor, get_executor_stats
from database.DML.db_client import register_user, is_user_in_db

from .create_order import cmd_make_new_order

async def command_start(message: types.Message):
    user_in_db = await is_user_in_db(message)
    user_is_executor = await is_user_executor(message)
    if not user_in_db:
        await message.answer('<b>Привет!</b>\nЕсли хочешь стать исполнителем или заказать работу, то сначала нужно зарегистрироваться &#128579;\n\n'
                         'Просто нажми на кнопку... &#128071;', reply_markup=register_button)
    else:
        await message.answer('<b>Снова здравствуйте!</b>\n\nЧего хочешь?',
                             reply_markup=user_purpose if not user_is_executor else executor_purpose)


async def register_user_handler(call: types.CallbackQuery):
    await register_user(call)

async def new_executor_handler(call: types.CallbackQuery):
    await new_executor(call)

async def time_to_think_handler(call: types.CallbackQuery):
    await call.message.answer('<b>Без проблем</b>\n\nЕсли надумаешь, возвращайся!')

async def get_my_stats_handler(call: types.CallbackQuery):
    await get_executor_stats(call)

async def take_offer_handler(call: types.CallbackQuery):
    await call.message.answer('Вы взяли задачу!')

async def offer_your_price(call: types.CallbackQuery):
    await call.message.answer('Предложите свою цену')

async def cancel_offer_handler(call: types.CallbackQuery):
    await call.message.answer('Вы отклонили предложение')




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_callback_query_handler(register_user, text='/register_user')
    dp.register_callback_query_handler(new_executor_handler, text='/create_new_executor')
    dp.register_callback_query_handler(time_to_think_handler, text='/give_time_to_think')
    dp.register_callback_query_handler(get_my_stats_handler, text='/get_my_stats')
    dp.register_callback_query_handler(take_offer_handler, text='/take_offer')