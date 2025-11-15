# bot/handlers/webapp.py
from aiogram import Router, F
from aiogram.types import Message
import json
import base64
import io
from db import get_or_create_user
from services.face_swap_api import FaceSwapClient
from asyncpg import Pool

router = Router()


@router.message(F.web_app_data)  # <-- ИСПРАВЛЕНО!
async def webapp_data_handler(message: Message, pool: Pool, api_client: FaceSwapClient):
    """Обработка данных из WebApp (JSON с photo base64, template_id)."""
    user_id = message.from_user.id
    await get_or_create_user(pool, user_id, message.from_user.username, message.from_user.first_name)

    try:
        data = json.loads(message.web_app_data.data)
    except (json.JSONDecodeError, AttributeError):
        await message.answer("Ошибка: неверные данные из приложения.")
        return

    photo_base64 = data.get("photo")
    template_id = data.get("template_id")

    if not photo_base64 or not template_id:
        await message.answer("Пожалуйста, выберите фото и шаблон.")
        return

    try:
        photo_bytes = base64.b64decode(photo_base64)
    except base64.BinasciiError:
        await message.answer("Ошибка: повреждённое изображение.")
        return

    await message.answer("Фото из приложения получено, выполняю обработку...")

    processed = await api_client.process_gif(photo_bytes, template_id)
    if processed:
        processed_io = io.BytesIO(processed)
        processed_io.name = "processed.gif"
        await message.answer_animation(processed_io, caption="Готово!")
        # TODO: save_history(pool, user_id, original_file_id, processed_file_id, template_id)
    else:
        await message.answer("Ошибка обработки, попробуйте позже.")