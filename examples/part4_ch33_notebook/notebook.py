import re
import sqlite3

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
db.execute("""create table notebook (
    id integer primary key, customer text, topic text,
    text text, source text, until text,
    active integer default 1, replaces integer)""")

SECRET = re.compile(
    r"(?i)(password|\bpin\b|cvv"
    r"|\d{4}[ .-]?\d{4}[ .-]?\d{4})")
LOOKS_LIKE_RULE = re.compile(
    r"(?i)(ignor|authoriz|without approval|discount)")


def add_note(customer, topic, text, source, until=None):
    """Write gate: decides what gets in."""
    if SECRET.search(text):
        return "BLOCKED (secret)"
    if LOOKS_LIKE_RULE.search(text):
        return "BLOCKED (looks like a rule, not a fact)"
    current = db.execute(
        "select * from notebook where customer=? and "
        "topic=? and active=1", (customer, topic)
    ).fetchone()
    if current and current["text"] == text:
        return "NOTHING TO DO"
    old = None
    if current:                 # don't delete: replace
        old = current["id"]
        db.execute(
            "update notebook set active=0 where id=?",
            (old,))
    db.execute(
        "insert into notebook (customer, topic, text, "
        "source, until, replaces) values (?,?,?,?,?,?)",
        (customer, topic, text, source, until, old))
    return "UPDATED" if old else "NEW"
