from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import MenuButtonWebApp, WebAppInfo

from utils.messages import *
from keyboards.user_keyboards import *
from utils.configs import FEEDBACK_CHANNEL
from states.feedback_states import FeedbackStatesGroup
from states.main_menu_states import MainMenuStatesGroup
from states.registration_states import RegistrationStatesGroup
from utils.funcs import check_user_registered, register_user, create_feedback

user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    user_exists = await check_user_registered(telegram_id)
    if user_exists:
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
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    user_exists = await check_user_registered(telegram_id)
    if user_exists:
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>{messages['message_7']}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=generate_main_menu_buttons()
        )

        await bot.set_chat_menu_button(
            chat_id=message.from_user.id,
            menu_button=MenuButtonWebApp(
                text="📱 Ilova",
                web_app=WebAppInfo(url="https://127.0.0.1:8000/")
            )
        )

        await state.set_state(MainMenuStatesGroup.main_menu)


# =====================================================================================================================

@user_router.message(MainMenuStatesGroup.main_menu)
async def handle_main_menu(message: Message, bot: Bot,
                           state: FSMContext):
    chat_id = message.chat.id
    handlers = {
        "📍 Manzil": show_address,
        "📞 Bog'lanish": show_contacts,
        "✍️ Fikr bildirish": ask_for_feedback,
        "ℹ️ Info": send_info_about_bot
    }

    handler = handlers.get(message.text)
    if handler:
        await handler(message, bot, state)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>{messages['message_7']}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
# =====================================================================================================================
async def show_address(message: Message, bot: Bot,
                       state: FSMContext):

    await bot.send_message(
        chat_id=message.chat.id,
        text=generate_address_text(),
        parse_mode=ParseMode.HTML
    )
# =====================================================================================================================


async def show_contacts(message: Message, bot: Bot,
                        state: FSMContext):
    pass
    # Контактная информация жонатиш кере
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text=generate_contacts_text(),
    #     parse_mode=ParseMode.HTML
    # )

# =====================================================================================================================

async def ask_for_feedback(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>{messages['message_9']}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=generate_back_button()
    )
    await state.set_state(FeedbackStatesGroup.ask_feedback)


@user_router.message(FeedbackStatesGroup.ask_feedback)
async def get_feedback(message: Message, bot: Bot, state: FSMContext):
    telegram_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь
    user_check = await check_user_registered(telegram_id)

    if not user_check.get('exists'):
        # Если пользователь не зарегистрирован
        await bot.send_message(
            chat_id=message.chat.id,
            text="<b>❌ Siz ro'yxatdan o'tmagansiz.\nRo'yxatdan o'tish uchun /start bosing.</b>",
            parse_mode=ParseMode.HTML
        )
        await state.clear()
        return

    # Если пользователь зарегистрирован
    if message.text == "⬅ Ortga":
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>{messages['message_10']}</b>",
            parse_mode=ParseMode.HTML
        )
        await show_main_menu(message, bot, state)
    else:
        # Создаем отзыв через API
        result = await create_feedback(telegram_id, message.text)

        if 'error' in result:
            # Если произошла ошибка при создании отзыва
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>❌ Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.</b>",
                parse_mode=ParseMode.HTML
            )
            await state.clear()
            return

        # Отправляем в канал
        try:
            feedback_message = generate_feedback_message(result)
            await bot.send_message(
                chat_id=FEEDBACK_CHANNEL,
                text=feedback_message,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            print(f"Ошибка при отправке в канал: {e}")

        # Подтверждение пользователю
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>{messages['message_10']}</b>",
            parse_mode=ParseMode.HTML
        )

        await show_main_menu(message, bot, state)

# =====================================================================================================================

async def send_info_about_bot(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=generate_info_text(),
        parse_mode=ParseMode.HTML
    )


# =====================================================================================================================
