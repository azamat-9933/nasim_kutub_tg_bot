from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def generate_send_contact_button():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Kontaktni jo'natish 📲", request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def generate_submitting_keyboards():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Tasdiqlash ✅")
    builder.button(text="Bekor qilish ❌")

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)