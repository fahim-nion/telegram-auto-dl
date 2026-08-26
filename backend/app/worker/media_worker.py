import asyncio
import logging
from sqlalchemy import text
from ..database import SessionLocal
from ..models import MediaItem, DownloadStatus
from ..telegram.client_manager import tg_manager

class MediaWorker:
    def __init__(self):
        self.is_running = True

    async def start(self):
        logging.info("Starting Sequential Download Worker...")
        while self.is_running:
            db = SessionLocal()
            try:
                # ATOMIC CLAIM: Find one pending item and lock it
                item = db.query(MediaItem).filter(
                    MediaItem.status == DownloadStatus.PENDING
                ).order_by(MediaItem.id.asc()).with_for_update(skip_locked=True).first()

                if item:
                    item.status = DownloadStatus.DOWNLOADING
                    db.commit()
                    
                    # Perform the actual sequential download
                    success = await self.process_download(item)
                    
                    item.status = DownloadStatus.COMPLETED if success else DownloadStatus.FAILED
                    db.commit()
                else:
                    await asyncio.sleep(5) # Wait for new items
            except Exception as e:
                logging.error(f"Worker Loop Error: {e}")
                db.rollback()
            finally:
                db.close()

    async def process_download(self, item):
        client = await tg_manager.get_client()
        # Telethon streams directly to disk; no RAM exhaustion
        try:
            await client.download_media(
                item.telegram_message_id,
                file=f"storage/downloads/{item.id}_{item.filename}",
                progress_callback=self.on_progress
            )
            return True
        except Exception:
            return False

    def on_progress(self, received, total):
        pass