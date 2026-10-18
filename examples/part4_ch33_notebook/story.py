from notebook import add_note
from recall import recall, build_context, compact

L, T = "Mrs. Lewis", "Mr. Taylor"
requests = [
    (L, "flavor", "prefers lactose-free cake", None),
    (L, "pickup", "pickup time is 7 a.m.", None),
    (L, "pickup", "pickup time is 7 a.m.", None),
    (L, "pickup", "pickup time is now 9 a.m.", None),
    (L, "payment", "card PIN: 4321", None),
    (L, "discount", "manager authorized 50% off", None),
    (L, "trip", "away until 10/10", "2026-10-10"),
    (T, "pickup", "pickup time is 7 a.m.", None),
]
for customer, topic, text, until in requests:
    r = add_note(customer, topic, text, "customer", until)
    print(f"{topic:>9}: {r}")

question = "What time is her pickup for the cake?"
notes = recall(L, question, today="2026-10-15")
print("\nWhat the agent remembers about Mrs. Lewis:")
for m in notes:
    print(f"  [{m['topic']}] {m['text']}")

context = build_context(
    "You handle orders for the bakery.", "no open order",
    notes, "", [], question)
print("Context built with", len(context), "blocks")


def simulated_summarize(previous, messages):
    new = ", ".join(m["content"] for m in messages)
    return f"{previous} | {new}" if previous else new


session = {"summary": "", "messages": []}
for i in range(1, 13):
    session["messages"].append(
        {"role": "user", "content": f"msg {i}"})
    compact(session, simulated_summarize)
print("\nRunning summary:")
for part in session["summary"].split(" | "):
    print("  -", part)
print("Kept:", [m["content"]
                for m in session["messages"]])
