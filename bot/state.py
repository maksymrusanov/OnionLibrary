from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    book_title = State()
