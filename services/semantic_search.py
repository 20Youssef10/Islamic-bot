"""
Mock semantic search for testing without heavy ML dependencies
"""

import sqlite3
from db.database import get_connection

def semantic_search(query, limit=5):
    """
    Simple keyword-based search as fallback when ML model not available
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Simple keyword search in the text
        keywords = query.lower().split()
        
        cur.execute("SELECT text FROM embeddings LIMIT 100")
        rows = cur.fetchall()
        conn.close()
        
        if not rows:
            return []
        
        # Simple scoring based on keyword matches
        scored = []
        for row in rows:
            text = row['text']
            score = sum(1 for kw in keywords if kw in text.lower())
            if score > 0:
                scored.append((score, text))
        
        # Sort by score
        scored.sort(reverse=True)
        return [text for _, text in scored[:limit]]
        
    except Exception as e:
        print(f"Search error: {e}")
        return []

# Mock model for compatibility
try:
    from services.embeddings_service import model
except ImportError:
    # Create mock model
    class MockModel:
        def encode(self, text):
            return [0.0] * 384  # Return dummy vector
    
    model = MockModel()
