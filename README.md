# Islamic Bot - Enhanced Version

A comprehensive Discord bot for Islamic content including Quran verses, Hadith, prayer times, azkar, and more.

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Edit `.env` file with your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   GUILD_ID=your_server_id
   ```

3. **Populate Database:**
   ```bash
   python data_loader.py
   ```

4. **Run the Bot:**
   ```bash
   python main.py
   ```

## 📋 Available Commands

### 📖 Quran Commands
- `/ayah` - Get a random Quranic verse
- `/ayah_audio [reciter]` - Get a verse with audio recitation
- `/tafsir [surah] [ayah] [source]` - Get tafsir (interpretation) for a specific verse
- `/search_semantic [query]` - Search Quran using AI-powered semantic search

### 📚 Hadith Commands
- `/hadith [collection]` - Get a random Hadith (optional: specify collection like bukhari, muslim)

### 🤲 Azkar Commands
- `/zikr [morning/evening]` - Get morning or evening dhikr
- `/schedule_azkar [type]` - Enable automatic azkar delivery in the channel

### 🕌 Prayer Times
- `/prayer_times [city] [country]` - Get prayer times for any location
- `/next_prayer` - Show the next upcoming prayer

### ⭐ Favorites
- `/favorites` - View your saved favorites
- `/add_favorite [type] [id]` - Add an item to favorites
- `/remove_favorite [type] [id]` - Remove an item from favorites

### ❓ Help
- `/help` - Display all available commands

## 🗂️ Project Structure

```
islamic-bot/
├── main.py                      # Entry point
├── data_loader.py              # Database population script
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── bot/
│   ├── discord_client.py      # Bot client setup
│   └── commands.py            # All bot commands
├── services/
│   ├── quran_service.py       # Quran verse fetching
│   ├── hadith_service.py      # Hadith fetching
│   ├── tafsir_service.py      # Tafsir/interpretation
│   ├── azkar_service.py       # Dhikr/azkar
│   ├── audio_service.py       # Audio recitations
│   ├── prayer_times_service.py # Prayer times API
│   ├── semantic_search.py     # AI-powered search
│   ├── embeddings_service.py  # Vector embeddings
│   ├── favorites_service.py   # Favorites management
│   └── scheduled_azkar_service.py # Automated azkar
├── db/
│   ├── database.py            # Database connection
│   └── models.py              # Database schema
├── data/                      # SQLite database storage
└── audio/                     # Cached audio files
```

## 🆕 What's New

### ✅ Fixed Issues
1. **Import Bug Fixed** - Corrected `embedding_service` to `embeddings_service` in `semantic_search.py`
2. **Empty Services** - Implemented `hadith_service.py` and `tafsir_service.py`
3. **Error Handling** - Added comprehensive try-catch blocks to all commands
4. **Database** - Added proper schema for favorites and scheduled azkar

### ✨ New Features
1. **Help Command** (`/help`) - Beautiful embed showing all commands
2. **Prayer Times** (`/prayer_times`, `/next_prayer`) - Get Islamic prayer times worldwide
3. **Hadith Command** (`/hadith`) - Fetch authentic hadiths with translations
4. **Tafsir Command** (`/tafsir`) - Get verse interpretations
5. **Scheduled Azkar** - Automatically send morning/evening azkar at 6 AM/PM
6. **Favorites System** - Save and manage favorite verses and hadiths
7. **Logging** - Comprehensive logging to `bot.log` file
8. **Graceful Shutdown** - Proper signal handling for clean exits

## 🔧 Configuration

### Reciters for Audio
- `ar.alafasy` - Mishary Alafasy (default)
- `ar.abdulbasit` - Abdul Basit
- `ar.husary` - Mahmoud Khalil Al-Husary
- More available at https://alquran.cloud/api

### Prayer Calculation Methods
- 1 - University of Islamic Sciences, Karachi
- 2 - Islamic Society of North America (ISNA) [default]
- 3 - Muslim World League
- 4 - Umm Al-Qura University, Makkah
- 5 - Egyptian General Authority of Survey

### Hadith Collections
- `bukhari` - Sahih Bukhari
- `muslim` - Sahih Muslim
- `tirmidhi` - Jami' Tirmidhi
- `abudawud` - Sunan Abu Dawud
- `nasai` - Sunan An-Nasa'i
- `ibnmajah` - Sunan Ibn Majah

## 📊 Database Schema

The bot uses SQLite with the following tables:
- `ayat` - Quran verses with tracking
- `azkar` - Morning and evening adhkar
- `embeddings` - Vector embeddings for semantic search
- `favorites` - User-saved favorites
- `scheduled_azkar` - Channel scheduling settings
- `user_settings` - User preferences

## 📝 Logs

Bot activity is logged to `bot.log`:
- Connection events
- Command usage
- Errors with stack traces
- Scheduled azkar delivery

## ⚠️ Notes

1. **Data Population**: Run `data_loader.py` once to populate Quran verses and azkar. This may take several minutes as it downloads and embeds all verses.

2. **API Limits**: The bot uses free APIs that may have rate limits. Error handling is in place for API failures.

3. **Audio Cache**: Audio files are cached in the `audio/` folder to avoid re-downloading.

4. **Embeddings**: The first run will download the sentence-transformers model (~400MB).

## 🤝 Contributing

Feel free to add more features like:
- Tasbeeh counter
- Qibla direction
- Islamic calendar
- Ramadan countdown
- More reciters

## 📄 License

This bot is for educational and personal use. Respect the terms of the APIs used.

---

**جزاك الله خيراً** - May Allah reward you for using this bot!
