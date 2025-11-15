import asyncpg
from asyncpg import Pool
from typing import Optional
from datetime import datetime

async def init_db(pool: Pool) -> None:
    """Инициализация таблиц при запуске."""
    async with pool.acquire() as conn:
        # Таблица users
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY,
                username VARCHAR(255),
                first_name VARCHAR(255),
                first_use TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Таблица history (опционально)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(id),
                original_file_id VARCHAR(255),
                processed_file_id VARCHAR(255),
                template_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

async def get_or_create_user(pool: Pool, user_id: int, username: Optional[str], first_name: Optional[str]) -> int:
    """Получить или создать пользователя."""
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT id FROM users WHERE id = $1", user_id
        )
        if not user:
            await conn.execute(
                "INSERT INTO users (id, username, first_name) VALUES ($1, $2, $3)",
                user_id, username, first_name
            )
        return user_id

async def save_history(pool: Pool, user_id: int, original_file_id: str, processed_file_id: str, template_id: str) -> None:
    """Сохранить историю обработки."""
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO history (user_id, original_file_id, processed_file_id, template_id) VALUES ($1, $2, $3, $4)",
            user_id, original_file_id, processed_file_id, template_id
        )