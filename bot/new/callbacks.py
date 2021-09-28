from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

CPCallbackData = CallbackData('company', 'action', 'e_message')
ADCallbackData = CallbackData('admin', 'action')
AUCallbackData = CallbackData('user', 'action')
JADCallbackData = CallbackData('job', 'action')


class callBackBottons:
    def __init__(self) -> None:
        pass

    def CPbuttons(self, edit_msg):
        keyboard_cp = InlineKeyboardMarkup()
        keyboard_c = InlineKeyboardButton(
            text="Cancel", callback_data=CPCallbackData.new(action="Cancel", e_message='------Canceled------'))
        keyboard_p = InlineKeyboardButton(
            text="Proceed", callback_data=CPCallbackData.new(action="Proceed", e_message=edit_msg))
        keyboard_cp.row(keyboard_p, keyboard_c)
        return keyboard_cp

    def ADbuttons(self, edit_msg):
        keyboard_ad = InlineKeyboardMarkup()
        keyboard_a = InlineKeyboardButton(
            text="Accept", callback_data=ADCallbackData.new(action="Accept", e_msg=edit_msg))
        keyboard_d = InlineKeyboardButton(
            text="Deny", callback_data=ADCallbackData.new(action="Deny", e_msg=edit_msg))
        keyboard_ad.add(keyboard_a, keyboard_d)
        return keyboard_ad

    def ApproveUpload(self):
        keyboard_ad = InlineKeyboardMarkup()
        keyboard_a = InlineKeyboardButton(
            text="Save", callback_data=AUCallbackData.new(action="Save"))
        keyboard_d = InlineKeyboardButton(
            text="Cancel", callback_data=AUCallbackData.new(action="Cancel"))
        keyboard_ad.add(keyboard_a, keyboard_d)
        return keyboard_ad

    def JADbuttons(self):
        keyboard_ad = InlineKeyboardMarkup()
        keyboard_a = InlineKeyboardButton(
            text="Accept", callback_data=JADCallbackData.new(action="Accept"))
        keyboard_d = InlineKeyboardButton(
            text="Deny", callback_data=JADCallbackData.new(action="Deny"))
        keyboard_ad.add(keyboard_a, keyboard_d)
        return keyboard_ad
