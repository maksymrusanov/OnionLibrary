from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ga = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="fb2", callback_data="fb2")],
        [InlineKeyboardButton(text="epub", callback_data="epub")],
        [InlineKeyboardButton(text="mobi", callback_data="mobi")],
    ]
)
