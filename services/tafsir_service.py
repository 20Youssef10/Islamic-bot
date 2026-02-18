"""
Tafsir Service - Provides Quranic verse interpretations
"""

import requests
import json
from pathlib import Path

CACHE_DIR = Path("data/tafsir_cache")
CACHE_DIR.mkdir(exist_ok=True)

TAFSIR_SOURCES = {
    "ibn-kathir": "Tafsir Ibn Kathir",
    "jalalayn": "Tafsir Al-Jalalayn",
    "maariful-quran": "Maariful Quran"
}

def get_tafsir(surah: int, ayah: int, source: str = "ibn-kathir") -> dict:
    """
    Get tafsir for a specific verse
    
    Args:
        surah: Surah number (1-114)
        ayah: Ayah number
        source: Tafsir source name
    
    Returns:
        Dictionary with tafsir text and metadata
    """
    try:
        # Validate input
        if not (1 <= surah <= 114):
            return {
                "error": "Invalid surah number. Must be between 1 and 114.",
                "surah": surah,
                "ayah": ayah
            }
        
        # Try to fetch from API
        # Using quran.com API or alternative
        api_url = f"https://api.quran.com/api/v4/tafsirs/{source}/by_ayah/{surah}:{ayah}"
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "tafsir" in data:
                    return {
                        "surah": surah,
                        "ayah": ayah,
                        "source": TAFSIR_SOURCES.get(source, source),
                        "text": data["tafsir"]["text"],
                        "success": True
                    }
        except:
            pass
        
        # Fallback to generic explanation
        return get_generic_tafsir(surah, ayah, source)
        
    except Exception as e:
        return {
            "error": f"Error fetching tafsir: {str(e)}",
            "surah": surah,
            "ayah": ayah,
            "success": False
        }

def get_generic_tafsir(surah: int, ayah: int, source: str) -> dict:
    """Provide generic tafsir information when API is unavailable"""
    
    # Famous verses with known interpretations
    known_tafsirs = {
        (1, 1): {
            "text": "**Tafsir of Bismillah**: 'Bismillah' means 'In the name of Allah.' This phrase is recited before starting any good deed. Allah teaches us to begin everything by seeking His name and blessings.",
            "summary": "Starting with Allah's name brings barakah (blessings)"
        },
        (1, 2): {
            "text": "**Tafsir of Alhamdulillah**: All praise belongs to Allah alone. He is the Lord of all worlds - seen and unseen, physical and spiritual realms.",
            "summary": "Praise is exclusively for Allah, the Sustainer of all existence"
        },
        (2, 255): {
            "text": "**Ayat al-Kursi**: This is the greatest verse in the Quran. It describes Allah's absolute oneness, His eternal existence, His complete knowledge, and His supreme authority over the heavens and earth.",
            "summary": "The Throne Verse - greatest protection and declaration of Allah's majesty"
        },
        (112, 1): {
            "text": "**Surah Al-Ikhlas**: This surah declares the absolute oneness of Allah. It negates any partners, offspring, or equals to Allah. It equals one-third of the Quran in reward.",
            "summary": "Pure monotheism - Allah is One, Eternal, Unique"
        }
    }
    
    tafsir_data = known_tafsirs.get((surah, ayah), {
        "text": f"Tafsir for Surah {surah}, Ayah {ayah} from {TAFSIR_SOURCES.get(source, source)}. This verse contains divine guidance and wisdom. Refer to authentic tafsir books for detailed explanation.",
        "summary": "Divine guidance and wisdom"
    })
    
    return {
        "surah": surah,
        "ayah": ayah,
        "source": TAFSIR_SOURCES.get(source, source),
        "text": tafsir_data["text"],
        "summary": tafsir_data["summary"],
        "success": True,
        "note": "This is a summary. For detailed tafsir, consult authentic sources."
    }

def get_surah_info(surah: int) -> dict:
    """Get information about a specific surah"""
    surah_names = {
        1: {"name": "Al-Fatiha", "meaning": "The Opening", "verses": 7, "revelation": "Makkah"},
        2: {"name": "Al-Baqarah", "meaning": "The Cow", "verses": 286, "revelation": "Madinah"},
        112: {"name": "Al-Ikhlas", "meaning": "The Sincerity", "verses": 4, "revelation": "Makkah"},
    }
    
    return surah_names.get(surah, {
        "name": f"Surah {surah}",
        "meaning": "Unknown",
        "verses": "Unknown",
        "revelation": "Unknown"
    })
