from twitter_scraper import TwitterSearchAPI
from config.settings import DATE_RANGES
from config.keywords import CLIMATE_KEYWORDS
from utils.logger import setup_logger

logger = setup_logger('main')

def main():
    """Main execution function."""
    try:
        twitter_search = TwitterSearchAPI()
        twitter_search.process_keywords(CLIMATE_KEYWORDS, DATE_RANGES)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()