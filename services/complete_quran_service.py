"""
Complete Quran Service - Full Mushaf with all 6236 verses
"""

import requests
import json
from db.database import get_connection

# Complete Quran structure with surah information
QURAN_STRUCTURE = {
    1: {"name": "الفاتحة", "english_name": "Al-Fatiha", "verses": 7, "revelation": "مكية"},
    2: {"name": "البقرة", "english_name": "Al-Baqarah", "verses": 286, "revelation": "مدنية"},
    3: {"name": "آل عمران", "english_name": "Aal-E-Imran", "verses": 200, "revelation": "مدنية"},
    4: {"name": "النساء", "english_name": "An-Nisa", "verses": 176, "revelation": "مدنية"},
    5: {"name": "المائدة", "english_name": "Al-Ma'idah", "verses": 120, "revelation": "مدنية"},
    6: {"name": "الأنعام", "english_name": "Al-An'am", "verses": 165, "revelation": "مكية"},
    7: {"name": "الأعراف", "english_name": "Al-A'raf", "verses": 206, "revelation": "مكية"},
    8: {"name": "الأنفال", "english_name": "Al-Anfal", "verses": 75, "revelation": "مدنية"},
    9: {"name": "التوبة", "english_name": "At-Tawbah", "verses": 129, "revelation": "مدنية"},
    10: {"name": "يونس", "english_name": "Yunus", "verses": 109, "revelation": "مكية"},
    11: {"name": "هود", "english_name": "Hud", "verses": 123, "revelation": "مكية"},
    12: {"name": "يوسف", "english_name": "Yusuf", "verses": 111, "revelation": "مكية"},
    13: {"name": "الرعد", "english_name": "Ar-Ra'd", "verses": 43, "revelation": "مدنية"},
    14: {"name": "إبراهيم", "english_name": "Ibrahim", "verses": 52, "revelation": "مكية"},
    15: {"name": "الحجر", "english_name": "Al-Hijr", "verses": 99, "revelation": "مكية"},
    16: {"name": "النحل", "english_name": "An-Nahl", "verses": 128, "revelation": "مكية"},
    17: {"name": "الإسراء", "english_name": "Al-Isra", "verses": 111, "revelation": "مكية"},
    18: {"name": "الكهف", "english_name": "Al-Kahf", "verses": 110, "revelation": "مكية"},
    19: {"name": "مريم", "english_name": "Maryam", "verses": 98, "revelation": "مكية"},
    20: {"name": "طه", "english_name": "Taha", "verses": 135, "revelation": "مكية"},
    21: {"name": "الأنبياء", "english_name": "Al-Anbiya", "verses": 112, "revelation": "مكية"},
    22: {"name": "الحج", "english_name": "Al-Hajj", "verses": 78, "revelation": "مدنية"},
    23: {"name": "المؤمنون", "english_name": "Al-Mu'minun", "verses": 118, "revelation": "مكية"},
    24: {"name": "النور", "english_name": "An-Nur", "verses": 64, "revelation": "مدنية"},
    25: {"name": "الفرقان", "english_name": "Al-Furqan", "verses": 77, "revelation": "مكية"},
    26: {"name": "الشعراء", "english_name": "Ash-Shu'ara", "verses": 227, "revelation": "مكية"},
    27: {"name": "النمل", "english_name": "An-Naml", "verses": 93, "revelation": "مكية"},
    28: {"name": "القصص", "english_name": "Al-Qasas", "verses": 88, "revelation": "مكية"},
    29: {"name": "العنكبوت", "english_name": "Al-Ankabut", "verses": 69, "revelation": "مكية"},
    30: {"name": "الروم", "english_name": "Ar-Rum", "verses": 60, "revelation": "مكية"},
    31: {"name": "لقمان", "english_name": "Luqman", "verses": 34, "revelation": "مكية"},
    32: {"name": "السجدة", "english_name": "As-Sajda", "verses": 30, "revelation": "مكية"},
    33: {"name": "الأحزاب", "english_name": "Al-Ahzab", "verses": 73, "revelation": "مدنية"},
    34: {"name": "سبأ", "english_name": "Saba", "verses": 54, "revelation": "مكية"},
    35: {"name": "فاطر", "english_name": "Fatir", "verses": 45, "revelation": "مكية"},
    36: {"name": "يس", "english_name": "Ya-Sin", "verses": 83, "revelation": "مكية"},
    37: {"name": "الصافات", "english_name": "As-Saffat", "verses": 182, "revelation": "مكية"},
    38: {"name": "ص", "english_name": "Sad", "verses": 88, "revelation": "مكية"},
    39: {"name": "الزمر", "english_name": "Az-Zumar", "verses": 75, "revelation": "مكية"},
    40: {"name": "غافر", "english_name": "Ghafir", "verses": 85, "revelation": "مكية"},
    41: {"name": "فصلت", "english_name": "Fussilat", "verses": 54, "revelation": "مكية"},
    42: {"name": "الشورى", "english_name": "Ash-Shura", "verses": 53, "revelation": "مكية"},
    43: {"name": "الزخرف", "english_name": "Az-Zukhruf", "verses": 89, "revelation": "مكية"},
    44: {"name": "الدخان", "english_name": "Ad-Dukhan", "verses": 59, "revelation": "مكية"},
    45: {"name": "الجاثية", "english_name": "Al-Jathiya", "verses": 37, "revelation": "مكية"},
    46: {"name": "الأحقاف", "english_name": "Al-Ahqaf", "verses": 35, "revelation": "مكية"},
    47: {"name": "محمد", "english_name": "Muhammad", "verses": 38, "revelation": "مدنية"},
    48: {"name": "الفتح", "english_name": "Al-Fath", "verses": 29, "revelation": "مدنية"},
    49: {"name": "الحجرات", "english_name": "Al-Hujurat", "verses": 18, "revelation": "مدنية"},
    50: {"name": "ق", "english_name": "Qaf", "verses": 45, "revelation": "مكية"},
    51: {"name": "الذاريات", "english_name": "Adh-Dhariyat", "verses": 60, "revelation": "مكية"},
    52: {"name": "الطور", "english_name": "At-Tur", "verses": 49, "revelation": "مكية"},
    53: {"name": "النجم", "english_name": "An-Najm", "verses": 62, "revelation": "مكية"},
    54: {"name": "القمر", "english_name": "Al-Qamar", "verses": 55, "revelation": "مكية"},
    55: {"name": "الرحمن", "english_name": "Ar-Rahman", "verses": 78, "revelation": "مدنية"},
    56: {"name": "الواقعة", "english_name": "Al-Waqi'a", "verses": 96, "revelation": "مكية"},
    57: {"name": "الحديد", "english_name": "Al-Hadid", "verses": 29, "revelation": "مدنية"},
    58: {"name": "المجادلة", "english_name": "Al-Mujadila", "verses": 22, "revelation": "مدنية"},
    59: {"name": "الحشر", "english_name": "Al-Hashr", "verses": 24, "revelation": "مدنية"},
    60: {"name": "الممتحنة", "english_name": "Al-Mumtahanah", "verses": 13, "revelation": "مدنية"},
    61: {"name": "الصف", "english_name": "As-Saff", "verses": 14, "revelation": "مدنية"},
    62: {"name": "الجمعة", "english_name": "Al-Jumu'ah", "verses": 11, "revelation": "مدنية"},
    63: {"name": "المنافقون", "english_name": "Al-Munafiqun", "verses": 11, "revelation": "مدنية"},
    64: {"name": "التغابن", "english_name": "At-Taghabun", "verses": 18, "revelation": "مدنية"},
    65: {"name": "الطلاق", "english_name": "At-Talaq", "verses": 12, "revelation": "مدنية"},
    66: {"name": "التحريم", "english_name": "At-Tahrim", "verses": 12, "revelation": "مدنية"},
    67: {"name": "الملك", "english_name": "Al-Mulk", "verses": 30, "revelation": "مكية"},
    68: {"name": "القلم", "english_name": "Al-Qalam", "verses": 52, "revelation": "مكية"},
    69: {"name": "الحاقة", "english_name": "Al-Haqqah", "verses": 52, "revelation": "مكية"},
    70: {"name": "المعارج", "english_name": "Al-Ma'arij", "verses": 44, "revelation": "مكية"},
    71: {"name": "نوح", "english_name": "Nuh", "verses": 28, "revelation": "مكية"},
    72: {"name": "الجن", "english_name": "Al-Jinn", "verses": 28, "revelation": "مكية"},
    73: {"name": "المزمل", "english_name": "Al-Muzzammil", "verses": 20, "revelation": "مكية"},
    74: {"name": "المدثر", "english_name": "Al-Muddaththir", "verses": 56, "revelation": "مكية"},
    75: {"name": "القيامة", "english_name": "Al-Qiyamah", "verses": 40, "revelation": "مكية"},
    76: {"name": "الإنسان", "english_name": "Al-Insan", "verses": 31, "revelation": "مدنية"},
    77: {"name": "المرسلات", "english_name": "Al-Mursalat", "verses": 50, "revelation": "مكية"},
    78: {"name": "النبأ", "english_name": "An-Naba", "verses": 40, "revelation": "مكية"},
    79: {"name": "النازعات", "english_name": "An-Nazi'at", "verses": 46, "revelation": "مكية"},
    80: {"name": "عبس", "english_name": "Abasa", "verses": 42, "revelation": "مكية"},
    81: {"name": "التكوير", "english_name": "At-Takwir", "verses": 29, "revelation": "مكية"},
    82: {"name": "الإنفطار", "english_name": "Al-Infitar", "verses": 19, "revelation": "مكية"},
    83: {"name": "المطففين", "english_name": "Al-Mutaffifin", "verses": 36, "revelation": "مكية"},
    84: {"name": "الإنشقاق", "english_name": "Al-Inshiqaq", "verses": 25, "revelation": "مكية"},
    85: {"name": "البروج", "english_name": "Al-Buruj", "verses": 22, "revelation": "مكية"},
    86: {"name": "الطارق", "english_name": "At-Tariq", "verses": 17, "revelation": "مكية"},
    87: {"name": "الأعلى", "english_name": "Al-A'la", "verses": 19, "revelation": "مكية"},
    88: {"name": "الغاشية", "english_name": "Al-Ghashiyah", "verses": 26, "revelation": "مكية"},
    89: {"name": "الفجر", "english_name": "Al-Fajr", "verses": 30, "revelation": "مكية"},
    90: {"name": "البلد", "english_name": "Al-Balad", "verses": 20, "revelation": "مكية"},
    91: {"name": "الشمس", "english_name": "Ash-Shams", "verses": 15, "revelation": "مكية"},
    92: {"name": "الليل", "english_name": "Al-Layl", "verses": 21, "revelation": "مكية"},
    93: {"name": "الضحى", "english_name": "Ad-Duha", "verses": 11, "revelation": "مكية"},
    94: {"name": "الشرح", "english_name": "Ash-Sharh", "verses": 8, "revelation": "مكية"},
    95: {"name": "التين", "english_name": "At-Tin", "verses": 8, "revelation": "مكية"},
    96: {"name": "العلق", "english_name": "Al-Alaq", "verses": 19, "revelation": "مكية"},
    97: {"name": "القدر", "english_name": "Al-Qadr", "verses": 5, "revelation": "مكية"},
    98: {"name": "البينة", "english_name": "Al-Bayyinah", "verses": 8, "revelation": "مدنية"},
    99: {"name": "الزلزلة", "english_name": "Az-Zalzalah", "verses": 8, "revelation": "مدنية"},
    100: {"name": "العاديات", "english_name": "Al-Adiyat", "verses": 11, "revelation": "مكية"},
    101: {"name": "القارعة", "english_name": "Al-Qari'ah", "verses": 11, "revelation": "مكية"},
    102: {"name": "التكاثر", "english_name": "At-Takathur", "verses": 8, "revelation": "مكية"},
    103: {"name": "العصر", "english_name": "Al-Asr", "verses": 3, "revelation": "مكية"},
    104: {"name": "الهمزة", "english_name": "Al-Humazah", "verses": 9, "revelation": "مكية"},
    105: {"name": "الفيل", "english_name": "Al-Fil", "verses": 5, "revelation": "مكية"},
    106: {"name": "قريش", "english_name": "Quraysh", "verses": 4, "revelation": "مكية"},
    107: {"name": "الماعون", "english_name": "Al-Ma'un", "verses": 7, "revelation": "مكية"},
    108: {"name": "الكوثر", "english_name": "Al-Kawthar", "verses": 3, "revelation": "مكية"},
    109: {"name": "الكافرون", "english_name": "Al-Kafirun", "verses": 6, "revelation": "مكية"},
    110: {"name": "النصر", "english_name": "An-Nasr", "verses": 3, "revelation": "مدنية"},
    111: {"name": "المسد", "english_name": "Al-Masad", "verses": 5, "revelation": "مكية"},
    112: {"name": "الإخلاص", "english_name": "Al-Ikhlas", "verses": 4, "revelation": "مكية"},
    113: {"name": "الفلق", "english_name": "Al-Falaq", "verses": 5, "revelation": "مكية"},
    114: {"name": "الناس", "english_name": "An-Nas", "verses": 6, "revelation": "مكية"}
}

