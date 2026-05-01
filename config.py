# ===== TELEGRAM =====
TELEGRAM_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

# ===== NEWS API =====
NEWS_API_KEY = os.getenv("NEWS_API_KEY") 

# ===== FILTERS =====
MIN_AWARD = 50_000_000      # minimum contract size
MIN_MCAP = 100_000_000     # 100M
MAX_MCAP = 10_000_000_000  # 10B

TOP_N = 5                  # number of alerts to send

# ===== PREMARKET FILTERS =====
MIN_PREMARKET_VOLUME = 100_000
MIN_GAP = 0.02

# ===== RELATIVE VOLUME =====
MIN_REL_VOL = 1.5
