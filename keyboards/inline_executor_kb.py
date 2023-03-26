from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .inline_client_kb import make_new_order_btn


get_my_stats_btn = InlineKeyboardButton(text = "Моя статистика",
                                 callback_data='/get_my_stats')

take_offer_btn = InlineKeyboardButton(text="Взять заказ", callback_data='/take_offer')
offer_your_price_btn = InlineKeyboardButton(text="Предложить свою цену", callback_data='/offer_your_price')
cancel_offer_btn = InlineKeyboardButton(text="Отклонить", callback_data='/cancel_offer')

executor_purpose = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            make_new_order_btn
        ],
        [
            get_my_stats_btn
        ]
    ]
)

executor_order_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            take_offer_btn
        ],
        [
            offer_your_price_btn
        ],
        [
            cancel_offer_btn
        ]
    ]
)