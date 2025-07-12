import os

# Get absolute path to project root (one level up from app/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to assets directory inside app/
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'app', 'assets')

# Path to icons folder
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')

# Path to images folder
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
