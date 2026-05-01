import yfinance as yf

def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="10d")

        if hist.empty:
            return None

        avg_vol = hist["Volume"][:-1].mean()
        vol_ratio = hist["Volume"].iloc[-1] / avg_vol if avg_vol else 0

        return {
            "mcap": info.get("marketCap"),
            "float": info.get("floatShares"),
            "short": info.get("shortPercentOfFloat"),
            "avg_vol": avg_vol,
            "vol_ratio": vol_ratio,
            "price": hist["Close"].iloc[-1]
        }
    except:
        return None
