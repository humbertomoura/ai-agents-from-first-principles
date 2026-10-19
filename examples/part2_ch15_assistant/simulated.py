from tools import TOOLS


def key(name, args):
    # e.g., "check_calendar(day='Saturday')": field names,
    # fixed order, and quoted values. It only indexes
    # results; it is not an idempotency key.
    fields = ", ".join(f"{k}={v!r}"
                       for k, v in sorted(args.items()))
    return f"{name}({fields})"


def dollars(value):
    return f"${value:,.2f}"


def simulated_model(request, seen):
    """Pretends to be the LLM: returns (requests, answer)."""
    if not seen:
        # First round: requests two tools together.
        return [("check_calendar", {"day": "Saturday"}),
                ("check_price",
                 {"product": "carrot cake"})], None
    price = seen["check_price(product='carrot cake')"]
    price = dollars(price["price"])
    if seen["check_calendar(day='Saturday')"]["openings"] > 0:
        return [], f"Saturday is open! It's {price}."
    if "check_calendar(day='Friday')" not in seen:
        return [("check_calendar",
                 {"day": "Friday"})], None
    if seen["check_calendar(day='Friday')"]["openings"] > 0:
        return [], (f"Saturday is booked, but Friday has "
                    f"openings! It's {price}. "
                    f"Want me to put you down?")
    return [], "Friday and Saturday are booked. Another day?"


def run_agent(request, decide, max_rounds=5):
    seen, trail = {}, []
    for rnd in range(1, max_rounds + 1):
        requests, answer = decide(request, seen)
        if not requests:              # the model is done
            state = "SUCCESS" if answer else "FAILURE"
            return state, answer, trail
        for name, args in requests:
            if name in TOOLS:         # simple gate
                result = TOOLS[name](**args)
            else:                     # becomes a notice
                result = {"error": "no such tool"}
            seen[key(name, args)] = result
            line = f"[{rnd}] {key(name, args)}"
            trail.append(f"{line} -> {result}")
    return "LIMIT_REACHED", None, trail


state, answer, trail = run_agent(
    "Do you have carrot cake for Saturday? How much is it?",
    simulated_model)
for line in trail:
    print(line)
print("state:", state)
print("answer:")
print(answer)
