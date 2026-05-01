from config import *
from core.contracts import fetch_awards
from core.market import get_data, get_premarket_data, get_relative_volume
from core.scoring import score
from core.alerts import send
from core.ticker_resolver import resolve_ticker
from core.sec import get_sec_filings
from core.news_api import get_news_api
from core.probability import open_move_probability


def run():
    data = fetch_awards()

    if not data:
        send("No data from USAspending")
        return

    # sort biggest contracts first
    data = sorted(
        data,
        key=lambda x: x.get("Award Amount", x.get("award_amount", 0)),
        reverse=True
    )

    results = []

    for x in data:

        # normalize fields
        company = (x.get("Recipient Name") or x.get("recipient_name") or "").upper().strip()
        amount = x.get("Award Amount") or x.get("award_amount") or 0

        if not company or amount < MIN_AWARD:
            continue

        # resolve ticker
        ticker = resolve_ticker(company)

        if not ticker:
            print(f"No ticker match: {company}")
            continue

        # market data
        m = get_data(ticker)

        if not m or not m.get("mcap"):
            continue

        if not (MIN_MCAP <= m["mcap"] <= MAX_MCAP):
            continue

        # premarket
        pm = get_premarket_data(ticker)

        if not pm:
            continue

        if pm["premarket_volume"] < MIN_PREMARKET_VOLUME:
            continue

        if abs(pm["gap"]) < MIN_GAP:
            continue

        # relative volume
        rel_vol = get_relative_volume(ticker)

        if not rel_vol or rel_vol < MIN_REL_VOL:
            continue

        # SEC + news
        sec = get_sec_filings(ticker)
        news = get_news_api(company)

        # require at least one catalyst
        if not sec and not news:
            continue

        # base score (kept for reference)
        s, r = score(
            amount,
            m["mcap"],
            m["vol_ratio"],
            m["avg_vol"],
            m["float"],
            m["short"]
        )

        # probability model
        prob = open_move_probability(
            pm["gap"],
            rel_vol,
            amount,
            m["mcap"],
            m["float"],
            m["short"],
            bool(news),
            bool(sec)
        )

        # filter by probability
        if prob < 60:
            continue

        # build message
        msg = f"""
🚀 OPEN MOVE PROBABILITY: {prob}%

Ticker: {ticker}
Company: {company}

💰 Contract: ${amount:,.0f}
📊 Impact Score: {r:.2%}

⚡ Premarket
Gap: {pm['gap']:.2%}
Volume: {pm['premarket_volume']}
Rel Vol: {rel_vol:.2f}x

📰 Catalysts
SEC Filings: {len(sec) if sec else 0}
News: {news or "None"}

📉 Structure
Float: {m['float']}
Short Interest: {m['short']}
Volume Ratio: {m['vol_ratio']:.2f}x
Price: ${m['price']:.2f}
"""

        results.append((prob, msg))

    # sort highest probability first
    results.sort(reverse=True)

    if not results:
        send("No strong open-move candidates today")
        return

    final = "🔥 TOP PRE-MARKET OPEN MOVERS\n\n"

    for _, msg in results[:TOP_N]:
        final += msg + "\n-----\n"

    send(final)


if __name__ == "__main__":
    run()
