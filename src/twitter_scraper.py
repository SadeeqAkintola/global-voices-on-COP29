import os
import requests
import time
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv

from config.settings import BASE_URL, MAX_RETRIES, INITIAL_WAIT, MAX_WAIT, DateRange, OUTPUT_DIR
from utils.logger import setup_logger
from utils.data_processor import create_tweet_dataframe, select_columns, clean_dataframe

logger = setup_logger('twitter_scraper')

class TwitterSearchAPI:
    """Handles Twitter data collection using Data365.co API."""
    
    def __init__(self):
        load_dotenv()
        self.access_token = os.getenv('access_token')
        if not self.access_token:
            raise ValueError("Access token not found in .env file")
            
        self.base_url = BASE_URL
        self.metrics = []
        
        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def _create_search_task(self, keywords: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """Create a new search task on the API."""
        params = {
            "keywords": keywords,
            "search_type": "latest",
            "max_posts": 10000,
            "from_date": from_date,
            "to_date": to_date,
            "load_replies": "true",
            "max_replies": 50,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(f"{self.base_url}/post/update", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create search task: {e}")
            raise

    def _check_task_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check the status of an ongoing search task."""
        try:
            response = requests.get(f"{self.base_url}/post/update", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check task status: {e}")
            raise

    def _wait_for_completion(self, keywords: str, from_date: str, to_date: str) -> bool:
        """Wait for task completion with exponential backoff."""
        wait_time = INITIAL_WAIT
        attempts = 0
        
        params = {
            "keywords": keywords,
            "from_date": from_date,
            "to_date": to_date,
            "access_token": self.access_token
        }

        while attempts < MAX_RETRIES:
            status_response = self._check_task_status(params)
            status = status_response.get('data', {}).get('status', '').lower()
            
            logger.info(f"Task status: {status} (Attempt {attempts + 1}/{MAX_RETRIES})")
            
            if status == 'finished':
                return True
            elif status == 'failed':
                logger.error("Search task failed")
                return False
            
            logger.info(f"Waiting {wait_time} seconds before next check...")
            time.sleep(wait_time)
            
            wait_time = min(wait_time * 2, MAX_WAIT)
            attempts += 1

        logger.error("Max retries reached without completion")
        return False

    def _collect_results(self, keywords: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """Collect all results from a completed search task."""
        all_results = []
        cursor = None
        page = 0

        while True:
            params = {
                "keywords": keywords,
                "order_by": "date_desc",
                "max_page_size": 100,
                "access_token": self.access_token,
                "from_date": from_date,
                "to_date": to_date,
                "cursor": cursor
            }
            
            try:
                response = requests.get(f"{self.base_url}/post/posts", params=params)
                response.raise_for_status()
                page_data = response.json().get('data', {})
                
                if 'items' in page_data:
                    items = page_data['items']
                    all_results.extend(items)
                    logger.info(f"Retrieved page {page + 1} with {len(items)} items")
                
                page_info = page_data.get('page_info', {})
                if not page_info.get('has_next_page', False):
                    break
                    
                cursor = page_info.get('cursor')
                page += 1
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to collect results: {e}")
                raise

        logger.info(f"Total results retrieved: {len(all_results)}")
        return all_results

    def _save_results(self, results: List[Dict[str, Any]], keyword: str, period: str):
        """Save results to CSV file and update metrics."""
        if not results:
            logger.warning(f"No results to save for {keyword} in {period}")
            return

        try:
            # Create period directory
            period_dir = os.path.join(OUTPUT_DIR, period)
            os.makedirs(period_dir, exist_ok=True)

            # Process DataFrame
            df = create_tweet_dataframe(results)
            df = select_columns(df)
            df = clean_dataframe(df)
            
            # Save to file
            safe_keyword = keyword.replace('#', '').replace('/', '_')
            filename = os.path.join(period_dir, f"{period}({safe_keyword}).csv")
            df.to_csv(filename, index=False)
            
            # Update metrics
            self.metrics.append({
                'keyword': keyword,
                'period': period,
                'tweet_count': len(results),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            logger.info(f"Saved {len(results)} tweets to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise

    def search_all(self, keywords: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Perform complete search operation for given parameters.
        
        Args:
            keywords: Search keywords
            from_date: Start date
            to_date: End date
            
        Returns:
            List of tweet data
        """
        logger.info(f"Starting search for period: {from_date} to {to_date}")
        
        # Create and monitor search task
        self._create_search_task(keywords, from_date, to_date)
        if not self._wait_for_completion(keywords, from_date, to_date):
            raise Exception("Search task failed to complete")

        # Collect results
        return self._collect_results(keywords, from_date, to_date)

    def process_keywords(self, keywords: List[str], date_ranges: List[DateRange]):
        """
        Process multiple keywords across specified date ranges.
        
        Args:
            keywords: List of keywords to search
            date_ranges: List of date ranges to search within
        """
        logger.info(f"Processing {len(keywords)} keywords across {len(date_ranges)} date ranges")
        
        for keyword in keywords:
            for date_range in date_ranges:
                try:
                    results = self.search_all(
                        keyword, 
                        date_range.start_date, 
                        date_range.end_date
                    )
                    
                    if results:
                        self._save_results(results, keyword, date_range.name)
                        
                except Exception as e:
                    logger.error(f"Error processing {keyword} for {date_range.name}: {e}")
                
                time.sleep(2) 