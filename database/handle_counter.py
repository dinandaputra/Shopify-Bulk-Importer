import json
import os
from datetime import datetime
from typing import Dict

class HandleCounter:
    """Manages daily counter for handle generation with persistence"""
    
    def __init__(self, counter_file: str = "handle_counter.json"):
        self.counter_file = counter_file
        self.counter_data = self._load_counter()
    
    def _load_counter(self) -> Dict[str, int]:
        """Load counter data from file"""
        if os.path.exists(self.counter_file):
            try:
                with open(self.counter_file, 'r') as f:
                    data = json.load(f)
                    return data
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_counter(self):
        """Save counter data to file"""
        try:
            with open(self.counter_file, 'w') as f:
                json.dump(self.counter_data, f, indent=2)
        except IOError:
            pass  # Fail silently if can't save
    
    def _get_today_key(self) -> str:
        """Get today's date key in YYMMDD format"""
        return datetime.now().strftime("%y%m%d")
    
    def get_next_counter(self) -> int:
        """Get the next counter value for today"""
        today_key = self._get_today_key()
        
        # Initialize today's counter if not exists
        if today_key not in self.counter_data:
            self.counter_data[today_key] = 0
        
        # Increment counter
        self.counter_data[today_key] += 1
        
        # Save to file
        self._save_counter()
        
        return self.counter_data[today_key]
    
    def get_current_counter(self) -> int:
        """Get current counter value for today without incrementing"""
        today_key = self._get_today_key()
        return self.counter_data.get(today_key, 0)
    
    def cleanup_old_counters(self, days_to_keep: int = 30):
        """Clean up old counter data"""
        today = datetime.now()
        keys_to_remove = []
        
        for date_key in self.counter_data.keys():
            try:
                counter_date = datetime.strptime(date_key, "%y%m%d")
                days_diff = (today - counter_date).days
                
                if days_diff > days_to_keep:
                    keys_to_remove.append(date_key)
            except ValueError:
                keys_to_remove.append(date_key)  # Invalid date format
        
        for key in keys_to_remove:
            del self.counter_data[key]
        
        if keys_to_remove:
            self._save_counter()

# Global instance
handle_counter = HandleCounter()