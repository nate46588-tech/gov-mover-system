import pandas as pd
from config import *
from core.contracts import fetch_awards
from core.market import get_data
from core.scoring import score
from core.alerts import send

from core.ticker_resolver import resolve_ticker

ticker = resolve_ticker(company)

if not ticker:
    continue
    
mapping["company"] = mapping["company"].str.upper().str.strip()

def run():
    data = fetch_awards()

    data = sorted(data, key=lambda x: x.get("Award Amount", 0), reverse=True)

    results = []

    for x in data:
        company = x.get("Recipient Name", "").upper().strip()
        amount = x.get("Award Amount", 0)
        
        ticker = resolve_ticker(company)

        if not ticker:
            continue
       
        if amount < MIN_AWARD:
            continue


        m = get_data(ticker)
        if not m or not m["mcap"]:
            continue

        if not (MIN_MCAP <= m["mcap"] <= MAX_MCAP):
            continue

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

Award: ${amount:,.0f}
Impact: {r:.2%}

Float: {m['float']}
Short: {m['short']}
Volume: {m['vol_ratio']:.2f}x
Price: ${m['price']:.2f}
"""

        results.append((s, msg))

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
