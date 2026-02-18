"""
Islamic Calendar Service - Hijri calendar calculations and dates
"""

from datetime import datetime, timedelta
import math

HIJRI_MONTHS = [
    "محرم", "صفر", "ربيع الأول", "ربيع الثاني",
    "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
    "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
]

ISLAMIC_HOLIDAYS = {
    "1-1": {"name": "رأس السنة الهجرية", "description": "بداية العام الهجري الجديد"},
    "1-10": {"name": "عاشوراء", "description": "يوم عاشوراء"},
    "3-12": {"name": "المولد النبوي", "description": "ذكرى مولد النبي محمد ﷺ"},
    "7-27": {"name": "ليلة الإسراء والمعراج", "description": "إسراء النبي ﷺ"},
    "8-15": {"name": "نصف شعبان", "description": "ليلة النصف من شعبان"},
    "9-1": {"name": "أول رمضان", "description": "بداية شهر رمضان المبارك"},
    "9-27": {"name": "ليلة القدر", "description": "خير من ألف شهر"},
    "10-1": {"name": "عيد الفطر", "description": "عيد الفطر المبارك"},
    "12-8": {"name": "يوم التروية", "description": "أول أيام الحج"},
    "12-9": {"name": "يوم عرفة", "description": "يوم عرفة المبارك"},
    "12-10": {"name": "عيد الأضحى", "description": "عيد الأضحى المبارك"},
    "12-11": {"name": "أيام التشريق", "description": "أيام التشريق"},
    "12-12": {"name": "أيام التشريق", "description": "أيام التشريق"},
    "12-13": {"name": "أيام التشريق", "description": "آخر أيام التشريق"}
}

def gregorian_to_hijri(year, month, day):
    """Convert Gregorian date to Hijri date (approximate)"""
    # This is an approximate calculation
    # For precise calculations, use a dedicated library like hijri-converter
    
    # Days since Hijri epoch (16 July 622 CE)
    jd = (1461 * (year + 4800 + (month - 14) // 12)) // 4 + \
         (367 * (month - 2 - 12 * ((month - 14) // 12))) // 12 - \
         (3 * ((year + 4900 + (month - 14) // 12) // 100)) // 4 + day - 32075
    
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    
    hijri_month = (24 * l) // 709
    hijri_day = l - (709 * hijri_month) // 24
    hijri_year = 30 * n + j - 30
    
    return hijri_year, hijri_month, hijri_day

def get_islamic_date():
    """Get current Islamic date"""
    today = datetime.now()
    hijri_year, hijri_month, hijri_day = gregorian_to_hijri(
        today.year, today.month, today.day
    )
    
    return {
        "day": hijri_day,
        "month": hijri_month,
        "month_name": HIJRI_MONTHS[hijri_month - 1],
        "year": hijri_year,
        "formatted": f"{hijri_day} {HIJRI_MONTHS[hijri_month - 1]} {hijri_year}هـ"
    }

def get_upcoming_holiday():
    """Get the next Islamic holiday"""
    today = datetime.now()
    hijri_year, hijri_month, hijri_day = gregorian_to_hijri(
        today.year, today.month, today.day
    )
    
    # Search for upcoming holidays
    for days_ahead in range(0, 365):
        check_date = today + timedelta(days=days_ahead)
        check_h_year, check_h_month, check_h_day = gregorian_to_hijri(
            check_date.year, check_date.month, check_date.day
        )
        
        holiday_key = f"{check_h_month}-{check_h_day}"
        if holiday_key in ISLAMIC_HOLIDAYS:
            holiday = ISLAMIC_HOLIDAYS[holiday_key]
            return {
                "name": holiday["name"],
                "description": holiday["description"],
                "date": f"{check_h_day} {HIJRI_MONTHS[check_h_month - 1]}",
                "days_left": days_ahead,
                "gregorian_date": check_date.strftime("%Y-%m-%d")
            }
    
    return None

def get_islamic_year_info(year=None):
    """Get information about Islamic year"""
    if year is None:
        today = datetime.now()
        year, _, _ = gregorian_to_hijri(today.year, today.month, today.day)
    
    return {
        "year": year,
        "is_leap": year % 30 in [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29],
        "days_in_year": 355 if year % 30 in [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29] else 354
    }

def get_month_info(month_number):
    """Get information about a Hijri month"""
    if not 1 <= month_number <= 12:
        return None
    
    month_names = {
        1: {"name": "محرم", "significance": "شهر الحرام، رأس السنة الهجرية"},
        2: {"name": "صفر", "significance": "شهر صفر"},
        3: {"name": "ربيع الأول", "significance": "شهر مولد النبي ﷺ"},
        4: {"name": "ربيع الثاني", "significance": "شهر ربيع الثاني"},
        5: {"name": "جمادى الأولى", "significance": "شهر جمادى الأولى"},
        6: {"name": "جمادى الآخرة", "significance": "شهر جمادى الآخرة"},
        7: {"name": "رجب", "significance": "شهر رجب، من الأشهر الحرم"},
        8: {"name": "شعبان", "significance": "شهر شعبان، شهر النبي ﷺ"},
        9: {"name": "رمضان", "significance": "شهر الصيام والقرآن"},
        10: {"name": "شوال", "significance": "شهر العيد والست من شوال"},
        11: {"name": "ذو القعدة", "significance": "شهر ذو القعدة، من الأشهر الحرم"},
        12: {"name": "ذو الحجة", "significance": "شهر الحج والأضحى"}
    }
    
    return month_names.get(month_number)
