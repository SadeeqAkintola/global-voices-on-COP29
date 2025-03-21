from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class DateRange:
    name: str
    start_date: str
    end_date: str

# API Configuration
BASE_URL = "https://api.data365.co/v1.1/twitter/search"
MAX_RETRIES = 10
INITIAL_WAIT = 60
MAX_WAIT = 3600

# Date Ranges for COP29
DATE_RANGES = [
    DateRange("PRE_COP", "2024-10-11", "2024-11-10"),
    DateRange("COP", "2024-11-11", "2024-11-22"),
    DateRange("POST_COP", "2024-11-23", "2024-12-11")
]

# Output Configuration
OUTPUT_DIR = "twitter_data"