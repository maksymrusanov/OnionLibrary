from parser import book_parser

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from .keyboard import ga
from .state import Form

router = Router()


@router.message(CommandStart())
async def get_book_title(message, state: FSMContext):
    await state.set_state(Form.book_title)
    await message.answer("Enter the book title:")


@router.message(Form.book_title, F.text)
async def get_data(message, state: FSMContext):
    await state.update_data(book_title=message.text)
    data = await state.get_data()
    book_title = data.get("book_title")
    res = book_parser.get_books(book_title)
    for i in res:
        await message.answer(
            f"Title: {i['title']}\nAuthor: {i['author']}", reply_markup=ga
        )
    await state.clear()


@router.callback_query(F.data == "fb2")
async def send_fb2(callback_query):
    await callback_query.answer("You chose fb2 format")


@router.callback_query(F.data == "epub")
async def send_epub(callback_query):
    await callback_query.answer("You chose epub format")


@router.callback_query(F.data == "mobi")
async def send_mobi(callback_query):
    await callback_query.answer("You chose mobi format")
