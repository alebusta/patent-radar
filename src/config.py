"""
Strategic Patent Radar — Configuration
QaiLabs / AREA_51 / patent_radar
"""

import os

# === Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# === Google Patents Search ===
GOOGLE_PATENTS_SEARCH_URL = "https://patents.google.com/"
GOOGLE_PATENTS_RESULT_URL = "https://patents.google.com/patent/{patent_id}"

# === HTTP Headers (Anti-blocking) ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
]

HEADERS_BASE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# === Rate Limiting ===
REQUEST_DELAY_MIN = 2.0  # seconds
REQUEST_DELAY_MAX = 4.0  # seconds

# === Default Search Queries (Walmart Vertical) ===
DEFAULT_QUERIES = {
    "drones_ultima_milla": '"drone delivery" OR "last mile drone" OR "autonomous delivery"',
    "robotica_warehouse": '"warehouse robotics" OR "automated inventory" OR "robotic picking"',
    "retail_media": '"retail media" OR "point of sale personalization" OR "in-store analytics"',
    "sostenibilidad": '"sustainable packaging" OR "circular economy retail" OR "carbon footprint supply chain"',
    "fintech_checkout": '"frictionless checkout" OR "contactless payment" OR "autonomous store"',
}

# === Extraction Limits ===
MAX_RESULTS_PER_QUERY = 20
MAX_PAGES = 2  # Each page has ~10 results
