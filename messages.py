messages = {
    "message_1": f"""Assalomu alaykum. Nasim Kutub nashriyoti onlayn do'koniga xush kelibsiz😊""",
    "message_2": f"""Siz ushbu bot imkoniyatlaridan foydalana olishingiz uchun ro'yxatdan o'tishingiz zarur 😄""",
    "message_3": f"""To'liq ismingizni yozing😄""",
    "message_4": f"""Telefon raqamingizni jo'nating: 😄""",
    "message_5": "❌ Ro'yxatdan o'tish bekor qilindi !",
    "message_6": "✅ Raxmat. Siz ro'yxatdan muvofaqqiyatli o'tdingiz !",
}



def generate_text_user_submitting_data(name, phone_number):
    text = f"""Ma'lumotlaringizni tasdiqlang:
Ism: {name}
Telefon raqam: {phone_number}"""

    return text