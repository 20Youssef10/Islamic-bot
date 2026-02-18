"""
Data Loader Script for Islamic Bot
Populates database with Quran verses, azkar, and generates embeddings
"""

import requests
import json
from db.database import get_connection
from services.embeddings_service import store_embedding

def load_quran_verses():
    """Load all Quran verses from API"""
    print("📖 Loading Quran verses...")
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Check if already populated
    cur.execute("SELECT COUNT(*) FROM ayat")
    if cur.fetchone()[0] > 0:
        print("   ✓ Quran verses already loaded")
        conn.close()
        return
    
    try:
        # Fetch Quran data from API
        response = requests.get("https://api.alquran.cloud/v1/quran/quran-uthmani")
        data = response.json()
        
        if data["status"] != "OK":
            print("   ✗ Failed to fetch Quran data")
            return
        
        verses = []
        for surah in data["data"]["surahs"]:
            for ayah in surah["ayahs"]:
                verses.append({
                    "id": str(ayah["number"]),
                    "ref": f"Surah {surah["englishName"]} ({surah["number"]}:{ayah["numberInSurah"]})",
                    "text": ayah["text"],
                    "surah": surah["englishName"],
                    "ayah_num": ayah["numberInSurah"]
                })
        
        # Insert into database
        for verse in verses:
            cur.execute(
                "INSERT INTO ayat (id, ref, text) VALUES (?, ?, ?)",
                (verse["id"], verse["ref"], verse["text"])
            )
            # Store embedding for semantic search
            store_embedding(verse["id"], verse["text"])
        
        conn.commit()
        print(f"   ✓ Loaded {len(verses)} verses")
        
    except Exception as e:
        print(f"   ✗ Error loading Quran: {e}")
    finally:
        conn.close()

def load_azkar():
    """Load morning and evening azkar"""
    print("🤲 Loading Azkar...")
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Check if already populated
    cur.execute("SELECT COUNT(*) FROM azkar")
    if cur.fetchone()[0] > 0:
        print("   ✓ Azkar already loaded")
        conn.close()
        return
    
    morning_azkar = [
        ("morning", "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ"),
        ("morning", "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ"),
        ("morning", "اللَّهُمَّ مَا أَصْبَحَ بِي مِنْ نِعْمَةٍ أَوْ بِأَحَدٍ مِنْ خَلْقِكَ فَمِنْكَ وَحْدَكَ لَا شَرِيكَ لَكَ، فَلَكَ الْحَمْدُ وَلَكَ الشُّكْرُ"),
        ("morning", "اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا، وَرِزْقًا طَيِّبًا، وَعَمَلًا مُتَقَبَّلًا"),
        ("morning", "أَعُوذُ بِاللَّهِ مِنَ الشَّيْطَانِ الرَّجِيمِ"),
        ("morning", "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ، وَهُوَ السَّمِيعُ الْعَلِيمُ"),
        ("morning", "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ نَبِيًّا"),
        ("morning", "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ: عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ"),
    ]
    
    evening_azkar = [
        ("evening", "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ"),
        ("evening", "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ"),
        ("evening", "اللَّهُمَّ مَا أَمْسَى بِي مِنْ نِعْمَةٍ أَوْ بِأَحَدٍ مِنْ خَلْقِكَ فَمِنْكَ وَحْدَكَ لَا شَرِيكَ لَكَ، فَلَكَ الْحَمْدُ وَلَكَ الشُّكْرُ"),
        ("evening", "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ"),
        ("evening", "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ هَذِهِ اللَّيْلَةِ، فَتْحَهَا، وَنَصْرَهَا، وَنُورَهَا، وَبَرَكَتَهَا، وَهُدَاهَا"),
        ("evening", "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ، وَهُوَ السَّمِيعُ الْعَلِيمُ"),
        ("evening", "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ نَبِيًّا"),
    ]
    
    try:
        for zikr_type, text in morning_azkar + evening_azkar:
            cur.execute(
                "INSERT INTO azkar (type, text) VALUES (?, ?)",
                (zikr_type, text)
            )
        
        conn.commit()
        print(f"   ✓ Loaded {len(morning_azkar)} morning and {len(evening_azkar)} evening azkar")
        
    except Exception as e:
        print(f"   ✗ Error loading azkar: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Starting data initialization...\n")
    load_quran_verses()
    load_azkar()
    print("\n✅ Data initialization complete!")
