from control import Run, resume
from runtime import frozen


def simulated_model(seen):
    """Pretends to be the LLM: returns (requests, answer)."""
    if not seen:
        return [("p1", "check_calendar",
                 {"day": "Friday"})], ""
    name, last = seen[-1]
    if not last["ok"]:              # an error is feedback
        return [], f"Sorry, that didn't work: {last['error']}."
    if name == "check_calendar":
        if last["openings"] == 0:
            return [], "Friday is fully booked. Another day?"
        cake = {"product": "carrot cake",
                "day": "Friday"}
        # By mistake, it asks for the same thing twice.
        return [("p2", "record_order", cake),
                ("p3", "record_order", cake)], ""
    return [], f"Order {last['number']} confirmed!"


approved = {}       # request ID -> exactly what was approved
run = Run(session={"customer": "Mrs. Lewis"})
run = resume(run, simulated_model, approved)

while run.state == "BLOCKED":
    req_id, name, args = run.pending[0]
    run.trail.append(f"    >> Rosa approved {req_id}")
    approved[req_id] = (run.session["customer"], name,
                        frozen(args))   # a frozen copy
    run = resume(run, simulated_model, approved)

for line in run.trail:
    print(line)
print("state:", run.state)
print("answer:", run.answer)
