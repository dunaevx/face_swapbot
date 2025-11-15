from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import io
from bot.keyboards.inline import get_start_keyboard, get_templates_keyboard
from services.face_swap_api import FaceSwapClient
from db import get_or_create_user, save_history
from asyncpg import Pool  # <-- ЭТОТ ИМПОРТ БЫЛ ПРОПУЩЕН!

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, pool: Pool):
    """Старт бота."""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    await get_or_create_user(pool, user_id, username, first_name)
    await message.answer(
        "Привет! Отправь фото или GIF для face-swap, или открой приложение.",
        reply_markup=get_start_keyboard()
    )

@router.message(F.photo | F.animation)
async def process_media(message: Message, pool: Pool, api_client: FaceSwapClient):
    """Обработка фото/GIF из чата."""
    user_id = message.from_user.id
    await get_or_create_user(pool, user_id, message.from_user.username, message.from_user.first_name)
    
    file = message.photo[-1] if message.photo else message.animation  # Последнее фото или animation
    file_id = file.file_id
    
    # Скачиваем файл
    file_info = await message.bot.get_file(file_id)
    file_bytes = await message.bot.download_file(file_info.file_path)
    
    await message.answer("Фото/GIF получено, выполняю обработку...")
    
    # Показываем выбор шаблонов
    await message.answer("Выбери шаблон:", reply_markup=get_templates_keyboard())
    
    # Здесь в реальности используй FSM для хранения file_bytes и user_id, но для простоты — callback ниже

@router.callback_query(F.data.startswith("template_"))
async def process_template(callback: CallbackQuery, pool: Pool, api_client: FaceSwapClient):
    """Обработка выбора шаблона."""
    template_id = callback.data.split("_")[1]
    # Получаем file_bytes из контекста (в проде — FSMContext)
    # Заглушка: assume file_bytes from previous
    file_bytes = b'dummy_photo_bytes'  # Замени на реальные из FSM
    
    await callback.message.edit_text("Обработка...")
    
    processed = await api_client.process_gif(file_bytes, template_id)
    if processed:
        processed_io = io.BytesIO(processed)
        processed_io.name = "processed.gif"
        await callback.message.answer_video(processed_io, caption="Готово!")
        await save_history(pool, callback.from_user.id, "original_id", "processed_id", template_id)
    else:
        await callback.message.answer("Ошибка обработки, попробуйте позже.")
    
    await callback.answer()