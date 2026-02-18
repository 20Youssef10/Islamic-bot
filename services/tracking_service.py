"""
Personal Tracking Service - Track prayers, fasting, Quran reading, etc.
"""

import sqlite3
from datetime import datetime, timedelta
from db.database import get_connection

def track_prayer(user_id: str, prayer_name: str, status: str = "completed", is_qada: bool = False):
    """Track daily prayers"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            INSERT INTO prayer_tracking (user_id, prayer_name, status, date, is_qada)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, prayer_name, status, today, 1 if is_qada else 0))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error tracking prayer: {e}")
        return False

def get_prayer_stats(user_id: str, days: int = 7):
    """Get prayer statistics for user"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        cur.execute("""
            SELECT prayer_name, status, COUNT(*) as count
            FROM prayer_tracking
            WHERE user_id = ? AND date >= ?
            GROUP BY prayer_name, status
        """, (user_id, start_date))
        
        rows = cur.fetchall()
        conn.close()
        
        stats = {}
        for row in rows:
            prayer = row['prayer_name']
            status = row['status']
            if prayer not in stats:
                stats[prayer] = {}
            stats[prayer][status] = row['count']
        
        return stats
    except Exception as e:
        print(f"Error getting prayer stats: {e}")
        return {}

def track_qada_prayers(user_id: str, prayer_name: str, count: int = 1):
    """Track Qada (makeup) prayers"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            INSERT INTO qada_prayers (user_id, prayer_name, count, date_added)
            VALUES (?, ?, ?, ?)
        """, (user_id, prayer_name, count, today))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error tracking qada: {e}")
        return False

def get_qada_count(user_id: str):
    """Get remaining Qada prayers"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT prayer_name, SUM(count) as total
            FROM qada_prayers
            WHERE user_id = ? AND completed = 0
            GROUP BY prayer_name
        """, (user_id,))
        
        rows = cur.fetchall()
        conn.close()
        
        return {row['prayer_name']: row['total'] for row in rows}
    except Exception as e:
        print(f"Error getting qada count: {e}")
        return {}

def mark_qada_completed(user_id: str, prayer_name: str):
    """Mark one Qada prayer as completed"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Get oldest incomplete qada prayer
        cur.execute("""
            SELECT id, count FROM qada_prayers
            WHERE user_id = ? AND prayer_name = ? AND completed = 0
            ORDER BY date_added ASC LIMIT 1
        """, (user_id, prayer_name))
        
        row = cur.fetchone()
        if row:
            if row['count'] > 1:
                # Decrement count
                cur.execute("""
                    UPDATE qada_prayers SET count = count - 1
                    WHERE id = ?
                """, (row['id'],))
            else:
                # Mark as completed
                cur.execute("""
                    UPDATE qada_prayers SET completed = 1
                    WHERE id = ?
                """, (row['id'],))
            
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    except Exception as e:
        print(f"Error marking qada complete: {e}")
        return False

def track_fasting(user_id: str, date: str = None, status: str = "fasted"):
    """Track fasting days"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            INSERT OR REPLACE INTO fasting_tracking (user_id, date, status)
            VALUES (?, ?, ?)
        """, (user_id, date, status))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error tracking fasting: {e}")
        return False

def get_fasting_stats(user_id: str, year: int = None):
    """Get fasting statistics"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        if not year:
            year = datetime.now().year
        
        cur.execute("""
            SELECT status, COUNT(*) as count
            FROM fasting_tracking
            WHERE user_id = ? AND strftime('%Y', date) = ?
            GROUP BY status
        """, (user_id, str(year)))
        
        rows = cur.fetchall()
        conn.close()
        
        return {row['status']: row['count'] for row in rows}
    except Exception as e:
        print(f"Error getting fasting stats: {e}")
        return {}

def track_quran_reading(user_id: str, surah: int, verses_read: int):
    """Track Quran reading progress"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            INSERT INTO quran_reading (user_id, surah, verses_read, date_read)
            VALUES (?, ?, ?, ?)
        """, (user_id, surah, verses_read, today))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error tracking Quran reading: {e}")
        return False

def get_quran_reading_stats(user_id: str, days: int = 30):
    """Get Quran reading statistics"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        cur.execute("""
            SELECT SUM(verses_read) as total_verses,
                   COUNT(DISTINCT surah) as surahs_read,
                   COUNT(DISTINCT date_read) as days_read
            FROM quran_reading
            WHERE user_id = ? AND date_read >= ?
        """, (user_id, start_date))
        
        row = cur.fetchone()
        conn.close()
        
        return {
            "total_verses": row['total_verses'] or 0,
            "surahs_read": row['surahs_read'] or 0,
            "days_read": row['days_read'] or 0
        }
    except Exception as e:
        print(f"Error getting Quran stats: {e}")
        return {"total_verses": 0, "surahs_read": 0, "days_read": 0}

def get_khatm_progress(user_id: str):
    """Get progress toward completing the Quran"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT surah, MAX(ayah) as last_ayah
            FROM quran_reading
            WHERE user_id = ?
            GROUP BY surah
        """, (user_id,))
        
        rows = cur.fetchall()
        conn.close()
        
        # Surah verse counts (simplified)
        surah_verses = {
            1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75,
            9: 129, 10: 109, 11: 123, 12: 111, 13: 43, 14: 52, 15: 99
        }
        
        completed_surahs = 0
        for row in rows:
            surah = row['surah']
            last_ayah = row['last_ayah']
            if surah in surah_verses and last_ayah >= surah_verses[surah]:
                completed_surahs += 1
        
        return {
            "completed_surahs": completed_surahs,
            "total_surahs": 114,
            "progress_percentage": round((completed_surahs / 114) * 100, 2)
        }
    except Exception as e:
        print(f"Error getting khatm progress: {e}")
        return {"completed_surahs": 0, "total_surahs": 114, "progress_percentage": 0}

def track_tasbeeh(user_id: str, dhikr: str, count: int):
    """Track tasbeeh count"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            INSERT INTO tasbeeh_tracking (user_id, dhikr, count, date)
            VALUES (?, ?, ?, ?)
        """, (user_id, dhikr, count, today))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error tracking tasbeeh: {e}")
        return False

def get_tasbeeh_stats(user_id: str, days: int = 7):
    """Get tasbeeh statistics"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        cur.execute("""
            SELECT dhikr, SUM(count) as total
            FROM tasbeeh_tracking
            WHERE user_id = ? AND date >= ?
            GROUP BY dhikr
        """, (user_id, start_date))
        
        rows = cur.fetchall()
        conn.close()
        
        return {row['dhikr']: row['total'] for row in rows}
    except Exception as e:
        print(f"Error getting tasbeeh stats: {e}")
        return {}
