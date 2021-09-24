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

    def check(self):
        keyboard_check = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        check = types.KeyboardButton(text="Check")
        keyboard_check.add(check)
        return keyboard_check

    def BackToMainMenu(self):
        keyboard_back = types.ReplayKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        BackToMenu = types.KeyboardButton(text="Back to main menu")
        keyboard_back.add(BackToMenu)
        return keyboard_back

    def skip(self):
        keyboard_skip = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        skip = types.KeyboardButton(text="Skip")
        prev = types.KeyboardButton(text="Previous")
        keyboard_skip.add(prev, skip)
        return keyboard_skip
