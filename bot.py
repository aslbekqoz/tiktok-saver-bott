import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import aiohttp
import os

TOKEN = os.getenv("BOT_TOKEN")  # Render ENV o‘zgaruvchilaridan token olish
CHAT_ID = os.getenv("CHAT_ID")  # Ping yuborish uchun chat ID

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

async def download_tiktok_video(url: str):
    """TikTok video yuklab olish funksiyasi"""
    api_url = "https://www.tikwm.com/api/"
    params = {"url": url}
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            if response.status != 200:
                return None
            data = await response.json()
            if data.get("data") and data["data"].get("play"):
                return data["data"]["play"]
            return None

@dp.message(CommandStart())
async def send_welcome(message: Message):
    """Start komandasi"""
    await message.reply("👋 Salom! TikTok videolarini yuklab olish uchun menga video havolasini yuboring.")

@dp.message(lambda message: "tiktok.com" in message.text)
async def tiktok_download(message: Message):
    """TikTok videolarini yuklab olish"""
    await message.reply("⏳ Yuklab olinmoqda, iltimos kuting...")
    video_url = await download_tiktok_video(message.text)
    if video_url:
        await message.reply_video(video_url, caption="✅ Mana video!")
    else:
        await message.reply("❌ Video yuklab olinmadi. URL to'g'ri ekanligini tekshiring!")

async def keep_alive():
    """Har 10 daqiqada botga ping yuborish (Render uchun)"""
    while True:
        await asyncio.sleep(600)  # 10 daqiqa (600 soniya)
        try:
            if CHAT_ID:
                await bot.send_message(chat_id=CHAT_ID, text="✅ Bot ishlayapti! (/ping)")
                logging.info("✅ Ping yuborildi!")
        except Exception as e:
            logging.error(f"❌ Ping yuborishda xatolik: {e}")

async def main():
    """Botni ishga tushirish"""
    asyncio.create_task(keep_alive())  # Ping tizimini ishga tushiramiz
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
