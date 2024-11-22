import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / 'common'))

from . import create_flask_app
from settings import FLASK_CONFIG


app = create_flask_app(FLASK_CONFIG)
