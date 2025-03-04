import asyncio
import logging
import os
import re
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage

# Bot tokenini olish
TOKEN = os.getenv("BOT_TOKEN")  # Muhitdan token olish
if not TOKEN:
    raise ValueError("BOT_TOKEN muhit o‘zgaruvchisi topilmadi!")

# Logging sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# TikTok havolalarini tekshirish regexi
TIKTOK_REGEX = r"(https?://(?:www\.)?tiktok\.com/\S+)"

# /start komandasi
@dp.message_handler(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "TikTok videolarini yuklash uchun havolani yuboring."
    )

# TikTok video yuklab beruvchi funksiya
async def download_tiktok_video(url: str):
    api_url = "https://api.tikmate.app/api/lookup"
    params = {"url": url}

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            if response.status == 200:
                json_response = await response.json()
                if "videoUrl" in json_response:
                    return json_response["videoUrl"]
            return None

# TikTok havolalarini qabul qilish
@dp.message_handler()
async def handle_tiktok_link(message: Message):
    match = re.search(TIKTOK_REGEX, message.text)
    if match:
        url = match.group(1)
        await message.answer("🔄 Yuklab olinmoqda, biroz kuting...")

        video_url = await download_tiktok_video(url)
        if video_url:
            await message.answer_video(video_url, caption="✅ TikTok videongiz tayyor!")
        else:
            await message.answer("❌ Xatolik: Videoni yuklab bo‘lmadi.")
    else:
        await message.answer("❌ Noto‘g‘ri havola. Iltimos, haqiqiy TikTok havolasini yuboring.")

# Asosiy ishga tushirish funksiyasi
async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Webhookni o‘chirish
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

# Kodni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
