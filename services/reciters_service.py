"""
Extended Reciters List - More Quran reciters for audio service
"""

RECITERS = {
    # Arabic Reciters
    "ar.alafasy": {
        "name": "مشاري العفاسي",
        "name_en": "Mishary Alafasy",
        "language": "العربية",
        "style": "مجود",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "ar.abdulbasit": {
        "name": "عبد الباسط عبد الصمد",
        "name_en": "Abdul Basit Abdus Samad",
        "language": "العربية",
        "style": "مجود",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "ar.husary": {
        "name": "محمود خليل الحصري",
        "name_en": "Mahmoud Khalil Al-Husary",
        "language": "العربية",
        "style": "مجود",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "ar.minshawi": {
        "name": "محمد صديق المنشاوي",
        "name_en": "Mohamed Siddiq El-Minshawi",
        "language": "العربية",
        "style": "مجود",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "ar.ghamdi": {
        "name": "سعد الغامدي",
        "name_en": "Saad Al-Ghamdi",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐"
    },
    "ar.shatri": {
        "name": "أبو بكر الشاطري",
        "name_en": "Abu Bakr Al-Shatri",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐"
    },
    "ar.ajamy": {
        "name": "أحمد بن علي العجمي",
        "name_en": "Ahmad Al-Ajmi",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐"
    },
    "ar.juhany": {
        "name": "عبدالله الجهني",
        "name_en": "Abdullah Al-Juhany",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐"
    },
    "ar.sudais": {
        "name": "عبدالرحمن السديس",
        "name_en": "Abdul Rahman Al-Sudais",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "ar.shuraim": {
        "name": "سعود الشريم",
        "name_en": "Saud Al-Shuraim",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    "ar.maher": {
        "name": "ماهر المعيقلي",
        "name_en": "Maher Al-Muaiqly",
        "language": "العربية",
        "style": "حدر",
        "popularity": "⭐⭐⭐⭐"
    },
    "ar.basit": {
        "name": "عبد الباسط (مصورة)",
        "name_en": "Abdul Basit (Mujawwad)",
        "language": "العربية",
        "style": "مجود",
        "popularity": "⭐⭐⭐⭐⭐"
    },
    
    # Non-Arabic Reciters
    "en.walk": {
        "name": "Ibrahim Walk (English)",
        "name_en": "Ibrahim Walk",
        "language": "English",
        "style": "Translation",
        "popularity": "⭐⭐⭐"
    },
    "fr.leclerc": {
        "name": "Youssouf Leclerc (French)",
        "name_en": "Youssouf Leclerc",
        "language": "Français",
        "style": "Translation",
        "popularity": "⭐⭐"
    },
    "ur.khan": {
        "name": "Shamshad Ali Khan (Urdu)",
        "name_en": "Shamshad Ali Khan",
        "language": "اردو",
        "style": "ترجمة",
        "popularity": "⭐⭐⭐"
    },
    "id.mahalli": {
        "name": "Muhammad Thaha al Junayd (Indonesian)",
        "name_en": "Muhammad Thaha",
        "language": "Bahasa Indonesia",
        "style": "ترجمة",
        "popularity": "⭐⭐"
    }
}

def get_reciter_info(reciter_id):
    """Get reciter information"""
    return RECITERS.get(reciter_id, None)

def get_reciters_by_style(style):
    """Get reciters by style (Mujawwad or Murattal)"""
    result = {}
    for reciter_id, info in RECITERS.items():
        if info["style"] == style:
            result[reciter_id] = info
    return result

def get_arabic_reciters():
    """Get only Arabic reciters"""
    result = {}
    for reciter_id, info in RECITERS.items():
        if info["language"] == "العربية":
            result[reciter_id] = info
    return result

def get_reciters_list_formatted():
    """Get formatted list of reciters"""
    lines = ["📖 **قائمة القراء المتاحين:**\n"]
    
    lines.append("\n**🌟 قراء العرب:**")
    for reciter_id, info in RECITERS.items():
        if info["language"] == "العربية":
            lines.append(f"`{reciter_id}` - {info['name']} ({info['style']}) {info['popularity']}")
    
    lines.append("\n**🌍 قراء بلغات أخرى:**")
    for reciter_id, info in RECITERS.items():
        if info["language"] != "العربية":
            lines.append(f"`{reciter_id}` - {info['name']} ({info['language']})")
    
    return "\n".join(lines)

def get_default_reciter():
    """Get default reciter"""
    return "ar.alafasy"

def get_random_reciter():
    """Get random reciter"""
    import random
    return random.choice(list(RECITERS.keys()))
