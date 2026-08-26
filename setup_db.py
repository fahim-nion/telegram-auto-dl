import os
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Enum
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import enum

load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("Error: DATABASE_URL not found in .env file!")
    exit()

engine = create_engine(db_url)
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

if __name__ == "__main__":
    print(f"Connecting to: {db_url.split('@')[-1]}")
    try:
        Base.metadata.create_all(engine)
        print("✅ Success! Tables created. Refresh Supabase to see 'media_items'.")
    except Exception as e:
        print(f"❌ Error: {e}")