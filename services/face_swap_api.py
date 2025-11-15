import aiohttp
from typing import Optional
import asyncio

class FaceSwapClient:
    def __init__(self, session: aiohttp.ClientSession, api_url: str, api_key: str = ""):
        self.session = session
        self.api_url = api_url
        self.api_key = api_key

    async def process_gif(self, photo_bytes: bytes, template_id: str) -> Optional[bytes]:
        """Обработка face-swap: отправка фото + шаблон в API."""
        try:
            data = aiohttp.FormData()
            data.add_field('photo', photo_bytes, filename='photo.jpg', content_type='image/jpeg')
            data.add_field('template', template_id)

            if self.api_key:
                data.add_field('key', self.api_key)

            async with asyncio.timeout(30):  # Таймаут 30с
                async with self.session.post(self.api_url, data=data) as resp:
                    if resp.status == 200:
                        return await resp.read()
                    else:
                        raise ValueError(f"API error: {resp.status}")
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
            print(f"API error: {e}")  # Лог
            return None  # Fallback

    async def close(self):
        """Закрытие сессии."""
        await self.session.close()