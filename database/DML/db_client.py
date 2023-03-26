from typing import Union

from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.inline_client_kb import user_purpose

from database.models import User

async def register_user(event: Union[types.Message ,types.CallbackQuery]):
    '''
    Function adds user in Tabel 'users'

    :param event: Message or CallBackQuery from user
    :return: None
    '''

    db_session = event.bot.get('db')
    async with db_session() as session:
        session: AsyncSession
        result = await session.execute(select(User).where(User.user_id == event.from_user.id))
        user = result.one_or_none()
        if user:
            user = await session.get(User, event.from_user.id)
            await event.answer(f'Вы в базе, дата регистрации \n {user.reg_date}')
        else:
            await session.merge(User(
                user_id=event.from_user.id,
                username=event.from_user.username
            ))
            await session.commit()
            await event.message.answer(f'Вы успешно зареганы', reply_markup=user_purpose)


# Проверка наличия пользователя в БД
async def is_user_in_db(event: Union[types.Message, types.CallbackQuery]):
    '''
    :param event: Message or CallBackQuery from user
    :return: True if user is in Table 'users' else False
    '''

    db_session = event.bot.get('db')
    async with db_session() as session:
        session: AsyncSession
        user = await session.execute(select(User).where(User.user_id == event.from_user.id))
        result = user.one_or_none()
        return result