from sqlalchemy import and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, select, DateTime, func
from pyrogram import Client, filters
from loguru import logger

from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TELEGRAM_ID = int(os.getenv("TELEGRAM_ID"))
PHOTO_PATH = "./photo/cat.png"
USERS_TASKS = {}

DATABASE_URL = "postgresql+asyncpg://user:pass123@db/dbname"
Base = declarative_base()

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String)
    username = Column(String)
    date_registered = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f"<User(id={self.id}, telegram_id={self.telegram_id}, "
                f"first_name={self.first_name}, username={self.username})>")


async def manage_tasks(client):
    while True:
        current_time = datetime.utcnow()
        for chat_id, task_info in list(USERS_TASKS.items()):
            time_passed = current_time - task_info['last_message_time']
            if 'next_task' not in task_info or task_info['next_task'] == '10min':
                if time_passed > timedelta(minutes=10):
                    await client.send_message(chat_id, "Добрый день!")
                    task_info['next_task'] = '90min'
            elif task_info['next_task'] == '90min':
                if time_passed > timedelta(minutes=90):
                    await client.send_message(chat_id, "Подготовила для ваc материал")
                    await client.send_photo(chat_id, photo=PHOTO_PATH, caption=None)
                    task_info['next_task'] = '120min'
            elif task_info['next_task'] == '120min':
                if time_passed > timedelta(minutes=120):
                    await client.send_message(chat_id, "Скоро вернусь с новым материалом!")
                    del USERS_TASKS[chat_id]
        await asyncio.sleep(5)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_message(filters.text & ~filters.bot &
                ~filters.chat(TELEGRAM_ID) &
                ~filters.user(TELEGRAM_ID))
async def handle_message(client, message):
    USERS_TASKS[message.chat.id] = {'last_message_time': datetime.utcnow(), 'next_task': '10min'}
    async with async_session() as session:
        user = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = user.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=message.from_user.id,
                first_name=message.from_user.first_name,
                username=message.from_user.username
            )
            session.add(user)
            await session.commit()
            logger.info(f"Новый пользователь добавлен: {user}")


@app.on_message(filters.command("users_today") &
                filters.chat(TELEGRAM_ID))
async def users_today(client, message):
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    if message.from_user.id == message.chat.id:
        async with async_session() as session:
            count = await session.execute(
                select(func.count()).where(
                    and_(
                        User.date_registered >= today,
                        User.date_registered < tomorrow
                    )
                )
            )
            count = count.scalar_one()

            await message.reply_text(f"Количество пользователей, зарегистрированных сегодня: {count}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables())
    loop.create_task(manage_tasks(app))
    app.run()
