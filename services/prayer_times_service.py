"""
Prayer Times Service - Calculates Islamic prayer times
"""

import requests
import datetime
from typing import Dict, Optional

def get_prayer_times(
    city: str = "Mecca",
    country: str = "Saudi Arabia",
    method: int = 2
) -> Dict:
    """
    Get prayer times for a specific location
    
    Args:
        city: City name
        country: Country name
        method: Calculation method (1-15)
    
    Returns:
        Dictionary with prayer times and metadata
    """
    try:
        # Using Aladhan API
        url = f"http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": city,
            "country": country,
            "method": method,
            "iso8601": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("code") == 200:
            timings = data["data"]["timings"]
            date_info = data["data"]["date"]
            
            return {
                "success": True,
                "city": city,
                "country": country,
                "date": date_info["readable"],
                "hijri": date_info["hijri"]["date"],
                "times": {
                    "Fajr": timings.get("Fajr", "N/A"),
                    "Sunrise": timings.get("Sunrise", "N/A"),
                    "Dhuhr": timings.get("Dhuhr", "N/A"),
                    "Asr": timings.get("Asr", "N/A"),
                    "Maghrib": timings.get("Maghrib", "N/A"),
                    "Isha": timings.get("Isha", "N/A")
                },
                "method": get_method_name(method)
            }
        else:
            return {
                "success": False,
                "error": "Failed to fetch prayer times",
                "city": city
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {str(e)}",
            "city": city
        }

def get_method_name(method_id: int) -> str:
    """Get calculation method name"""
    methods = {
        1: "University of Islamic Sciences, Karachi",
        2: "Islamic Society of North America (ISNA)",
        3: "Muslim World League",
        4: "Umm Al-Qura University, Makkah",
        5: "Egyptian General Authority of Survey"
    }
    return methods.get(method_id, "Custom")

def get_next_prayer(prayer_times: Dict) -> Optional[str]:
    """Determine the next prayer based on current time"""
    if not prayer_times.get("success"):
        return None
    
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    
    prayers = prayer_times["times"]
    for prayer, time in prayers.items():
        if time > current_time:
            return f"{prayer} at {time}"
    
    return f"Fajr tomorrow at {prayers['Fajr']}"
