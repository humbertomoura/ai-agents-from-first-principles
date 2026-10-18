from dataclasses import dataclass, field
from runtime import execute


@dataclass
class Run:
    session: dict                 # who the customer is
    seen: list = field(default_factory=list)
    pending: list = field(default_factory=list)
    trail: list = field(default_factory=list)
    state: str = "READY"
    answer: str = ""
    rounds: int = 0


def summarize(r):
    if not r["ok"]:
        return r["error"]
    extra = " (repeated)" if r.get("repeated") else ""
    data = {k: v for k, v in r.items()
            if k not in ("ok", "repeated")}
    return f"{data}{extra}"


def resume(run, decide, approved, max_rounds=6):
    run.state = "RUNNING"
    while run.rounds < max_rounds:
        if not run.pending:             # ask the model
            requests, answer = decide(run.seen)
            if not requests:
                run.state = "SUCCESS"
                run.answer = answer
                return run
            run.pending = list(requests)
        while run.pending:              # execute in order
            req_id, name, args = run.pending[0]
            r = execute(name, args, run.session, req_id,
                        approved)
            rnd = run.rounds + 1
            run.trail.append(
                f"[{rnd}] {req_id} {name}: {summarize(r)}")
            if r.get("error") == "NEEDS_APPROVAL":
                run.state = "BLOCKED"   # stop and wait
                return run
            run.seen.append((name, r))
            run.pending.pop(0)
        run.rounds += 1
    run.state = "LIMIT_REACHED"
    return run
