import os
import requests
import time
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import dataclass

@dataclass
class DateRange:
    name: str
    start_date: str
    end_date: str

@dataclass
class KeywordMetric:
    keyword: str
    date_range: str
    tweet_count: int
    timestamp: str

class TwitterSearchAPI:
    def __init__(self, base_url: str = "https://api.data365.co/v1.1/twitter/search"):
        load_dotenv()
        self.access_token = os.getenv('access_token')
        if not self.access_token:
            raise ValueError("Access token not found. Please set access_token in your .env file")
        self.base_url = base_url
        self.max_retries = 10
        self.initial_wait = 60
        self.max_wait = 3600
        
        self.date_ranges = [
            DateRange("PRE_COP", "2024-10-11", "2024-11-10"),
            DateRange("COP", "2024-11-11", "2024-11-22"),
            DateRange("POST_COP", "2024-11-23", "2024-12-11")
        ]
        
        self.output_dir = "twitter_data"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.metrics: List[KeywordMetric] = []

    def create_search_task(
        self, 
        keywords: str,
        search_type: str = "latest",
        max_posts: int = 10000,
        from_date: str = None,
        to_date: str = None,
        load_replies: bool = True,
        max_replies: int = 50
    ) -> Dict[str, Any]:
        params = {
            "keywords": keywords,
            "search_type": search_type,
            "max_posts": max_posts,
            "from_date": from_date,
            "to_date": to_date,
            "load_replies": str(load_replies).lower(),
            "max_replies": max_replies,
            "access_token": self.access_token
        }

        try:
            response = requests.post(f"{self.base_url}/post/update", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Create Search Task Error: {e}")
            raise

    def check_search_task_status(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.get(f"{self.base_url}/post/update", params=search_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Check Search Task Status Error: {e}")
            raise

    def search_posts(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = requests.get(f"{self.base_url}/post/posts", params=search_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Search Posts Error: {e}")
            raise

    def wait_for_completion(self, search_params: Dict[str, Any]) -> bool:
        wait_time = self.initial_wait
        attempts = 0

        while attempts < self.max_retries:
            status_response = self.check_search_task_status(search_params)
            status = status_response.get('data', {}).get('status', '').lower()
            
            print(f"Current status: {status} (Attempt {attempts + 1}/{self.max_retries})")
            
            if status == 'finished':
                return True
            elif status == 'failed':
                print("Search task failed")
                return False
            
            print(f"Waiting {wait_time} seconds before next check...")
            time.sleep(wait_time)
            
            wait_time = min(wait_time * 2, self.max_wait)
            attempts += 1

        print("Max retries reached without completion")
        return False

    def search_all(
        self, 
        keywords: str,
        search_type: str = "latest",
        max_posts: int = 10000,
        from_date: str = None,
        to_date: str = None,
        load_replies: bool = True,
        max_replies: int = 50,
        order_by: str = "date_desc",
        max_page_size: int = 50
    ) -> List[Dict[str, Any]]:
        print(f"\nStarting search for period: {from_date} to {to_date}")
        
        # Step 1: Create search task
        print("Creating search task...")
        self.create_search_task(
            keywords=keywords,
            search_type=search_type,
            max_posts=max_posts,
            from_date=from_date,
            to_date=to_date,
            load_replies=load_replies,
            max_replies=max_replies
        )

        # Step 2: Create search parameters for status checking
        search_params = {
            "keywords": keywords,
            "search_type": search_type,
            "max_posts": max_posts,
            "from_date": from_date,
            "to_date": to_date,
            "load_replies": str(load_replies).lower(),
            "max_replies": max_replies,
            "access_token": self.access_token
        }

        # Step 3: Wait for task completion
        print("Waiting for task completion...")
        if not self.wait_for_completion(search_params):
            raise Exception("Search task failed to complete")

        # Step 4: Retrieve all results
        print("Retrieving results...")
        all_results = []
        cursor = None
        page = 0

        while True:
            get_posts_params = {
                "keywords": keywords,
                "order_by": order_by,
                "max_page_size": max_page_size,
                "access_token": self.access_token,
                "from_date": from_date,
                "to_date": to_date,
                "cursor": cursor
            }
            
            response = self.search_posts(get_posts_params)
            page_data = response.get('data', {})
            
            if 'items' in page_data:
                items = page_data['items']
                all_results.extend(items)
                print(f"Retrieved page {page + 1} with {len(items)} items")
            
            page_info = page_data.get('page_info', {})
            if not page_info.get('has_next_page', False):
                break
                
            cursor = page_info.get('cursor')
            page += 1

        print(f"Total results retrieved: {len(all_results)}")
        return all_results

    def process_date_range(
        self,
        date_range: DateRange,
        keywords: str,
        max_page_size: int = 100
    ) -> Optional[pd.DataFrame]:
        try:
            date_range_dir = os.path.join(self.output_dir, date_range.name)
            os.makedirs(date_range_dir, exist_ok=True)
            
            results = self.search_all(
                keywords=keywords,
                from_date=date_range.start_date,
                to_date=date_range.end_date,
                max_page_size=max_page_size
            )
            
            tweet_count = len(results) if results else 0
            
            # Record metric
            self.metrics.append(KeywordMetric(
                keyword=keywords,
                date_range=date_range.name,
                tweet_count=tweet_count,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            if not results:
                print(f"No results found for {date_range.name} with keyword {keywords}")
                return None
            
            tweet_df = create_tweet_dataframe(tweets=results)
            cleaned_df = clean_dataframe(tweet_df)
            
            safe_keywords = keywords.replace('#', '').replace('/', '_')
            filename = os.path.join(date_range_dir, f"{date_range.name}({safe_keywords}).csv")
            cleaned_df.to_csv(filename, index=False)
            print(f"Saved results to {filename}")
            
            return cleaned_df
            
        except Exception as e:
            print(f"Error processing {date_range.name} with keyword {keywords}: {e}")
            return None

    def save_metrics_report(self):
        """Save metrics to a formatted text file."""
        if not self.metrics:
            return
        
        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.output_dir, f"tweet_metrics_{report_time}.txt")
        
        with open(report_path, 'w') as f:
            f.write("Twitter Data Collection Metrics Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Group metrics by date range
            for date_range in self.date_ranges:
                f.write(f"\n{date_range.name} ({date_range.start_date} to {date_range.end_date})\n")
                f.write("-" * 40 + "\n")
                
                date_range_metrics = [m for m in self.metrics if m.date_range == date_range.name]
                
                # Sort by tweet count (descending)
                date_range_metrics.sort(key=lambda x: x.tweet_count, reverse=True)
                
                # Calculate total tweets for this period
                total_tweets = sum(m.tweet_count for m in date_range_metrics)
                
                for metric in date_range_metrics:
                    percentage = (metric.tweet_count / total_tweets * 100) if total_tweets > 0 else 0
                    f.write(f"{metric.keyword:<20} : {metric.tweet_count:>6} tweets ({percentage:>5.1f}%)\n")
                
                f.write(f"\nTotal tweets for {date_range.name}: {total_tweets:,}\n")
                f.write("-" * 40 + "\n")
            
            # Overall statistics
            total_overall = sum(m.tweet_count for m in self.metrics)
            f.write(f"\nOverall Statistics\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total tweets collected: {total_overall:,}\n")
            
            # Keywords ranked by total volume
            f.write("\nKeywords Ranked by Total Volume\n")
            keyword_totals = {}
            for metric in self.metrics:
                keyword_totals[metric.keyword] = keyword_totals.get(metric.keyword, 0) + metric.tweet_count
            
            sorted_keywords = sorted(keyword_totals.items(), key=lambda x: x[1], reverse=True)
            for keyword, count in sorted_keywords:
                percentage = (count / total_overall * 100) if total_overall > 0 else 0
                f.write(f"{keyword:<20} : {count:>6} tweets ({percentage:>5.1f}%)\n")
        
        print(f"\nMetrics report saved to: {report_path}")
    
    def process_all_keywords(self, keywords: List[str]):
        """Process all provided keywords for all date ranges with error handling and progress tracking."""
        if not keywords:
            raise ValueError("No keywords provided")
            
        total_combinations = len(keywords) * len(self.date_ranges)
        processed = 0
        failed = []
        
        print(f"\nStarting processing of {total_combinations} keyword-date range combinations...")
        
        for keyword in keywords:
            print(f"\n{'='*50}")
            print(f"Processing keyword: {keyword}")
            print(f"{'='*50}")
            
            for date_range in self.date_ranges:
                processed += 1
                print(f"\n[Progress: {processed}/{total_combinations}]")
                print(f"Processing {date_range.name} period for {keyword}...")
                
                try:
                    df = self.process_date_range(
                        date_range=date_range,
                        keywords=keyword
                    )
                    
                    if df is None:
                        failed.append((keyword, date_range.name))
                        print(f"Failed to process {keyword} for {date_range.name}")
                    else:
                        print(f"Successfully processed {keyword} for {date_range.name}")
                        
                except Exception as e:
                    failed.append((keyword, date_range.name))
                    print(f"Error processing {keyword} for {date_range.name}: {e}")
                
                time.sleep(2)
        
        # Save metrics report
        self.save_metrics_report()
        
        # Print summary
        print("\n" + "="*50)
        print("Processing Complete!")
        print(f"Total combinations processed: {total_combinations}")
        print(f"Successful: {total_combinations - len(failed)}")
        print(f"Failed: {len(failed)}")
        
        if failed:
            print("\nFailed combinations:")
            for keyword, date_range in failed:
                print(f"- {keyword} for {date_range}")


keywords_1 = [
"#NetZero",
"#ParisAgreement",
"#Sustainability",
"#COP29Outcomes",
"#COP29Agreement",
"#COP29Resolution",
"#GreenEnergy",
"#ClimateJustice",
"#FridaysForFuture", 
"#ExtinctionRebellion", 
"#ClimateStrike",
"#PeopleNotProfit", 
"#ClimateAfrica",
"#ClimateAsia",
"#ClimateEU",
"#ClimateAmerica", 
"#GreenEconomy",
"#NatureBasedSolutions", 
"#COP29Debate",
"#Reindeer",
]
