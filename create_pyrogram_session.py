from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

with Client("my_account", api_id=API_ID, api_hash=API_HASH) as app:
    me = app.get_me()
    telegram_id = me.id
    with open(".env", "a") as env_file:
        env_file.write(f"\nTELEGRAM_ID={telegram_id}\n")
    # app.send_message(telegram_id, "Привет! Это ваша новая сессия Pyrogram.")
