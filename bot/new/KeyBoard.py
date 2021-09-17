from aiogram import types


class KeyBoards:
    def __init__(self) -> None:
        pass

    def main(self):
        keyboard_main = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        add_company = types.KeyboardButton(text="Add Company")
        post_job = types.KeyboardButton(text="Post Job")
        keyboard_main.add(add_company, post_job)
        return keyboard_main
