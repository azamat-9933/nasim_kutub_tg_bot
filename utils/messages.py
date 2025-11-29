messages = {
    "message_1": f"""Assalomu alaykum. Nasim Kutub nashriyoti onlayn do'koniga xush kelibsiz😊""",
    "message_2": f"""Siz ushbu bot imkoniyatlaridan foydalana olishingiz uchun ro'yxatdan o'tishingiz zarur 😄""",
    "message_3": f"""To'liq ismingizni yozing😄""",
    "message_4": f"""Telefon raqamingizni jo'nating: 😄""",
    "message_5": "❌ Ro'yxatdan o'tish bekor qilindi !",
    "message_6": "✅ Raxmat. Siz ro'yxatdan muvofaqqiyatli o'tdingiz !",
    "message_7": " 🛍 Asosiy menyuga hush kelibsiz !",
    "message_8": "Iltimos, quyidagi tugmalardan birini tanlang: ",
    "message_9": "✍️ O'z fikringizni yozib qoldiring va biz siz bilan tezda qayta aloqaga chiqamiz ⁉",
    "message_10": "ℹ Siz asosiy menyuga qaytdingiz",
}



def generate_text_user_submitting_data(name, phone_number):
    text = f"""Ma'lumotlaringizni tasdiqlang:
Ism: {name}
Telefon raqam: {phone_number}"""

    return text


def generate_contacts_text():
    contact_text = """
<b>📞 Telefon:</b> +998 77 155 15 15

<b>📧 E-mail:</b> nasimkutub1@gmail.com

<b>🔔 Telegram kanal:</b> https://t.me/nasimkutub

<b>👨‍💻 Admin: https://t.me/nasimulgurji</b>"""

    return contact_text


def show_transports_text():
    transports_text = """
<b>Jamoat transportlari: </b>
<b>🚇 Metro:</b> <i>Chorsu -> 650m</i>
<b>🚇 Metro:</b> <i>G'ofur G'ulom -> 860m</i>
<b>🚌 Avtobus:</b> <i>8T, 11, 17, 23, 27, 28, 29, 32, 35, 43, 44, 46, 47, 53, 56, 64, 65, 68, 73, 76, 84, 89, 91, 100, 103, 109, 115, 118, 120, 123, 136, 146, 147, 152, 177, 188, 196, 472</i>
<b>🚐 Marshrutka:</b> <i>27m, 52m, 76m, 88m, 92m, 130m, 182m, 191m, 453</i>
"""
    return transports_text


def generate_feedback_message(feedback_data: dict) -> str:
    """Генерирует текст для отправки в канал"""
    fb = feedback_data['feedback']

    message = f"""
📝 <b>Yangi fikr-mulohaza</b>

🆔 <b>ID:</b> #{fb['id']}
👤 <b>Ism:</b> {fb['user_full_name']}
📱 <b>Telefon:</b> {fb['user_phone']}
"""

    if fb.get('user_username'):
        message += f"💬 <b>Username:</b> @{fb['user_username']}\n"

    message += f"""
💬 <b>Xabar:</b>
{fb['message']}

🕐 <b>Sana:</b> {fb['created_date']}
"""

    return message

def generate_info_text():
    return f"""<b>Ushbu telegram bot orqali siz Nasim Kutub nashriyotiga tegishli onlayn do'konimizga murojaat qilishingiz mumkin va kitoblarni onlayn harid qilishingiz mumkin. Buning uchun siz 📱 Ilova tugmasini bosing va sizda onlayn do'konimiz ochiladi !</b>

<b>👨🏻‍💻 Telegram bot yaratuvchisi bilan aloqa: https://t.me/azza_back_end_dev</b>"""