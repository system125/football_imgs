import hashlib
import json
from functools import wraps
from typing import Callable, Any
import sqlite3

# SQLite setup
conn = sqlite3.connect("cache.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cache (
        func_name TEXT,
        key TEXT PRIMARY KEY,
        result TEXT
    )
''')
conn.commit()


def cache_by_id(model_class):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(id: int, *args, **kwargs) -> Any:
            key = f"{func.__name__}:{id}"
            hashed_key = hashlib.sha256(key.encode()).hexdigest()

            cursor.execute("SELECT result FROM cache WHERE key = ?", (hashed_key,))
            row = cursor.fetchone()
            if row:
                print(f"[CACHE HIT] {func.__name__}({id})")
                cached_data = json.loads(row[0])
                # Reconstruct model objects safely
                if isinstance(cached_data, list):
                    return [model_class(**item) for item in cached_data]
                return model_class(**cached_data)

            # Cache miss
            result = func(id, *args, **kwargs)

            # Serialize result safely
            def serialize(obj):
                if hasattr(obj, "dict"):  # Pydantic or similar
                    return obj.dict()
                elif hasattr(obj, "__dict__"):
                    return {
                        k: v for k, v in obj.__dict__.items()
                        if not k.startswith('_') and isinstance(v, (str, int, float, bool, list, dict, type(None)))
                    }
                else:
                    raise ValueError("Cannot serialize object for caching")

            if isinstance(result, list):
                result_json = json.dumps([serialize(r) for r in result])
            else:
                result_json = json.dumps(serialize(result))

            cursor.execute(
                "INSERT INTO cache (func_name, key, result) VALUES (?, ?, ?)",
                (func.__name__, hashed_key, result_json)
            )
            conn.commit()

            print(f"[CACHE MISS] {func.__name__}({id}) - Caching result")
            return result
        return wrapper
    return decorator
