import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


def retry_on_exception(attempts: int = 3, delay: float = 2.0):
    def decorator(func: Callable[..., Any]):
        def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(f"DB call failed (attempt {i+1}/{attempts}): {e}")
                    time.sleep(delay)
            logger.error(f"DB call failed after {attempts} attempts: {last_exc}")
            raise last_exc
        return wrapper
    return decorator
