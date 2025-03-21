import re
import pandas as pd
from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger('data_processor')

def create_tweet_dataframe(tweets: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert tweet data to pandas DataFrame with selected fields.
    
    Args:
        tweets: List of tweet dictionaries
        
    Returns:
        pd.DataFrame: Formatted tweet data
    """
    if not isinstance(tweets, list):
        tweets = [tweets]
        
    logger.info(f"Creating DataFrame from {len(tweets)} tweets")

    try:
        df = pd.DataFrame({
            'tweet_id': [tweet['id'] for tweet in tweets],
            'author_username': [tweet['author_username'] for tweet in tweets],
            'created_time': [tweet['created_time'] for tweet in tweets],
            'text': [tweet['text'] for tweet in tweets],
            'text_lang': [tweet['text_lang'] for tweet in tweets],
            'post_type': [tweet['post_type'] for tweet in tweets],
            'favorite_count': [tweet['favorite_count'] for tweet in tweets],
            'reply_count': [tweet['reply_count'] for tweet in tweets],
            'retweet_count': [tweet['retweet_count'] for tweet in tweets],
            'view_count': [tweet['view_count'] for tweet in tweets],
            'source': [tweet['source'] for tweet in tweets],
            'text_tags': [tweet.get('text_tags', []) for tweet in tweets],
            'text_tagged_users': [tweet.get('text_tagged_users', []) for tweet in tweets],
            'attached_links': [tweet.get('attached_links_expanded_url', []) for tweet in tweets]
        })
        
        logger.info("DataFrame created successfully")
        return df
        
    except KeyError as e:
        logger.error(f"Missing key in tweet data: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating DataFrame: {e}")
        raise

def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Select and verify specific columns from DataFrame.
    
    Args:
        df: Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with selected columns
    """
    selected_columns = [
        'author_username',
        'created_time',
        'text',
        'text_lang',
        'post_type',
        'favorite_count',
        'reply_count',
        'retweet_count',
        'view_count',
        'source',
        'text_tags',
        'text_tagged_users'
    ]
    
    missing_columns = [col for col in selected_columns if col not in df.columns]
    if missing_columns:
        logger.error(f"Missing columns in DataFrame: {missing_columns}")
        raise ValueError(f"Missing columns in DataFrame: {missing_columns}")
    
    logger.info(f"Selected {len(selected_columns)} columns from DataFrame")
    return df[selected_columns]

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrame by removing unwanted characters and formatting lists.
    
    Args:
        df: Input DataFrame
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    chars_to_remove = ['"', r'\[', r'\]']

    def clean_string(value):
        if isinstance(value, str):
            for char in chars_to_remove:
                value = re.sub(char, '', value)
        return value

    def clean_list(lst):
        if isinstance(lst, list):
            return [clean_string(item) for item in lst]
        return lst

    try:
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].apply(clean_string)
            elif pd.api.types.is_list_like(df[col]):
                df[col] = df[col].apply(clean_list)
        
        logger.info("DataFrame cleaned successfully")
        return df
        
    except Exception as e:
        logger.error(f"Error cleaning DataFrame: {e}")
        raise