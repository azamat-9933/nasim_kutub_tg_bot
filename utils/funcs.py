import aiohttp
API_URL = "http://127.0.0.1:8000/tg_bot/api"
WEBAPP_URL = "https://your-webapp-url.com"



async def check_user_registered(telegram_id: int) -> dict:
    """Проверяет, зарегистрирован ли пользователь в БД"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/check-user/{telegram_id}/") as response:
                if response.status == 200:
                    return await response.json()
                return {'exists': False}
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return {'exists': False}


async def register_user(user_data: dict) -> bool:
    """Регистрирует нового пользователя"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/telegram/user/create/",
                json=user_data,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 201:
                    return True
                else:
                    error_text = await response.text()
                    print(f"Ошибка регистрации ({response.status}): {error_text}")
                    return False
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        return False
