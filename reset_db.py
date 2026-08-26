import os
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from downloader import MediaItem, DownloadStatus
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)

def reset():
    db = Session()
    print("Connecting to Supabase...")
    db.query(MediaItem).update({MediaItem.status: DownloadStatus.pending})
    db.commit()
    db.close()
    print("✅ Success! The queue has been reset to the beginning.")

if __name__ == "__main__":
    reset()