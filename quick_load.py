"""
Quick Data Loader - Sample Data for Testing
"""

from db.database import get_connection
from services.embeddings_service import model
import pickle

def load_sample_quran():
    """Load sample Quran verses for testing"""
    print("📖 Loading sample Quran verses...")
    
    sample_verses = [
        {"id": "1", "ref": "Al-Fatiha (1:1)", "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"},
        {"id": "2", "ref": "Al-Fatiha (1:2)", "text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"},
        {"id": "3", "ref": "Al-Baqarah (2:1)", "text": "الم"},
        {"id": "4", "ref": "Al-Baqarah (2:2)", "text": "ذَٰلِكَ الْكِتَابُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِلْمُتَّقِينَ"},
        {"id": "5", "ref": "Al-Baqarah (2:255)", "text": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَنْ ذَا الَّذِي يَشْفَعُ عِنْدَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ"},
        {"id": "6", "ref": "Al-Ikhlas (112:1)", "text": "قُلْ هُوَ اللَّهُ أَحَدٌ"},
        {"id": "7", "ref": "Al-Ikhlas (112:2)", "text": "اللَّهُ الصَّمَدُ"},
        {"id": "8", "ref": "Al-Ikhlas (112:3)", "text": "لَمْ يَلِدْ وَلَمْ يُولَدْ"},
        {"id": "9", "ref": "Al-Ikhlas (112:4)", "text": "وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ"},
        {"id": "10", "ref": "Al-Falaq (113:1)", "text": "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ"},
    ]
    
    conn = get_connection()
    cur = conn.cursor()
    
    for verse in sample_verses:
        # Insert ayah
        cur.execute(
            "INSERT OR IGNORE INTO ayat (id, ref, text) VALUES (?, ?, ?)",
            (verse["id"], verse["ref"], verse["text"])
        )
        # Store embedding using same connection
        vec = model.encode(verse["text"])
        blob = pickle.dumps(vec)
        cur.execute(
            "INSERT OR REPLACE INTO embeddings VALUES (?, ?, ?)",
            (verse["id"], blob, verse["text"])
        )
    
    conn.commit()
    conn.close()
    print(f"   ✓ Loaded {len(sample_verses)} sample verses")

def load_sample_azkar():
    """Load sample azkar for testing"""
    print("🤲 Loading sample azkar...")
    
    morning_azkar = [
        ("morning", "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ"),
        ("morning", "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا"),
        ("morning", "اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا"),
    ]
    
    evening_azkar = [
        ("evening", "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ"),
        ("evening", "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا"),
        ("evening", "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ"),
    ]
    
    conn = get_connection()
    cur = conn.cursor()
    
    for zikr_type, text in morning_azkar + evening_azkar:
        cur.execute(
            "INSERT OR IGNORE INTO azkar (type, text) VALUES (?, ?)",
            (zikr_type, text)
        )
    
    conn.commit()
    conn.close()
    print(f"   ✓ Loaded {len(morning_azkar) + len(evening_azkar)} azkar")

if __name__ == "__main__":
    print("🚀 Loading sample data...\n")
    load_sample_quran()
    load_sample_azkar()
    print("\n✅ Sample data loaded successfully!")
