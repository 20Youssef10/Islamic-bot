"""
Favorites Service - Manages user-saved favorite verses and hadiths
"""

from db.database import get_connection
from typing import List, Dict

def add_favorite(user_id: str, item_type: str, item_id: str) -> bool:
    """Add an item to user's favorites"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Check if already exists
        cur.execute(
            "SELECT id FROM favorites WHERE user_id=? AND item_type=? AND item_id=?",
            (user_id, item_type, item_id)
        )
        if cur.fetchone():
            conn.close()
            return False  # Already favorited
        
        cur.execute(
            "INSERT INTO favorites (user_id, item_type, item_id) VALUES (?, ?, ?)",
            (user_id, item_type, item_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding favorite: {e}")
        return False

def remove_favorite(user_id: str, item_type: str, item_id: str) -> bool:
    """Remove an item from user's favorites"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM favorites WHERE user_id=? AND item_type=? AND item_id=?",
            (user_id, item_type, item_id)
        )
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        print(f"Error removing favorite: {e}")
        return False

def get_user_favorites(user_id: str) -> List[Dict]:
    """Get all favorites for a user"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT item_type, item_id, created_at FROM favorites WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error getting favorites: {e}")
        return []

def is_favorite(user_id: str, item_type: str, item_id: str) -> bool:
    """Check if an item is in user's favorites"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM favorites WHERE user_id=? AND item_type=? AND item_id=?",
            (user_id, item_type, item_id)
        )
        result = cur.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error checking favorite: {e}")
        return False
