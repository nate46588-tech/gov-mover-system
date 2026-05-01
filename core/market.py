import yfinance as yf


# =========================
# BASIC MARKET DATA
# =========================
def get_data(ticker):
    """
    Core stock fundamentals:
    price, market cap, float, short interest, volume
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        hist = stock.history(period="5d")

        if not info:
            return None

        price = info.get("regularMarketPrice") or info.get("currentPrice")
        mcap = info.get("marketCap")
        float_shares = info.get("floatShares")
        short_ratio = info.get("shortRatio")

        avg_vol = hist["Volume"].mean() if not hist.empty else 0
        last_vol = hist["Volume"].iloc[-1] if not hist.empty else 0

        vol_ratio = last_vol / avg_vol if avg_vol else 0

        return {
            "price": price or 0,
            "mcap": mcap or 0,
            "float": float_shares or 0,
            "short": short_ratio or 0,
            "avg_vol": avg_vol or 0,
            "vol_ratio": vol_ratio
        }

    except:
        return None


# =========================
# PREMARKET DATA
# =========================
def get_premarket_data(ticker):
    """
    Detect premarket gap + volume
    """
    try:
        stock = yf.Ticker(ticker)

        hist = stock.history(period="2d", interval="5m", prepost=True)

        if hist is None or hist.empty:
            return None

        latest = hist.iloc[-1]
        prev_close = hist["Close"].iloc[0]

        price = latest["Close"]
        volume = hist["Volume"].sum()

        gap = (price - prev_close) / prev_close if prev_close else 0

        return {
            "premarket_price": price,
            "premarket_volume": volume,
            "gap": gap
        }

    except:
        return None


# =========================
# RELATIVE VOLUME
# =========================
def get_relative_volume(ticker):
    """
    Measures abnormal trading activity
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")

        if hist is None or hist.empty:
            return None

        avg_vol = hist["Volume"].mean()
        today_vol = hist["Volume"].iloc[-1]

        if avg_vol == 0:
            return None

        return today_vol / avg_vol

    except:
        return None
