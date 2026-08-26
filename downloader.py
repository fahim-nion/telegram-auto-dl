import os
import asyncio
import math
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

# --- ULTRA-FAST DOWNLOAD ENGINE ---
async def ultra_download(client, message, file_path, progress_callback):
    size = message.file.size
    concurrency = 8 
    chunk_size = 512 * 1024
    fd = os.open(file_path, os.O_CREAT | os.O_WRONLY)
    try:
        os.ftruncate(fd, size)
        downloaded_bytes = [0] * concurrency

        async def worker(worker_id, offset, limit):
            current_offset = offset
            async for chunk in client.iter_download(
                message.media,
                offset=offset,
                request_size=chunk_size,
                stride=chunk_size * concurrency,
                limit=limit
            ):
                os.pwrite(fd, chunk, current_offset)
                current_offset += chunk_size * concurrency
                downloaded_bytes[worker_id] += len(chunk)
                progress_callback(sum(downloaded_bytes), size)

        chunks_total = math.ceil(size / chunk_size)
        tasks = []
        for i in range(concurrency):
            offset = i * chunk_size
            worker_limit = math.ceil((chunks_total - i) / concurrency)
            if worker_limit > 0:
                tasks.append(worker(i, offset, worker_limit))

        await asyncio.gather(*tasks)
    finally:
        os.close(fd)

# --- MAIN WORKER ---
async def main():
    print("🚀 Starting Ultra-Fast Serial Downloader...")
    await client.start()
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    while True:
        db = Session()
        item = db.query(MediaItem).filter_by(status=DownloadStatus.pending).order_by(MediaItem.telegram_message_id.asc()).first()
        
        if not item:
            print("🏁 All files are finished! Checking for new ones in 60s...")
            db.close()
            await asyncio.sleep(60)
            continue

        item.status = DownloadStatus.downloading
        db.commit()
        clean_name = "".join([c for c in item.filename if c.isalnum() or c in (' ', '.', '_', '-')]).strip()
        final_filename = f"{item.telegram_message_id:05d}_{clean_name}"
        save_to = os.path.join("downloads", final_filename)
        
        print(f"📥 [{item.telegram_message_id}] Downloading: {clean_name}")
        
        try:
            entity = await client.get_entity(int(item.channel_id))
            message = await client.get_messages(entity, ids=item.telegram_message_id)

            if not message or not message.media:
                item.status = DownloadStatus.completed
            else:
                last_ui_update = -1
                def ui_callback(current, total):
                    nonlocal last_ui_update
                    percent = int((current / total) * 100)
                    if percent > last_ui_update:
                        print(f"   ↳ {percent}% | {current/1024/1024:.1f}MB / {total/1024/1024:.1f}MB", end='\r')
                        last_ui_update = percent

                await ultra_download(client, message, save_to, ui_callback)
                print(f"\n✅ Finished: {final_filename}")
                item.status = DownloadStatus.completed
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            item.status = DownloadStatus.failed
        
        db.commit()
        db.close()
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDownloader stopped.")