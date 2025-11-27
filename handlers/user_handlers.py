from aiogram import F
from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from messages import *
from keyboards.user_keyboards import *
from utils.funcs import check_user_registered, register_user
from states.registration_states import RegistrationStatesGroup

user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    user_exists = await check_user_registered(telegram_id)
    if not user_exists:
        await show_main_menu(message, bot, state)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>{messages['message_1']}</b>",
            parse_mode=ParseMode.HTML,
        )
        await start_registration(message, bot, state)

async def start_registration(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id

    await bot.send_message(
        chat_id=chat_id,
        text=f"<b>{messages['message_2']}</b>",
        parse_mode=ParseMode.HTML,
    )
    await ask_user_full_name(message, bot, state)


async def ask_user_full_name(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id

    await bot.send_message(
        chat_id=chat_id,
        text=f"<b>{messages['message_3']}</b>",
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(RegistrationStatesGroup.wait_full_name)


@user_router.message(RegistrationStatesGroup.wait_full_name)
async def ask_user_phone_number(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id

    await state.update_data(full_name=message.text)

    await bot.send_message(
        chat_id=chat_id,
        text=f"<b>{messages['message_4']}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=generate_send_contact_button()
    )
    await state.set_state(RegistrationStatesGroup.wait_phone_number)

@user_router.message(RegistrationStatesGroup.wait_phone_number)
async def ask_for_submit(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number if message.content_type == "contact" else message.text
    await state.update_data(phone_number=phone_number)

    data = await state.get_data()

    await bot.send_message(
        chat_id=chat_id,
        text=f"<b>{generate_text_user_submitting_data(data['full_name'], data['phone_number'])}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=generate_submitting_keyboards()
    )
    await state.set_state(RegistrationStatesGroup.wait_for_submit)


@user_router.message(RegistrationStatesGroup.wait_for_submit)
async def submit_registration(message: Message, bot: Bot, state: FSMContext):
    telegram_id = message.from_user.id
    data = await state.get_data()

    if message.text == "Tasdiqlash ✅":
        await register_user(user_data={
            "telegram_id": telegram_id,
            "full_name": data['full_name'],
            "phone_number": data['phone_number'],
            "username": message.from_user.username if message.from_user.username else ""
        })

        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>{messages['message_6']}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        await show_main_menu(message, bot, state)

    elif message.text == "Bekor qilish ❌":
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>{messages['message_5']}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        await start(message, bot, state)




async def show_main_menu(message: Message, bot: Bot, state: FSMContext):
    pass
