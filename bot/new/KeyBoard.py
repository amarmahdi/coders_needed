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

    def finish(self):
        keyboard_finish = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        finish = types.KeyboardButton(text="Finish")
        keyboard_finish.add(finish)
        return keyboard_finish

    def BackToMainMenu(self):
        keyboard_back = types.ReplayKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        BackToMenu = types.KeyboardButton(text="Back to main menu")
        keyboard_back.add(BackToMenu)
        return keyboard_back
