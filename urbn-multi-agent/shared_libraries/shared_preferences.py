import json
import os
from appdirs import user_data_dir


class SharedPreferences:
    def __init__(self, app_name, app_author):
        # Get platform-specific app data directory
        self.data_dir = user_data_dir(app_name, app_author)
        self.pref_file = os.path.join(self.data_dir, "preferences.json")
        self.prefs = {}
        
        # Create directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Load existing preferences
        self.load()
    
    def load(self):
        """Load preferences from the JSON file."""
        if os.path.exists(self.pref_file):
            try:
                with open(self.pref_file, 'r') as f:
                    self.prefs = json.load(f)
            except (json.JSONDecodeError, IOError):
                # Reset preferences if file is corrupted
                self.prefs = {}
    
    def save(self):
        """Save preferences to the JSON file."""
        with open(self.pref_file, 'w') as f:
            json.dump(self.prefs, f)
    
    def put_string(self, key, value):
        """Store a string value."""
        self.prefs[key] = str(value)
        self.save()
    
    def put_int(self, key, value):
        """Store an integer value."""
        self.prefs[key] = int(value)
        self.save()
    
    def put_float(self, key, value):
        """Store a float value."""
        self.prefs[key] = float(value)
        self.save()
    
    def put_bool(self, key, value):
        """Store a boolean value."""
        self.prefs[key] = bool(value)
        self.save()
    
    def put_list(self, key, value):
        """Store a list value."""
        self.prefs[key] = list(value)
        self.save()
    
    def put_dict(self, key, value):
        """Store a dictionary value."""
        self.prefs[key] = dict(value)
        self.save()
    
    def get_string(self, key, default=""):
        """Retrieve a string value."""
        return str(self.prefs.get(key, default))
    
    def get_int(self, key, default=0):
        """Retrieve an integer value."""
        return int(self.prefs.get(key, default))
    
    def get_float(self, key, default=0.0):
        """Retrieve a float value."""
        return float(self.prefs.get(key, default))
    
    def get_bool(self, key, default=False):
        """Retrieve a boolean value."""
        return bool(self.prefs.get(key, default))
    
    def get_list(self, key, default=None):
        """Retrieve a list value."""
        if default is None:
            default = []
        return self.prefs.get(key, default)
    
    def get_dict(self, key, default=None):
        """Retrieve a dictionary value."""
        if default is None:
            default = {}
        return self.prefs.get(key, default)
    
    def contains(self, key):
        """Check if a key exists in preferences."""
        return key in self.prefs
    
    def remove(self, key):
        """Remove a key from preferences."""
        if key in self.prefs:
            del self.prefs[key]
            self.save()
            return True
        return False
    
    def clear(self):
        """Clear all preferences."""
        self.prefs = {}
        self.save()
    
    def get_all(self):
        """Get all preferences as a dictionary."""
        return self.prefs.copy()