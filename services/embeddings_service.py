"""
Mock embeddings service for testing without heavy ML dependencies
"""

import pickle
from db.database import get_connection

# Mock model
class MockModel:
    def encode(self, text):
        """Return a simple hash-based vector instead of ML embedding"""
        # Create a simple vector based on text hash
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        # Create a 384-dimensional vector (standard for MiniLM)
        vector = [(hash_val >> (i % 32)) & 0xFF for i in range(384)]
        return vector

model = MockModel()

def store_embedding(ref_id, text):
    """Store text with mock embedding"""
    try:
        vec = model.encode(text)
        blob = pickle.dumps(vec)
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO embeddings VALUES (?, ?, ?)",
            (ref_id, blob, text)
        )
        conn.commit()
        conn.close()
        print(f"✓ Stored embedding for {ref_id}")
    except Exception as e:
        print(f"Error storing embedding: {e}")
