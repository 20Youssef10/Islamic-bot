"""
Islamic Knowledge Service - Various Islamic educational content
"""

import random

NAMES_OF_ALLAH = [
    {"name": "الرَّحْمَن", "transliteration": "Ar-Rahman", "meaning": "The Beneficent", "description": "The One who blesses everything with goodness and mercy"},
    {"name": "الرَّحِيم", "transliteration": "Ar-Raheem", "meaning": "The Merciful", "description": "The One who bestows His mercy on the believers"},
    {"name": "الْمَلِك", "transliteration": "Al-Malik", "meaning": "The King", "description": "The Owner of everything, the King of Kings"},
    {"name": "الْقُدُّوس", "transliteration": "Al-Quddus", "meaning": "The Holy", "description": "The Pure One, free from all imperfections"},
    {"name": "السَّلَام", "transliteration": "As-Salam", "meaning": "The Peace", "description": "The Source of peace and safety"},
    {"name": "الْمُؤْمِن", "transliteration": "Al-Mu'min", "meaning": "The Guardian of Faith", "description": "The One who gives faith and security"},
    {"name": "الْمُهَيْمِن", "transliteration": "Al-Muhaymin", "meaning": "The Protector", "description": "The Guardian, the Witness over all things"},
    {"name": "الْعَزِيز", "transliteration": "Al-Aziz", "meaning": "The Mighty", "description": "The Almighty, the Strong, the Invincible"},
    {"name": "الْجَبَّار", "transliteration": "Al-Jabbar", "meaning": "The Compeller", "description": "The Compeller, the One who enforces His will"},
    {"name": "الْمُتَكَبِّر", "transliteration": "Al-Mutakabbir", "meaning": "The Majestic", "description": "The Majestic, the One above all"},
    {"name": "الْخَالِق", "transliteration": "Al-Khaliq", "meaning": "The Creator", "description": "The One who creates everything from nothing"},
    {"name": "الْبَارِئ", "transliteration": "Al-Bari'", "meaning": "The Evolver", "description": "The Maker, the Creator with perfect design"},
    {"name": "الْمُصَوِّر", "transliteration": "Al-Musawwir", "meaning": "The Fashioner", "description": "The One who gives shape and form to creation"},
    {"name": "الْغَفَّار", "transliteration": "Al-Ghaffar", "meaning": "The Forgiver", "description": "The Ever-Forgiving, who forgives again and again"},
    {"name": "الْقَهَّار", "transliteration": "Al-Qahhar", "meaning": "The Subduer", "description": "The Subduer who has power over all things"},
    {"name": "الْوَهَّاب", "transliteration": "Al-Wahhab", "meaning": "The Giver", "description": "The Bestower who gives without expectation"},
    {"name": "الرَّزَّاق", "transliteration": "Ar-Razzaq", "meaning": "The Provider", "description": "The Provider who sustains all creation"},
    {"name": "الْفَتَّاح", "transliteration": "Al-Fattah", "meaning": "The Opener", "description": "The Opener who opens doors of mercy and provision"},
    {"name": "الْعَلِيم", "transliteration": "Al-Alim", "meaning": "The All-Knowing", "description": "The One who knows everything"},
    {"name": "الْقَابِض", "transliteration": "Al-Qabid", "meaning": "The Constrictor", "description": "The One who constricts provision or life"},
]

ISLAMIC_DUAS = {
    "travel": [
        "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَٰذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ",
        "اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، اللَّهُ أَكْبَرُ، سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا"
    ],
    "eating": [
        "بِسْمِ اللَّهِ",
        "الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ"
    ],
    "sleep": [
        "بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
        "سُبْحَانَ اللَّهِ، وَالْحَمْدُ لِلَّهِ، وَاللَّهُ أَكْبَرُ"
    ],
    "entering_home": [
        "بِسْمِ اللَّهِ وَلَجْنَا، وَبِسْمِ اللَّهِ خَرَجْنَا، وَعَلَى اللَّهِ رَبِّنَا تَوَكَّلْنَا"
    ],
    "studying": [
        "رَبِّ زِدْنِي عِلْمًا",
        "اللَّهُمَّ إِنِّي أَسْأَلُكَ فَهْمَ النَّبِيِّينَ"
    ],
    "sick": [
        "أَسْأَلُ اللَّهَ الْعَظِيمَ رَبَّ الْعَرْشِ الْعَظِيمِ أَنْ يَشْفِيَكَ",
        "اللَّهُمَّ رَبَّ النَّاسِ، أَذْهِبِ الْبَأْسَ، وَاشْفِ أَنْتَ الشَّافِي"
    ],
    "distress": [
        "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ",
        "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ"
    ],
    "rain": [
        "اللَّهُمَّ صَيِّبًا نَافِعًا",
        "اللَّهُمَّ أَغِثْنَا"
    ],
    "waking": [
        "الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ"
    ],
    "leaving_home": [
        "بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ"
    ]
}

