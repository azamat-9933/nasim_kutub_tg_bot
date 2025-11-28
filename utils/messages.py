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
<b>Telefon:</b> +998 71 238 64 89

<b>E-mail:</b> info@tuit.uz

<b>Ish grafigi:</b> Dushanba - Juma 8:30 - 18:00
Shanba Yakshanba dam olish kuni"""

    return contact_text

def generate_address_text():
    contact_text = """<b>Manzil:</b> Toshkent 100084, Amir Temur shox ko'chasi 108 uy

<b>Jamoat transportlari:</b>
10, 17, 19, 24, 38, 51, 60, 67, 72, 93, 115, 140

<b>Ish grafigi:</b> Dushanba - Juma 8:30 - 18:00
Shanba Yakshanba dam olish kuni"""

    return contact_text


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

