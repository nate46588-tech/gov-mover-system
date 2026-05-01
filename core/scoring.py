def score(amount, mcap, vol_ratio, avg_vol, flt, short):
    s = 0
    r = amount / mcap if mcap else 0

    if r > 0.1: s += 40
    elif r > 0.05: s += 30
    elif r > 0.02: s += 20

    if vol_ratio > 3: s += 25
    elif vol_ratio > 2: s += 15

    if flt and flt < 30_000_000: s += 25
    elif flt and flt < 80_000_000: s += 15

    if short and short > 0.20: s += 25
    elif short and short > 0.10: s += 15

    if avg_vol and avg_vol < 500_000: s += 10

    return s, r
