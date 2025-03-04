import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
import aiohttp

TOKEN = "8192351806:AAFHa5ks04YlHX5k3F3DBCXkNQJCpmKFu2o"

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

async def download_tiktok_video(url: str):
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

@dp.message(F.text.startswith("/start"))
async def send_welcome(message: Message):
    await message.reply("Salom! TikTok videolarini yuklab olish uchun menga video havolasini yuboring.")

@dp.message(F.text.contains("tiktok.com"))
async def tiktok_download(message: Message):
    await message.reply("⏳ Yuklab olinmoqda, iltimos kuting...")
    video_url = await download_tiktok_video(message.text)
    if video_url:
        await message.reply_video(video_url, caption="✅ Mana video!")
    else:
        await message.reply("❌ Video yuklab olinmadi. URL to'g'ri ekanligini tekshiring!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
