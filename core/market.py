import yfinance as yf

def get_premarket_data(ticker):
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


def get_relative_volume(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")

        if hist is None or hist.empty:
            return None

        avg_vol = hist["Volume"].mean()
        today_vol = hist["Volume"].iloc[-1]

        return today_vol / avg_vol if avg_vol else 0

    except:
        return None
