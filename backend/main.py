from backend.config import Settings
from backend.setup import setup_app

settings = Settings()
app = setup_app(settings)
