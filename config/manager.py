# config/manager.py
"""Configuration management for Chrommin"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

class ConfigManager:
    """Manage application configuration"""
    
    DEFAULT_CONFIG = {
        'num_bots': 5,
        'headless': False,
        'viewport': {'width': 1280, 'height': 720},
        'ws_host': 'localhost',
        'ws_port': 8765,
        'enable_extensions': True,
        'anti_detection': True,
        'humanize_inputs': True,
        'wallet_automation': True,
        'profiles_dir': 'profiles',
        'extensions_dir': 'extensions'
    }
    
    @classmethod
    def load_config(cls) -> 'ConfigManager':
        """Load configuration from file or use defaults"""
        config_path = Path('config.json')
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = {**cls.DEFAULT_CONFIG, **json.load(f)}
        else:
            config_data = cls.DEFAULT_CONFIG
            
        return cls(config_data)
        
    def __init__(self, config_data: Dict[str, Any]):
        self._data = config_data
        
    def __getattr__(self, name: str):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Configuration '{name}' not found")
        
    def get_extension_paths(self) -> List[str]:
        """Get paths to browser extensions"""
        ext_dir = Path(self.extensions_dir)
        if not ext_dir.exists():
            return []
            
        return [str(p) for p in ext_dir.iterdir() if p.is_dir() or p.suffix == '.crx']
        
    def save(self):
        """Save configuration to file"""
        config_path = Path('config.json')
        with open(config_path, 'w') as f:
            json.dump(self._data, f, indent=2)