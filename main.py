from config import *
from core.contracts import fetch_awards
from core.market import get_data, get_premarket_data, get_relative_volume
from core.scoring import score
from core.alerts import send
from core.ticker_resolver import resolve_ticker
from core.sec import get_sec_filings
from core.news_api import get_news_api


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

        # 🔑 ticker match
        ticker = resolve_ticker(company)

        if not ticker:
            print(f"No ticker match: {company}")
            continue

        # 📊 market data
        m = get_data(ticker)

        if not m or not m.get("mcap"):
            continue

        if not (MIN_MCAP <= m["mcap"] <= MAX_MCAP):
            continue

        # 📈 premarket
        pm = get_premarket_data(ticker)

        if not pm:
            continue

        if pm["premarket_volume"] < MIN_PREMARKET_VOLUME:
            continue

        if abs(pm["gap"]) < MIN_GAP:
            continue

        # 📊 relative volume
        rel_vol = get_relative_volume(ticker)

        if not rel_vol or rel_vol < MIN_REL_VOL:
            continue

        # 📄 SEC filings
        sec = get_sec_filings(ticker)

        # 📰 news
        news = get_news_api(company)

        # require at least one catalyst
        if not sec and not news:
            continue

        # 🧠 scoring
        s, r = score(
            amount,
            m["mcap"],
            m["vol_ratio"],
            m["avg_vol"],
            m["float"],
            m["short"]
        )

        # 🚀 boosts
        if pm["gap"] > 0.03:
            s += 20

        if pm["premarket_volume"] > 300_000:
            s += 15

        if rel_vol > 2:
            s += 20
        elif rel_vol > 1.5:
            s += 10

        if sec:
            s += 25

        if news:
            s += 15

        if s < 50:
            continue

        # 📨 message
        msg = f"""
{ticker} | Score: {s}

Company: {company}
Award: ${amount:,.0f}
Impact: {r:.2%}

Premarket Gap: {pm['gap']:.2%}
Premarket Volume: {pm['premarket_volume']}
Rel Volume: {rel_vol:.2f}x

SEC Filings: {len(sec) if sec else 0}
News: {news}

Float: {m['float']}
Short: {m['short']}
Volume: {m['vol_ratio']:.2f}x
Price: ${m['price']:.2f}
"""

        results.append((s, msg))

    # sort best setups
    results.sort(reverse=True)

    if not results:
        send("No strong multi-catalyst signals today")
        return

    final = "🔥 TOP PRE-MARKET MOVERS\n\n"

    for _, msg in results[:TOP_N]:
        final += msg + "\n-----\n"

    send(final)


if __name__ == "__main__":
    run()
