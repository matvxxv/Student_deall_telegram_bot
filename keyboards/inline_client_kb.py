from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


register_button = InlineKeyboardMarkup(
    inline_keyboard = [
        [
        InlineKeyboardButton(text = "Регистрация", callback_data='/register_user')
        ]
    ]
)

make_new_order_btn =  InlineKeyboardButton(text = "Хочу сделать заказ",
                                 callback_data='/make_new_order')

create_new_executor_btn =  InlineKeyboardButton(text="Хочу стать исполнителем",
                                 callback_data='/create_new_executor')

give_time_to_think_btn =  InlineKeyboardButton(text="Пока подумаю...",
                                 callback_data='/give_time_to_think')


user_purpose = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            make_new_order_btn
        ],
        [
            create_new_executor_btn
        ],
        [
           give_time_to_think_btn
        ]
    ]
)

