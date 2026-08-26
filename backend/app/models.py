from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime

Base = declarative_base()

class DownloadStatus(enum.Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"

class MediaItem(Base):
    __tablename__ = "media_items"
    id = Column(Integer, primary_key=True)
    channel_id = Column(String, index=True)
    telegram_message_id = Column(BigInteger)
    filename = Column(String)
    file_size = Column(BigInteger)
    mime_type = Column(String)
    # The current state of the download
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING)
    local_path = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ArchiveJob(Base):
    __tablename__ = "archive_jobs"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending") # pending, processing, completed
    progress = Column(Integer, default=0)
    total_parts = Column(Integer, default=0)
    storage_path = Column(String)