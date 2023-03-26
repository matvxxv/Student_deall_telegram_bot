from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message


class RegisterCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]

    ) -> Any:
        print('Hello from Middleware')
        # db_session = event.bot.get('db')
        # async with db_session() as session:
        #     session: AsyncSession
        #     result = await session.execute(select(User).where(User.user_id == event.from_user.id))
        #     user = result.one_or_none()
        #     if user:
        #         user = await session.get(User, event.from_user.id)
        #         await event.answer(f'Вы в базе, дата регистрации \n {user.reg_date}')
        #     else:
        #         # try:
        #         await session.merge(User(
        #             user_id=event.from_user.id,
        #             username=event.from_user.username
        #         ))
        #         # except:
        #         #     await session.rollback()
        #         await session.commit()
        #         await event.answer(f'Вы успешно зареганы')


        return await handler(event, data)
