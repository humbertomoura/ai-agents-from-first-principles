import json
from dataclasses import dataclass

CAPACITY = 5
CALENDAR = {"Friday": 2, "Saturday": 5}  # already booked
PRODUCTS = ("carrot cake", "chocolate cake")
ORDERS = {}                     # number -> data
ALREADY_DONE = {}               # intention -> result


# ---------- the tools ----------
def check_calendar(args, session):
    return {"openings": CAPACITY - CALENDAR[args["day"]]}


def record_order(args, session):
    number = f"ORD-{len(ORDERS) + 1:03d}"
    customer = session["customer"]  # comes from the session
    ORDERS[number] = {**args, "customer": customer}
    CALENDAR[args["day"]] += 1
    return {"number": number}


# ---------- the rules ----------
def check_form(args, fields):
    """Form: exactly the expected fields, each one
    holding one of the allowed values."""
    if not isinstance(args, dict) or set(args) != set(fields):
        return "invalid fields"
    for name, allowed in fields.items():
        if args[name] not in allowed:
            return f"invalid {name}"


def day_has_room(args):
    # Meaning: a business rule that changes over time.
    if CALENDAR[args["day"]] >= CAPACITY:
        return "day fully booked"


def order_intention(args, session):
    # Teaching simplification: same customer + same
    # product + same day this week = same intention.
    # A real system gives each new order an operation
    # ID and reuses that ID on retries.
    return (session["customer"], args["product"],
            args["day"])


def frozen(args):
    """A canonical, unchangeable copy of the arguments."""
    return json.dumps(args, sort_keys=True)


# ---------- the registry ----------
@dataclass(frozen=True)
class Tool:
    run: object
    fields: dict                # field -> allowed values
    read_only: bool
    precondition: object = None
    needs_approval: bool = False
    intention: object = None


DAYS = tuple(CALENDAR)
REGISTRY = {
    "check_calendar": Tool(
        check_calendar, {"day": DAYS}, read_only=True),
    "record_order": Tool(
        record_order, {"day": DAYS, "product": PRODUCTS},
        read_only=False, precondition=day_has_room,
        needs_approval=True, intention=order_intention),
}


# ---------- the executor ----------
def execute(name, args, session, request_id, approved):
    t = REGISTRY.get(name)
    if t is None:
        return {"ok": False, "error": "NO_SUCH_TOOL"}
    problem = check_form(args, t.fields)      # 1. form
    if problem:
        return {"ok": False, "error": problem}
    key = t.intention(args, session) if t.intention else None
    if key in ALREADY_DONE:                   # 2. done?
        return {"ok": True, **ALREADY_DONE[key],
                "repeated": True}
    if t.precondition:                        # 3. meaning
        problem = t.precondition(args)
        if problem:
            return {"ok": False, "error": problem}
    proposal = (session["customer"], name, frozen(args))
    if (t.needs_approval                      # 4. approval
            and approved.get(request_id) != proposal):
        return {"ok": False, "error": "NEEDS_APPROVAL"}
    result = t.run(args, session)
    if key:
        ALREADY_DONE[key] = result
    return {"ok": True, **result}
