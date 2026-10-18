from dataclasses import dataclass

CAPACITY = 5
CALENDAR = {"Friday": 2, "Saturday": 5}  # already booked
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


def validate_day(args):
    if args.get("day") not in CALENDAR:
        return "invalid day"


def validate_order(args):
    if validate_day(args):
        return "invalid day"
    if CALENDAR[args["day"]] >= CAPACITY:
        return "day fully booked"


def order_intention(args, session):
    # Same customer + same product + same day =
    # same intention, no matter how many times
    # the model asks.
    return "|".join([session["customer"],
                     args["product"], args["day"]])


# ---------- the registry ----------
@dataclass(frozen=True)
class Tool:
    run: object
    validate: object
    read_only: bool
    needs_approval: bool = False
    intention: object = None


REGISTRY = {
    "check_calendar": Tool(
        check_calendar, validate_day, read_only=True),
    "record_order": Tool(
        record_order, validate_order,
        read_only=False, needs_approval=True,
        intention=order_intention),
}


# ---------- the executor ----------
def execute(name, args, session, request_id, approved):
    t = REGISTRY.get(name)
    if t is None:
        return {"ok": False, "error": "NO_SUCH_TOOL"}
    key = None
    if t.intention:
        key = t.intention(args, session)
    if key in ALREADY_DONE:         # already done?
        return {"ok": True, **ALREADY_DONE[key],
                "repeated": True}
    problem = t.validate(args)      # form and meaning
    if problem:
        return {"ok": False, "error": problem}
    if t.needs_approval and request_id not in approved:
        return {"ok": False, "error": "NEEDS_APPROVAL"}
    result = t.run(args, session)
    if key:
        ALREADY_DONE[key] = result
    return {"ok": True, **result}
