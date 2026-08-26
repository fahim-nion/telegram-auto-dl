import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

client = TelegramClient('user_session', os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH"))

async def main():
    await client.start()
    print("--- YOUR CHATS ---")
    async for dialog in client.iter_dialogs(limit=20):
        print(f"ID: {dialog.id} | Title: {dialog.title}")
    print("------------------")
    print("Copy the ID (including the minus sign -100...) for the channel you want.")

if __name__ == "__main__":
    asyncio.run(main())