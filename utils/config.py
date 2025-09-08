import os
from dotenv import load_dotenv

load_dotenv()

# --- Entorno y URLs ---
BASE_URL = os.getenv("BASE_URL", "https://default-url.com")

# --- Timeouts (en milisegundos) ---
DEFAULT_TIMEOUT = 30000
DEFAULT_NAVIGATION_TIMEOUT = 30000

# --- Configuración del Navegador ---
IS_HEADLESS = os.getenv("HEADLESS", "True").lower() in ('true', '1', 't')
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

# --- Configuración del Viewport ---
DEFAULT_VIEWPORT_WIDTH = 1280
DEFAULT_VIEWPORT_HEIGHT = 720