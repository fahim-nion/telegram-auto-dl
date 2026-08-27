import os
from downloader import Session, MediaItem, DownloadStatus
from dotenv import load_dotenv

load_dotenv()

def fix():
    db = Session()
    print("Searching for stuck or failed downloads...")
    # This finds 318 and any other files that didn't finish
    count = db.query(MediaItem).filter(
        (MediaItem.status == DownloadStatus.failed) | 
        (MediaItem.status == DownloadStatus.downloading)
    ).update({MediaItem.status: DownloadStatus.pending})
    
    db.commit()
    db.close()
    print(f"✅ Success! {count} files have been moved back to 'pending'.")

if __name__ == "__main__":
    fix()