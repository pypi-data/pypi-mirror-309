from typing import Any
from prisma import Prisma
import time

def with_db_retries(
    max_attempts: int = 2,
    delay: float = 1.0
) -> Any:
    """Decorator that retries database operations with exponential backoff."""
    assert max_attempts > 0, "max_attempts must be positive"
    assert delay >= 0, "delay must be non-negative"
    
    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 1
            print("Running function:", func.__name__)
            while attempt <= max_attempts:
                db = None
                try:
                    db = Prisma()
                    db.connect()
                    result = func(db, *args, **kwargs)
                    if db:
                        db.disconnect()
                    return result
                except Exception as e:
                    print("attempt:", attempt)
                    print(f"\n!!! Exception caught in attempt {attempt}: {type(e).__name__} - {str(e)}")
                    if db:
                        print("Disconnecting from database (error path)...")
                        db.disconnect()
                        print("Disconnected after error")
                    
                    if attempt < max_attempts:
                        wait_time = delay
                        print(f"Will retry. Attempt {attempt} failed. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        print("Finished waiting, starting next attempt")
                        attempt += 1
                    else:
                        print(f"!!! All {max_attempts} attempts failed. Final exception:", e)
                        print("Raising final exception")
                        raise
        return wrapper
    return decorator
