from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, FSInputFile, WebAppInfo
from aiogram import Router, Bot
from config import BOT_TOKEN
import requests
bot = Bot(token=BOT_TOKEN)

command_router = Router()

session = requests.Session()

def url_maker(telegram_id, username, first_name, avatar):
    web_app_url = f"https://blumazizbek.netlify.app/?telegram_id={telegram_id}&username={username}&first_name={first_name}&avatar={avatar}"
    return web_app_url

msg = "Welcome to Blum! 🎉🎉🎉nnAt Blum, we are building a decentralized exchange in Telegram, specializing in trading memecoins and new tokens. We feature a unique memepad for launching new meme-based projects and incorporate gamified mechanics to enhance user engagement.nnHere’s what you can do with Blum now:n💯 Farm Blum Points: Play our Drop game to earn Blum Points (BPs) 🧑 Invite Friends: Bring your friends and family for more BPs! More friends = more BPsn🥊 Complete Quests: Finish tasks to rack up even more BPs!nnStart farming points now, and who knows what cool stuff you'll snag withthem soon! 🚀nnStay Blum! 🌟"

@command_router.message(CommandStart())
async def start_handler(message: Message):
    
    params = message.text[10:]
    if params:
        authenticate_response = session.post('https://azizbekaliyev.uz/api/v1/authenticate/enter/', json={
            "telegram_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "avatar": "dsnadlnas.jpg"
        })
        
        # Check the response
        if authenticate_response.status_code == 200:
            print("Authentication successful")
        else:
            print(f"Failed to authenticate. Status code: {authenticate_response.status_code}")

        data = requests.post(f"https://azizbekaliyev.uz/api/v1/authenticate/invite/{params}/{message.from_user.id}/")

        if data.status_code == 201:
            print("successfully_invited")
        else:
            print("User already invited.")

    user_photos = await bot.get_user_profile_photos(message.from_user.id)

    if user_photos.total_count > 0:
        file_id = user_photos.photos[0][-1]
    else:
        file_id = "default_avatar_file_id"  # Replace with a default file_id if needed

    # Create URL with profile information
    url = url_maker(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        avatar=file_id
    )

    # Create InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Launch Blum", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text="Join Community", url="https://t.me/azizbek_channnel")]
    ])

    photo = FSInputFile(path="blum.jpg")
    await message.answer_photo(
        photo=photo,
        caption=msg,
        reply_markup=keyboard
    )
