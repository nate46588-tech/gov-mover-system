def sigmoid(x):
    import math
    return 1 / (1 + math.exp(-x))


def open_move_probability(
    gap,
    rel_vol,
    amount,
    mcap,
    float_shares,
    short_interest,
    has_news,
    has_sec
):
    """
    Returns probability (0–100%) of stock moving at open
    """

    score = 0

    # ===== GAP (strongest signal)
    score += gap * 8

    # ===== RELATIVE VOLUME
    score += min(rel_vol, 5) * 1.5

    # ===== CONTRACT IMPACT
    impact = amount / mcap if mcap else 0
    score += impact * 10

    # ===== FLOAT (lower = more explosive)
    if float_shares:
        if float_shares < 20_000_000:
            score += 2
        elif float_shares < 50_000_000:
            score += 1

    # ===== SHORT INTEREST
    if short_interest:
        if short_interest > 5:
            score += 2

    # ===== CATALYSTS
    if has_news:
        score += 2

    if has_sec:
        score += 2

    # convert to probability
    prob = sigmoid(score)

    return round(prob * 100, 2)
