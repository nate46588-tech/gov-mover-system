import os

# ======================
# TELEGRAM (alerts)
# ======================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ======================
# NEWS API
# ======================
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ======================
# CORE FILTERS
# ======================
MIN_AWARD = 50_000_000       # minimum contract size ($50M)
MIN_MCAP = 100_000_000       # $100M
MAX_MCAP = 10_000_000_000    # $10B (small/mid cap focus)

TOP_N = 5                    # number of alerts sent daily

# ======================
# PREMARKET FILTERS
# ======================
MIN_PREMARKET_VOLUME = 100_000
MIN_GAP = 0.02               # 2% move minimum

# ======================
# VOLUME FILTERS
# ======================
MIN_REL_VOL = 1.5            # relative volume threshold
