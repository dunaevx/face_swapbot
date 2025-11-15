from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Кнопка открыть WebApp."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть приложение",
            web_app={"url": config.webapp_url}
        )]
    ])
    return keyboard


def get_templates_keyboard() -> InlineKeyboardMarkup:
    """Выбор шаблонов (референсы GIF)."""
    templates = ["template1", "template2", "template3"]
    
    # Создаём кнопки с правильными индексами
    buttons = []
    for i, template_id in enumerate(templates, start=1):
        button = InlineKeyboardButton(
            text=f"Шаблон {i}",
            callback_data=f"template_{template_id}"
        )
        buttons.append(button)
    
    # Разбиваем по 2 в ряд
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[:2],      # Шаблон 1, Шаблон 2
        buttons[2:]       # Шаблон 3
    ])
    return keyboard