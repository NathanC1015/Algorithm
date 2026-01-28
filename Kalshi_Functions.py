def kalshi_sizing(m_yes, m_no, cap=100.0):
    # multipliers -> Kalshi prices
    p_yes = 1.0 / m_yes
    p_no  = 1.0 / m_no

    # green possible only if p_yes + p_no < 1
    edge = 1.0 - (p_yes + p_no)
    if edge <= 0:
        return {"green_possible": False, "edge": edge}

    # optimal ratio is Y/N = p_yes/p_no  (equivalently = m_no/m_yes)
    # scale up until one side hits the cap
    t = min(cap / p_yes, cap / p_no)

    Y = t * p_yes   # $ on YES
    N = t * p_no    # $ on NO

    locked_profit = t * edge

    return {
        "green_possible": True,
        "p_yes": p_yes, "p_no": p_no,
        "Y_yes_dollars": Y,
        "N_no_dollars": N,
        "ratio_Y_over_N": Y / N,
        "locked_profit": locked_profit
    }

def tennis_trigger_and_options(entry_mult: float,
                               entry_dollars: float,
                               cap: float = 50.0,
                               buffer: float = 0.0,
                               fav_mult_options=None,
                               n_options: int = 10):
    """
    entry_mult: your underdog entry multiplier (e.g., 2.0 or 3.0)
    entry_dollars: how much you put on the underdog (<= cap)
    cap: max dollars you're willing to put on either side (50)
    buffer: safety margin in probability space (0.01-0.03 recommended)
    fav_mult_options: optional list of favorite multipliers to evaluate (must be > trigger)
    n_options: number of options to return (default 10)
    """

    if entry_mult <= 1.0:
        raise ValueError("entry_mult must be > 1.0")
    if not (0 < entry_dollars <= cap):
        raise ValueError(f"entry_dollars must be in (0, {cap}]")

    # Trigger: favorite multiplier must be >= this to even have a green hedge (ignoring sizing/caps details)
    # Uses probability-space buffer: need 1/entry + 1/fav < 1 - buffer
    p_entry = 1.0 / entry_mult
    p_hedge_max = 1.0 - buffer - p_entry
    if p_hedge_max <= 0:
        return {"trigger": float("inf"), "options": [], "note": "Impossible with this buffer/entry_mult."}

    trigger = 1.0 / p_hedge_max

    # If user didn't provide fav multipliers, generate some above trigger
    # We generate in multiplier-space because that's what you think in.
    if fav_mult_options is None:
        # Make a spread of "above trigger" values; tennis odds can jump, so use a wide range.
        # Starts a bit above trigger to avoid razor-thin edges.
        steps = [0.02, 0.05, 0.10, 0.15, 0.25, 0.40, 0.60, 0.90, 1.30, 1.80]
        fav_mult_options = [trigger + s for s in steps][:n_options]

    options = []
    for fav_mult in fav_mult_options:
        if fav_mult <= trigger:
            continue
        if fav_mult <= 1.0:
            continue

        # Hedge dollar range for green both ways:
        # profit_if_fav = H*(fav_mult-1) - entry_dollars > 0  => H > entry_dollars/(fav_mult-1)
        # profit_if_dog = entry_dollars*(entry_mult-1) - H > 0 => H < entry_dollars*(entry_mult-1)
        hedge_min = entry_dollars / (fav_mult - 1.0)
        hedge_max = min(entry_dollars * (entry_mult - 1.0), cap)

        feasible = hedge_min < hedge_max

        # "Balanced" hedge that equalizes payouts (maximizes worst-case profit when feasible):
        # H_bal = entry_dollars * entry_mult / fav_mult
        hedge_bal = (entry_dollars * entry_mult) / fav_mult

        # clamp balanced hedge into [hedge_min, hedge_max] if feasible
        if feasible:
            hedge_pick = min(max(hedge_bal, hedge_min), hedge_max)
        else:
            hedge_pick = None

        # compute locked profits for the picked hedge (if feasible)
        if hedge_pick is not None:
            profit_if_dog = entry_dollars * (entry_mult - 1.0) - hedge_pick
            profit_if_fav = hedge_pick * (fav_mult - 1.0) - entry_dollars
            locked_profit = min(profit_if_dog, profit_if_fav)
        else:
            profit_if_dog = profit_if_fav = locked_profit = None

        options.append({
            "fav_mult": round(fav_mult, 3),
            "hedge_min_$": round(hedge_min, 2),
            "hedge_max_$": round(hedge_max, 2),
            "feasible_under_cap": feasible,
            "recommended_hedge_$": None if hedge_pick is None else round(hedge_pick, 2),
            "locked_profit_$": None if locked_profit is None else round(locked_profit, 2),
        })

    return {
        "entry_mult": entry_mult,
        "entry_dollars": entry_dollars,
        "cap": cap,
        "buffer": buffer,
        "trigger_fav_mult": round(trigger, 3),
        "options": options[:n_options],
    }

def print_tennis_plan(plan: dict):
    print("\n================ TENNIS HEDGE PLAN ================")
    print(f"Entry: ${plan['entry_dollars']} @ {plan['entry_mult']}x")
    print(f"Favorite hedge trigger: {plan['trigger_fav_mult']}x")
    print("---------------------------------------------------")
    print(f"{'Fav x':>6} | {'Min $':>7} | {'Max $':>7} | {'Rec $':>7} | {'Profit $':>9}")
    print("-" * 52)

    for row in plan["options"]:
        if not row["feasible_under_cap"]:
            continue

        print(
            f"{row['fav_mult']:>6.2f} | "
            f"{row['hedge_min_$']:>7.2f} | "
            f"{row['hedge_max_$']:>7.2f} | "
            f"{row['recommended_hedge_$']:>7.2f} | "
            f"{row['locked_profit_$']:>9.2f}"
        )

    print("===================================================\n")