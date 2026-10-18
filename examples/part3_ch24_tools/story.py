from control import Run, resume


def simulated_model(seen):
    """Pretends to be the LLM: returns (requests, answer)."""
    if not seen:
        return [("p1", "check_calendar",
                 {"day": "Friday"})], ""
    name, last = seen[-1]
    if name == "check_calendar":
        cake = {"product": "carrot cake",
                "day": "Friday"}
        # By mistake, it asks for the same thing twice.
        return [("p2", "record_order", cake),
                ("p3", "record_order", cake)], ""
    return [], f"Order {last['number']} confirmed!"


approved = set()
run = Run(session={"customer": "Mrs. Lewis"})
run = resume(run, simulated_model, approved)

while run.state == "BLOCKED":
    req_id = run.pending[0][0]
    run.trail.append(f"    >> Rosa approved {req_id}")
    approved.add(req_id)       # human approval
    run = resume(run, simulated_model, approved)

for line in run.trail:
    print(line)
print("state:", run.state)
print("answer:", run.answer)
