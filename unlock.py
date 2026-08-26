import os
from downloader import Session, MediaItem, DownloadStatus
from dotenv import load_dotenv

def unlock():
    db = Session()
    print("Checking for stuck files in Supabase...")
    # Find any files that were stuck in 'downloading' and move them back to 'pending'
    count = db.query(MediaItem).filter(MediaItem.status == DownloadStatus.downloading).update(
        {MediaItem.status: DownloadStatus.pending}
    )
    db.commit()
    db.close()
    print(f"✅ Success! {count} stuck files have been unlocked.")

if __name__ == "__main__":
    unlock()