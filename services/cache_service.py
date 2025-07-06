"""
Cache service for improving performance by caching generated tasks and user data.
"""
import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Simple file-based cache for tasks and user data"""
    
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir
        self.tasks_cache_dir = os.path.join(cache_dir, 'tasks')
        self.user_cache_dir = os.path.join(cache_dir, 'users')
        
        # Create cache directories
        os.makedirs(self.tasks_cache_dir, exist_ok=True)
        os.makedirs(self.user_cache_dir, exist_ok=True)
    
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key from text content"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _get_cache_path(self, cache_type: str, key: str) -> str:
        """Get the file path for a cache entry"""
        if cache_type == 'tasks':
            return os.path.join(self.tasks_cache_dir, f"{key}.json")
        elif cache_type == 'users':
            return os.path.join(self.user_cache_dir, f"{key}.json")
        else:
            raise ValueError(f"Unknown cache type: {cache_type}")
    
    def _is_cache_valid(self, cache_path: str, max_age_hours: int = 24) -> bool:
        """Check if cache file exists and is not expired"""
        if not os.path.exists(cache_path):
            return False
        
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        expiry_time = file_time + timedelta(hours=max_age_hours)
        
        return datetime.now() < expiry_time
    
    def get_cached_tasks(self, text: str, num_tasks: int = 5) -> Optional[List[Dict[str, Any]]]:
        """Get cached tasks for given text content"""
        try:
            cache_key = f"{self._get_cache_key(text)}_{num_tasks}"
            cache_path = self._get_cache_path('tasks', cache_key)
            
            if self._is_cache_valid(cache_path, max_age_hours=24):
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Retrieved {len(data['tasks'])} tasks from cache")
                    return data['tasks']
            
        except Exception as e:
            logger.error(f"Error reading task cache: {e}")
        
        return None
    
    def cache_tasks(self, text: str, tasks: List[Dict[str, Any]], num_tasks: int = 5) -> bool:
        """Cache generated tasks for given text content"""
        try:
            cache_key = f"{self._get_cache_key(text)}_{num_tasks}"
            cache_path = self._get_cache_path('tasks', cache_key)
            
            cache_data = {
                'text_hash': self._get_cache_key(text),
                'num_tasks': num_tasks,
                'tasks': tasks,
                'cached_at': datetime.now().isoformat(),
                'text_preview': text[:100] + '...' if len(text) > 100 else text
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            logger.info(f"Cached {len(tasks)} tasks")
            return True
            
        except Exception as e:
            logger.error(f"Error caching tasks: {e}")
            return False
    
    def get_cached_user_data(self, email: str) -> Optional[Dict[str, Any]]:
        """Get cached user data for given email"""
        try:
            cache_key = self._get_cache_key(email.lower())
            cache_path = self._get_cache_path('users', cache_key)
            
            if self._is_cache_valid(cache_path, max_age_hours=1):  # Shorter cache for user data
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    logger.debug(f"Retrieved user data from cache for {email}")
                    return data
            
        except Exception as e:
            logger.error(f"Error reading user cache: {e}")
        
        return None
    
    def cache_user_data(self, email: str, user_data: Dict[str, Any]) -> bool:
        """Cache user data for given email"""
        try:
            cache_key = self._get_cache_key(email.lower())
            cache_path = self._get_cache_path('users', cache_key)
            
            cache_data = {
                'email': email,
                'data': user_data,
                'cached_at': datetime.now().isoformat()
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            logger.debug(f"Cached user data for {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching user data: {e}")
            return False
    
    def clear_cache(self, cache_type: Optional[str] = None) -> bool:
        """Clear cache files. If cache_type is None, clears all caches"""
        try:
            if cache_type == 'tasks' or cache_type is None:
                for file in os.listdir(self.tasks_cache_dir):
                    os.remove(os.path.join(self.tasks_cache_dir, file))
                logger.info("Cleared task cache")
            
            if cache_type == 'users' or cache_type is None:
                for file in os.listdir(self.user_cache_dir):
                    os.remove(os.path.join(self.user_cache_dir, file))
                logger.info("Cleared user cache")
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            tasks_count = len(os.listdir(self.tasks_cache_dir))
            users_count = len(os.listdir(self.user_cache_dir))
            
            # Calculate total cache size
            total_size = 0
            for dir_path in [self.tasks_cache_dir, self.user_cache_dir]:
                for file in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file)
                    total_size += os.path.getsize(file_path)
            
            return {
                'tasks_cached': tasks_count,
                'users_cached': users_count,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'cache_dir': self.cache_dir
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {'error': str(e)}