ISLAMIC_QUIZZES = [
    {
        "question": "How many surahs are in the Quran?",
        "options": ["110", "112", "114", "116"],
        "correct": 2,
        "explanation": "The Quran has 114 surahs (chapters)."
    },
    {
        "question": "Who is the first prophet in Islam?",
        "options": ["Moses", "Abraham", "Adam", "Noah"],
        "correct": 2,
        "explanation": "Prophet Adam (AS) is the first prophet and human on Earth."
    },
    {
        "question": "How many pillars of Islam are there?",
        "options": ["3", "4", "5", "6"],
        "correct": 2,
        "explanation": "There are 5 pillars: Shahada, Salah, Zakat, Fasting, and Hajj."
    },
    {
        "question": "In which month do Muslims fast?",
        "options": ["Muharram", "Ramadan", "Shawwal", "Dhul Hijjah"],
        "correct": 1,
        "explanation": "Muslims fast during the month of Ramadan."
    },
    {
        "question": "What is the first revelation of the Quran?",
        "options": ["Al-Baqarah", "Al-Fatiha", "Al-Alaq", "Al-Ikhlas"],
        "correct": 2,
        "explanation": "The first revelation was Surah Al-Alaq (96:1-5)."
    }
]

ISLAMIC_GOLDEN_QUOTES = [
    "The strongest man is the one who controls his anger.",
    "Speak good or remain silent.",
    "The best of you are those who are best to their families.",
    "Cleanliness is half of faith.",
    "He who has no compassion for people, Allah has no compassion for him.",
    "The ink of the scholar is holier than the blood of the martyr.",
    "Seek knowledge from the cradle to the grave.",
    "A man's true wealth is the good he does in this world."
]

def get_random_name_of_allah():
    """Get a random name of Allah with meaning"""
    return random.choice(NAMES_OF_ALLAH)

def get_dua(situation: str = None):
    """Get dua for specific situation"""
    if situation and situation in ISLAMIC_DUAS:
        return {
            "situation": situation,
            "dua": random.choice(ISLAMIC_DUAS[situation]),
            "translation": get_dua_translation(situation)
        }
    
    # Return random dua
    all_duas = []
    for sit, duas in ISLAMIC_DUAS.items():
        for dua in duas:
            all_duas.append({"situation": sit, "dua": dua})
    
    selected = random.choice(all_duas)
    return {
        "situation": selected["situation"],
        "dua": selected["dua"],
        "translation": get_dua_translation(selected["situation"])
    }

def get_dua_translation(situation: str) -> str:
    """Get translation for dua situation"""
    translations = {
        "travel": "Glory to Him who has subjected this to us",
        "eating": "In the name of Allah",
        "sleep": "In Your name, O Allah, I die and I live",
        "entering_home": "In the name of Allah we enter",
        "studying": "My Lord, increase me in knowledge",
        "sick": "I ask Allah the Mighty to heal you",
        "distress": "There is no god but You, glory to You",
        "rain": "O Allah, send beneficial rain",
        "waking": "Praise be to Allah who gave us life",
        "leaving_home": "In the name of Allah, I rely on Allah"
    }
    return translations.get(situation, "Translation not available")

def get_islamic_quiz():
    """Get a random Islamic quiz question"""
    quiz = random.choice(ISLAMIC_QUIZZES)
    return {
        "question": quiz["question"],
        "options": quiz["options"],
        "correct_index": quiz["correct"],
        "explanation": quiz["explanation"]
    }

def get_islamic_quote():
    """Get a random Islamic golden quote"""
    return random.choice(ISLAMIC_GOLDEN_QUOTES)

def get_allah_names_list():
    """Get all names of Allah"""
    return NAMES_OF_ALLAH
