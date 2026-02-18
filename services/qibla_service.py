"""
Qibla Direction Calculator - Calculate Qibla direction from any location
"""

import math

# Coordinates of Kaaba in Mecca (Masjid al-Haram)
KAABA_LAT = 21.422487
KAABA_LON = 39.826206

def calculate_qibla_direction(latitude, longitude):
    """
    Calculate Qibla direction from given coordinates
    
    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
    
    Returns:
        dict with direction in degrees and cardinal direction
    """
    try:
        # Convert to radians
        lat1 = math.radians(latitude)
        lon1 = math.radians(longitude)
        lat2 = math.radians(KAABA_LAT)
        lon2 = math.radians(KAABA_LON)
        
        # Calculate Qibla direction using spherical trigonometry
        delta_lon = lon2 - lon1
        
        numerator = math.sin(delta_lon)
        denominator = (math.cos(lat1) * math.tan(lat2)) - (math.sin(lat1) * math.cos(delta_lon))
        
        qibla_rad = math.atan2(numerator, denominator)
        qibla_deg = math.degrees(qibla_rad)
        
        # Normalize to 0-360
        qibla_deg = (qibla_deg + 360) % 360
        
        # Get cardinal direction
        cardinal = get_cardinal_direction(qibla_deg)
        
        # Calculate distance
        distance = calculate_distance(latitude, longitude, KAABA_LAT, KAABA_LON)
        
        return {
            "direction_degrees": round(qibla_deg, 2),
            "cardinal_direction": cardinal,
            "direction_text": get_direction_text(qibla_deg),
            "distance_km": round(distance, 2),
            "distance_miles": round(distance * 0.621371, 2)
        }
    except Exception as e:
        return {
            "error": f"Error calculating Qibla direction: {str(e)}"
        }

def get_cardinal_direction(degrees):
    """Convert degrees to cardinal direction"""
    directions = ["شمال", "شمال شرقي", "شرق", "جنوب شرقي", 
                  "جنوب", "جنوب غربي", "غرب", "شمال غربي"]
    index = round(degrees / 45) % 8
    return directions[index]

def get_direction_text(degrees):
    """Get detailed direction text"""
    if 337.5 <= degrees or degrees < 22.5:
        return "شمال (اتجاه الأعلى)"
    elif 22.5 <= degrees < 67.5:
        return "شمال شرقي"
    elif 67.5 <= degrees < 112.5:
        return "شرق (اتجاه اليمين)"
    elif 112.5 <= degrees < 157.5:
        return "جنوب شرقي"
    elif 157.5 <= degrees < 202.5:
        return "جنوب (اتجاه الأسفل)"
    elif 202.5 <= degrees < 247.5:
        return "جنوب غربي"
    elif 247.5 <= degrees < 292.5:
        return "غرب (اتجاه اليسار)"
    else:
        return "شمال غربي"

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def get_qibla_for_major_cities():
    """Get Qibla direction for major cities"""
    cities = {
        "مكة": {"lat": 21.422487, "lon": 39.826206, "qibla": 0},
        "المدينة": {"lat": 24.524654, "lon": 39.569183, "qibla": 450.0},  # Already facing Qibla
        "القاهرة": {"lat": 30.044420, "lon": 31.235712, "qibla": 136.0},
        "الرياض": {"lat": 24.713552, "lon": 46.675296, "qibla": 245.0},
        "دبي": {"lat": 25.204849, "lon": 55.270783, "qibla": 267.0},
        "اسطنبول": {"lat": 41.008238, "lon": 28.978359, "qibla": 151.0},
        "جاكرتا": {"lat": -6.208763, "lon": 106.845599, "qibla": 295.0},
        "كوالالمبور": {"lat": 3.139003, "lon": 101.686855, "qibla": 293.0},
        "لندن": {"lat": 51.507351, "lon": -0.127758, "qibla": 119.0},
        "نيويورك": {"lat": 40.712776, "lon": -74.005974, "qibla": 59.0},
        "باريس": {"lat": 48.856614, "lon": 2.352222, "qibla": 119.0},
        "سيدني": {"lat": -33.868820, "lon": 151.209296, "qibla": 277.0}
    }
    
    result = {}
    for city, coords in cities.items():
        if city == "مكة":
            result[city] = {"direction": "في مكة!", "degrees": 0}
        else:
            qibla = calculate_qibla_direction(coords["lat"], coords["lon"])
            result[city] = {
                "direction": qibla["cardinal_direction"],
                "degrees": qibla["direction_degrees"],
                "distance_km": qibla["distance_km"]
            }
    
    return result
