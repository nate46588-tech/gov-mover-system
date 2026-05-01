import yfinance as yf
from difflib import get_close_matches

# small fallback universe (you can expand later)
COMMON_TICKERS = [
    "LDOS","CACI","SAIC","BAH","RTX","LMT","NOC",
    "AAPL","MSFT","AMZN","GOOGL","NVDA"
]

def resolve_ticker(company_name):
    """
    Try to map a company name → ticker using fuzzy matching + validation
    """

    if not company_name:
        return None

    name = company_name.upper().strip()

    # Step 1: fuzzy match against known tickers (fast path)
    match = get_close_matches(name, COMMON_TICKERS, n=1, cutoff=0.3)

    if match:
        return match[0]

    # Step 2: brute validation via yfinance search behavior
    for ticker in COMMON_TICKERS:
        try:
            info = yf.Ticker(ticker).info
            long_name = (info.get("longName") or "").upper()

            if long_name and name in long_name:
                return ticker
        except:
            continue

    return None
