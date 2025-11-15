from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from asyncpg import Pool

class DBMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        data["pool"] = self.pool
        return await handler(event, data)