import configparser
import os
 
class UtilService:
    def load_coldplay_config():
        config_dest = os.path.expanduser('~/.coldplay_config.ini')
        
        if not os.path.exists(config_dest):
            print("Config file not found. Please run coldplayagent-init first.")
            return None
        
        coldplay_config = configparser.ConfigParser()
        coldplay_config.read(config_dest)
        return coldplay_config
    