import asyncio
import logging
import os
import re
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Bot tokenni olish
TOKEN = os.getenv("BOT_TOKEN")  # Muhitdan token olish
if not TOKEN:
    raise ValueError("BOT_TOKEN muhit o‘zgaruvchisi topilmadi!")

# Logging sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher()

# TikTok havolalarini tekshirish regexi
TIKTOK_REGEX = r"(https?://(?:www\.)?tiktok\.com/\S+)"

# /start komandasi
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("👋 Assalomu alaykum!\n\nTikTok videolarini yuklash uchun havolani yuboring.")

# TikTok video yuklab beruvchi funksiya
async def download_tiktok_video(url: str):
    api_url = f"https://ssstik.io/api/ajax/search"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"url": url, "locale": "en"}

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=data) as response:
            if response.status == 200:
                json_response = await response.json()
                if "video_url" in json_response:
                    return json_response["video_url"]
            return None

# TikTok havolalarini qabul qilish
@dp.message()
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
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

# Kodni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
