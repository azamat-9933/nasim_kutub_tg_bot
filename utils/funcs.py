# utils/funcs.py
import aiohttp

API_URL = "http://127.0.0.1:8000/tg_bot/api"


async def get_user_info(telegram_id: int) -> dict:
    """Получает полную информацию о пользователе"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/user/{telegram_id}/") as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return {'error': 'Пользователь не найден'}
    except Exception as e:
        print(f"Ошибка: {e}")
        return {'error': str(e)}


async def check_user_registered(telegram_id: int) -> dict:
    """Проверяет регистрацию пользователя"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/check-user/{telegram_id}/") as response:
                if response.status == 200:
                    return await response.json()
                return {'exists': False}
    except Exception as e:
        print(f"Ошибка: {e}")
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


async def create_feedback(telegram_id: int, message_text: str) -> dict:
    """Создает отзыв через API"""
    try:
        async with aiohttp.ClientSession() as session:
            data = {
                'telegram_id': telegram_id,
                'message': message_text
            }
            async with session.post(
                f"{API_URL}/feedback/create/",
                json=data,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    return {'error': 'Ошибка при создании отзыва'}
    except Exception as e:
        print(f"Ошибка: {e}")
        return {'error': str(e)}