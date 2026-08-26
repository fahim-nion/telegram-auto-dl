
---

# Telegram Auto Batch Downloader Script

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-Supabase-green.svg)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An industrial-grade CLI tool designed for downloading massive Telegram media collections (**Limitations <50GB per day**) in **perfect sequential order**. Whether you are backing up an entire educational course or a media archive, this tool ensures your files are organized from Introduction to Conclusion with maximum speed.

---

## 🌟 Why Use This?

Most Telegram downloaders are slow or download files in a random order. This project solves those problems:

1.  **Strict Sequentiality:** Downloads from the first message to the last. Perfect for courses where order matters.
2.  **8-Stream Turbo Engine:** Uses parallel internal connections to saturate your bandwidth, making downloads **10x faster** than standard clients.
3.  **Cloud-Powered Queue:** Uses **Supabase (PostgreSQL)** to track progress. If your internet cuts out or your PC restarts, it resumes exactly where it left off.
4.  **Hardware Efficient:** Uses low-level `os.pwrite` to stream files directly to your drive, preventing RAM spikes and file corruption.

---

## 🛠️ Prerequisites

Before running, you need:
1.  **Telegram API Keys:** Generate `api_id` and `api_hash` from [my-telegram-org](https://my.telegram.org).
2.  **Supabase Account:** Set up a free project at [supabase](https://supabase.com) and get your **Database Connection String (URI)**.
3.  **Python 3.10+** installed on your local machine.

---

## 🚀 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/telegram-auto-dl.git
cd telegram-auto-dl
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install sqlalchemy psycopg2-binary python-dotenv telethon
```

### 4. Configure Environment Variables
Create a file named `.env` in the root folder and paste the following:
```env
TELEGRAM_API_ID=your_id_here
TELEGRAM_API_HASH=your_hash_here
DATABASE_URL=postgresql://postgres.[ID]:[PASS]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require
```

---

## 🎮 How to Run (Step-by-Step)

Follow these phases in order to start your download:

### Phase 1: Initialize the Database
Run this once to create the necessary tables in your Supabase cloud.
```bash
python setup_db.py
```

### Phase 2: Authenticate Telegram
Run this to link your Telegram account to the script. It will ask for your phone number and the code sent to your Telegram app.
```bash
python login.py
```

### Phase 3: Scan the Channel
This script indexes all media in the channel and saves the list to Supabase. Paste the channel link when prompted.
```bash
python scanner.py
```

### Phase 4: Start Downloading
The engine will now start downloading files sequentially. It will skip already completed files and handle errors automatically.
```bash
python downloader.py
```

---

## 🛠️ Maintenance & Troubleshooting

*   **Resume/Fix Stuck Files:** If a download was interrupted, run `fix_queue.py` to move "stuck" files back to the pending list so they can be retried.
*   **Full Reset:** If you want to start the entire channel from the beginning, run `reset_db.py`.
*   **Security:** If you accidentally push your `.session` files to GitHub, immediately go to **Telegram App > Settings > Devices > Terminate all other sessions**.

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `setup_db.py` | Provisions Supabase tables. |
| `login.py` | Handles Telegram OAuth and Session generation. |
| `scanner.py` | Indexes channel metadata to the cloud. |
| `downloader.py` | The main 8-stream Turbo download engine. |
| `fix_queue.py` | Resets `failed` or `downloading` items to `pending`. |
| `reset_db.py` | Wipes progress to restart the entire queue. |

---

## 🔒 Security Notice
**DO NOT** share or upload your `.env` or `user_session.session` files. These files contain full access to your database and your Telegram account. A `.gitignore` is included to help prevent accidental leaks.

---
**Disclaimer:** This tool is for personal use and backup purposes. Respect Telegram's Terms of Service and the copyright of the content owners.