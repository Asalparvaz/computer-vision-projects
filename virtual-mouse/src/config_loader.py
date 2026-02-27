import yaml
import pyautogui
from pathlib import Path

class Config:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        current_dir = Path(__file__).parent
        root_dir = current_dir.parent

        config_path = root_dir / 'config.yaml'
        example_path = root_dir / 'config.example.yaml'
        
        # Try to load user config
        if config_path.exists():
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            print(f"✅ Loaded configuration from {config_path}")
        elif example_path.exists():
            # Fallback to example if no config exists
            with open(example_path, 'r') as f:
                self._config = yaml.safe_load(f)
            print(f"⚠️  No config.yaml found, using {example_path} as fallback")
            print("   Run: cp config.example.yaml config.yaml to customize")
        else:
            # Ultimate fallback - hardcoded defaults
            self._config = self._get_default_config()
            print("⚠️  No config files found, using hardcoded defaults")
        
        # Process dynamic values
        self._process_dynamic_values()
    
    def _get_default_config(self):
        return {
            'camera': {'device_id': 1, 'width': 640, 'height': 480},
            'screen': {'width': None, 'height': None},
            'mouse': {
                'smoothening': 3,
                'click_length_threshold': 30,
                'drag_length_threshold': 90,
                'click_delay': 0.3,
                'double_click_timeout': 0.4
            },
            'scroll': {'speed': 100, 'deadzone': 20, 'cooldown': 0.05},
            'crop': {'horizontal': 100, 'top': 50, 'bottom': 150}
        }
    
    def _process_dynamic_values(self):
        # Auto-detect screen size if not specified
        if self._config['screen'].get('width') is None or self._config['screen'].get('height') is None:
            screen_width, screen_height = pyautogui.size()
            self._config['screen']['width'] = self._config['screen'].get('width') or screen_width
            self._config['screen']['height'] = self._config['screen'].get('height') or screen_height

    def get(self, *keys, default=None):
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default
    
    @property
    def camera(self):
        return self._config.get('camera', {})
    
    @property
    def mouse(self):
        return self._config.get('mouse', {})
    
    @property
    def scroll(self):
        return self._config.get('scroll', {})
    
    @property
    def crop(self):
        return self._config.get('crop', {})
    
    @property
    def screen_width(self):
        return self._config['screen']['width']
    
    @property
    def screen_height(self):
        return self._config['screen']['height']

# Create a global config instance
config = Config()

def get_config():
    return config