from db.database import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ayat (
        id TEXT PRIMARY KEY,
        ref TEXT,
        text TEXT,
        used INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS azkar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        text TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        ref_id TEXT PRIMARY KEY,
        vector BLOB,
        text TEXT
    )
    """)

    # Favorites table for user-saved verses
    cur.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        item_type TEXT,
        item_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Scheduled azkar settings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scheduled_azkar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id TEXT,
        channel_id TEXT,
        schedule_type TEXT,
        schedule_time TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    # User settings for prayer times
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id TEXT PRIMARY KEY,
        city TEXT DEFAULT 'Mecca',
        country TEXT DEFAULT 'Saudi Arabia',
        calculation_method INTEGER DEFAULT 2
    )
    """)

    # Prayer tracking table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS prayer_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        prayer_name TEXT,
        status TEXT,
        date TEXT,
        is_qada INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Qada prayers tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS qada_prayers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        prayer_name TEXT,
        count INTEGER DEFAULT 1,
        date_added TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    # Fasting tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fasting_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        date TEXT,
        status TEXT,
        notes TEXT
    )
    """)

    # Quran reading tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quran_reading (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        surah INTEGER,
        verses_read INTEGER,
        date_read TEXT
    )
    """)

    # Tasbeeh counter tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasbeeh_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        dhikr TEXT,
        count INTEGER,
        date TEXT
    )
    """)

    # Daily hadith tracking (for daily hadith feature)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_hadith_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        hadith_text TEXT,
        narrator TEXT,
        source TEXT
    )
    """)

    # User streaks tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_streaks (
        user_id TEXT PRIMARY KEY,
        prayer_streak INTEGER DEFAULT 0,
        fasting_streak INTEGER DEFAULT 0,
        quran_streak INTEGER DEFAULT 0,
        last_activity_date TEXT
    )
    """)

    # Interactive Tasbeeh sessions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasbeeh_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        dhikr TEXT,
        target_count INTEGER DEFAULT 33,
        current_count INTEGER DEFAULT 0,
        session_date TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    # Ramadan daily tips log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ramadan_daily_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        day_number INTEGER,
        tip_sent INTEGER DEFAULT 0
    )
    """)

    # Qibla direction history
    cur.execute("""
    CREATE TABLE IF NOT EXISTS qibla_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        location TEXT,
        latitude REAL,
        longitude REAL,
        direction_degrees REAL,
        query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Islamic calendar events
    cur.execute("""
    CREATE TABLE IF NOT EXISTS islamic_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hijri_month INTEGER,
        hijri_day INTEGER,
        event_name TEXT,
        event_description TEXT,
        is_holiday INTEGER DEFAULT 0
    )
    """)

    # Sunnah tracking
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sunnah_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        sunnah_type TEXT,
        date TEXT,
        completed INTEGER DEFAULT 0
    )
    """)

    # Hajj and Umrah guides
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hajj_umrah_guides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guide_type TEXT,
        title TEXT,
        content TEXT,
        category TEXT
    )
    """)

    # Reciters preferences
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_reciter_prefs (
        user_id TEXT PRIMARY KEY,
        preferred_reciter TEXT DEFAULT 'ar.alafasy',
        language_preference TEXT DEFAULT 'ar'
    )
    """)

    # Populate Islamic events
    islamic_events = [
        (1, 1, "رأس السنة الهجرية", "بداية العام الهجري الجديد", 1),
        (1, 10, "عاشوراء", "يوم عاشوراء", 1),
        (3, 12, "المولد النبوي", "ذكرى مولد النبي محمد ﷺ", 1),
        (7, 27, "ليلة الإسراء والمعراج", "ذكرى الإسراء والمعراج", 1),
        (8, 15, "نصف شعبان", "ليلة النصف من شعبان", 0),
        (9, 1, "أول رمضان", "بداية شهر رمضان المبارك", 1),
        (9, 27, "ليلة القدر", "خير من ألف شهر", 1),
        (10, 1, "عيد الفطر", "عيد الفطر المبارك", 1),
        (12, 8, "يوم التروية", "أول أيام الحج", 1),
        (12, 9, "يوم عرفة", "يوم عرفة المبارك", 1),
        (12, 10, "عيد الأضحى", "عيد الأضحى المبارك", 1),
    ]

    for month, day, name, desc, is_holiday in islamic_events:
        cur.execute("""
            INSERT OR IGNORE INTO islamic_events (hijri_month, hijri_day, event_name, event_description, is_holiday)
            VALUES (?, ?, ?, ?, ?)
        """, (month, day, name, desc, is_holiday))

    conn.commit()
    conn.close()