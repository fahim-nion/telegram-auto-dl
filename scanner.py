import os
import asyncio
from telethon import TelegramClient
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import enum

load_dotenv()
Base = declarative_base()

class DownloadStatus(enum.Enum):
    pending = "pending"
    downloading = "downloading"
    completed = "completed"
    failed = "failed"

class MediaItem(Base):
    __tablename__ = "media_items"
    id = Column(Integer, primary_key=True)
    channel_id = Column(String)
    telegram_message_id = Column(BigInteger)
    filename = Column(String)
    file_size = Column(BigInteger)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.pending)

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
client = TelegramClient('user_session', os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH"))

async def scan_channel():
    print("Connecting to Telegram...")
    await client.start()
    db = Session()
    link = "https://t.me/+fXxsH-ssfJhlNmM1"
    try:
        print(f"Resolving {link}...")
        target = await client.get_entity(link)
        real_id = target.id
        print(f"✅ Successfully Linked to: {target.title} (Internal ID: {real_id})")
    except Exception as e:
        print(f"❌ Error resolving link: {e}")
        return

    print("Scanning messages for media...")
    count = 0
    scanned = 0
    async for message in client.iter_messages(target):
        scanned += 1
        if scanned % 100 == 0:
            print(f"Read {scanned} messages... found {count} files so far.")

        if message.media:
            # Check if it's a file we can download
            if hasattr(message.media, 'document') or hasattr(message.media, 'photo'):
                filename = "file"
                if message.file and message.file.name:
                    filename = message.file.name
                elif hasattr(message.media, 'photo'):
                    filename = f"photo_{message.id}.jpg"

                peer_id = str(real_id)
                if not peer_id.startswith('-'):
                    peer_id = f"-100{peer_id}"

                exists = db.query(MediaItem).filter_by(telegram_message_id=message.id).first()
                if not exists:
                    new_item = MediaItem(
                        channel_id=peer_id,
                        telegram_message_id=message.id,
                        filename=filename,
                        file_size=message.file.size if message.file else 0,
                        status=DownloadStatus.pending
                    )
                    db.add(new_item)
                    count += 1
                    if count % 20 == 0:
                        db.commit()

    db.commit()
    print(f"✅ SUCCESS! Added {count} files to the queue.")

if __name__ == "__main__":
    asyncio.run(scan_channel())