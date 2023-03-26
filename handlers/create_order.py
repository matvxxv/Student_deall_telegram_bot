import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Order

from keyboards.inline_executor_kb import executor_order_kb

class FSMOrder(StatesGroup):
    subject = State()
    comment = State()
    price = State()
    photo = State()

async def cmd_make_new_order(call: types.CallbackQuery, state = FSMContext):
    await call.message.answer('<b>По какому предмету нужна помощь?</b>')

    await FSMOrder.subject.set()

async def subject_chosen(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text

    await message.answer('<b>Напиши комментарий, например:</b>\n\n'
                         'Нужно решить завтра в 12:00...\n'
                         'Нужна помощь с РК/экзаменом через 15 минут...')
    await FSMOrder.next()

async def set_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text

    await message.answer('<b>Установи свою цену:</b>')
    await FSMOrder.next()



async def set_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await message.answer('<b>Отправь фотографии с заданием, если они есть'
                         ' или примеры того, что ожидается в работе:</b>')
    await FSMOrder.next()


async def new_order_in_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        db_session = message.bot.get('db')
        async with db_session() as session:
            session: AsyncSession

            await session.merge(Order(
                order_id = 1,
                user_id = message.from_user.id,
                subject = data['subject'],
                price = data['price'],
                photo_id = data['photo'],
                comment = data['comment']
            ))

            await session.commit()
            await message.answer(f'Задача отправлена в чат исполнителей!\n\n'
                                     f'<b>Номер вашего заказа: {Order.order_id}</b>')

            message_to_chat = f"<b>Предмет:</b> {data['subject']}\n" \
                              f"<b>Прайс:</b> {data['price']}\n" \
                              f"<b>Описание:</b>\n{data['comment']}"

            await message.bot.send_photo(chat_id=os.environ.get("CHANEL_ID"), caption=message_to_chat, photo=data['photo'], reply_markup=executor_order_kb)

        await state.finish()

def register_order_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_make_new_order, text='/make_new_order')
    dp.register_message_handler(subject_chosen, state=FSMOrder.subject)
    dp.register_message_handler(set_comment, state=FSMOrder.comment)
    dp.register_message_handler(set_price, state=FSMOrder.price)
    dp.register_message_handler(new_order_in_db, content_types=['photo'],state=FSMOrder.photo)

