import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient('user_session', api_id, api_hash)

async def main():
    print("Starting Telegram Auth...")
    await client.start()
    print("✅ Login Successful! You now have a 'user_session.session' file.")
    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())