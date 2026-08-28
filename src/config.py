# Central, environment-driven configuration for the test harness
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
    AUTH_USERNAME: str = os.getenv("AUTH_USERNAME", "admin")
    AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "password123")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

    # Transport-level retry tuning (connection issues / 5xx)
    RETRY_TOTAL: int = int(os.getenv("RETRY_TOTAL", "3"))
    RETRY_BACKOFF_FACTOR: float = float(os.getenv("RETRY_BACKOFF_FACTOR", "0.5"))
    RETRY_STATUS_FORCELIST = (500, 502, 503, 504)


settings = Settings()