def get_surah_info_complete(surah_number):
    """Get complete surah information"""
    return QURAN_STRUCTURE.get(surah_number, None)

def get_ayah_text(surah_number, ayah_number):
    """Get specific ayah text from database"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Calculate global ayah number
        ayah_id = calculate_global_ayah_number(surah_number, ayah_number)
        
        cur.execute("SELECT text, ref FROM ayat WHERE id=?", (str(ayah_id),))
        row = cur.fetchone()
        conn.close()
        
        if row:
            return {
                "text": row['text'],
                "ref": row['ref'],
                "surah": surah_number,
                "ayah": ayah_number
            }
        return None
    except Exception as e:
        print(f"Error getting ayah: {e}")
        return None

def get_surah_text(surah_number, start_ayah=1, end_ayah=None):
    """Get text of entire surah or range of ayahs"""
    try:
        surah_info = get_surah_info_complete(surah_number)
        if not surah_info:
            return None
        
        if end_ayah is None or end_ayah > surah_info['verses']:
            end_ayah = surah_info['verses']
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Get all ayahs in range
        ayahs = []
        for ayah_num in range(start_ayah, end_ayah + 1):
            ayah_id = calculate_global_ayah_number(surah_number, ayah_num)
            cur.execute("SELECT text, ref FROM ayat WHERE id=?", (str(ayah_id),))
            row = cur.fetchone()
            if row:
                ayahs.append({
                    "number": ayah_num,
                    "text": row['text'],
                    "ref": row['ref']
                })
        
        conn.close()
        
        return {
            "surah_name": surah_info['name'],
            "surah_number": surah_number,
            "revelation": surah_info['revelation'],
            "total_verses": surah_info['verses'],
            "ayahs": ayahs,
            "start_ayah": start_ayah,
            "end_ayah": end_ayah
        }
    except Exception as e:
        print(f"Error getting surah text: {e}")
        return None

def calculate_global_ayah_number(surah_number, ayah_number):
    """Calculate global ayah number from surah and ayah"""
    global_ayah = 0
    for surah in range(1, surah_number):
        global_ayah += QURAN_STRUCTURE[surah]['verses']
    global_ayah += ayah_number
    return global_ayah

def get_page_info(page_number):
    """Get information about a Quran page (Mushaf page)"""
    if not 1 <= page_number <= 604:
        return None
    
    # Approximate mapping (simplified)
    # In a real implementation, you'd have a complete page-to-ayah mapping
    return {
        "page": page_number,
        "juz": ((page_number - 1) // 20) + 1,
        "note": "صفحة {} من 604".format(page_number)
    }

def search_in_quran(query):
    """Search for text in Quran"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id, text, ref FROM ayat WHERE text LIKE ? LIMIT 10", (f"%{query}%",))
        rows = cur.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "id": row['id'],
                "text": row['text'],
                "ref": row['ref']
            })
        
        return results
    except Exception as e:
        print(f"Error searching Quran: {e}")
        return []

def get_quran_stats():
    """Get Quran statistics"""
    total_surahs = 114
    total_ayahs = sum(surah['verses'] for surah in QURAN_STRUCTURE.values())
    makki_surahs = sum(1 for surah in QURAN_STRUCTURE.values() if surah['revelation'] == 'مكية')
    madani_surahs = sum(1 for surah in QURAN_STRUCTURE.values() if surah['revelation'] == 'مدنية')
    
    return {
        "total_surahs": total_surahs,
        "total_ayahs": total_ayahs,
        "makki_surahs": makki_surahs,
        "madani_surahs": madani_surahs
    }
