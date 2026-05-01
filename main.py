import pandas as pd
from config import *
from core.contracts import fetch_awards
from core.market import get_data
from core.scoring import score
from core.alerts import send
from core.ticker_resolver import resolve_ticker


def run():
    data = fetch_awards()

    if not data:
        send("No data from USAspending")
        return

    # Sort largest contracts first
    data = sorted(data, key=lambda x: x.get("Award Amount", x.get("award_amount", 0)), reverse=True)

    results = []

    for x in data:

        # Handle API field variations
        company = (x.get("Recipient Name") or x.get("recipient_name") or "").upper().strip()
        amount = x.get("Award Amount") or x.get("award_amount") or 0

        if not company or amount < MIN_AWARD:
            continue

        # 🔑 AUTO TICKER RESOLUTION
        ticker = resolve_ticker(company)

        if not ticker:
            print(f"No ticker match: {company}")
            continue

        # 📊 Market data
        m = get_data(ticker)

        if not m or not m.get("mcap"):
            continue

        if not (MIN_MCAP <= m["mcap"] <= MAX_MCAP):
            continue

        # 🧠 Scoring
        s, r = score(
            amount,
            m["mcap"],
            m["vol_ratio"],
            m["avg_vol"],
            m["float"],
            m["short"]
        )

        if s < 40:
            continue

        msg = f"""
{ticker} | Score: {s}

Company: {company}
Award: ${amount:,.0f}
Impact: {r:.2%}

Float: {m['float']}
Short: {m['short']}
Volume: {m['vol_ratio']:.2f}x
Price: ${m['price']:.2f}
"""

        results.append((s, msg))

    # 📈 Sort best signals
    results.sort(reverse=True)

    if not results:
        send("No strong gov contract signals today")
        return

    final = "🔥 TOP GOV CONTRACT MOVERS\n\n"

    for _, msg in results[:TOP_N]:
        final += msg + "\n-----\n"

    send(final)


if __name__ == "__main__":
    run()
