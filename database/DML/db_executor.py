from typing import Union

from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def new_executor(call: types.CallbackQuery):
    '''
    Function updates user's field 'is_executor' on True

    :param call: CallBackQuery from user
    :return: None
    '''
    db_session = call.bot.get('db')
    async with db_session() as session:
        session: AsyncSession
        user = await session.get(User, call.from_user.id)
        if user.is_executor == False:
            user.is_executor = True
            await session.commit()
            await call.message.answer('<b>Супер!</b>\nТеперь ты можешь выполнять заказы!\n'
                                      'Для начала работы вступи в закрытую группу исполнителей &#128071;')
        else:
            await call.message.answer('Вы уже являетсь исполнителем')

async def is_user_executor(event: Union[types.Message, types.CallbackQuery]):
    '''
    :param event: Message or CallBackQuery from user
    :return: True if user is executor else False
    '''
    db_session = event.bot.get('db')
    async with db_session() as session:
        session: AsyncSession
        user_executor = await session.execute(select(User).where((User.user_id == event.from_user.id) & (User.is_executor == True)))
        result = user_executor.one_or_none()
        return result

async def get_executor_stats(call: types.CallbackQuery):
    '''
    Send message to user with user's stats like 'completed_orders', 'rank', etc.
    :param call: CallBackQuery from user (is_executor is True)
    :return: None
    '''
    user_executor = await is_user_executor(call)
    if user_executor:
        db_session = call.bot.get('db')
        async with db_session() as session:
            session: AsyncSession
            user = await session.get(User, call.from_user.id)

            user_stats_str = f'Количество выполненных заказов: {user.completed_orders}\n' \
                             f'Количество отзывов: {user.feedback_num}\n' \
                             f'Рейтинг: {user.ranking} &#11088;\n' \
                             f'Получено денег: {user.total_cash_get}'

            await call.message.answer(user_stats_str)
    else:
        await call.message.answer('<b>Стоп стоп...</b>\nТы же не исполнитель')