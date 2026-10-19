import re
from folder import allowed
from by_keyword import keyword_search
from by_meaning import meaning_search

def merge(*lists, k=60):
    """Rank fusion (RRF): it doesn't compare scores."""
    total = {}
    for lst in lists:
        for pos, (doc, _) in enumerate(lst, start=1):
            total[doc] = total.get(doc, 0) + 1 / (k + pos)
    return sorted(total, key=total.get, reverse=True)

def search(question, profile, limit=3):
    docs = allowed(profile)
    order = merge(keyword_search(question, docs),
                  meaning_search(question, docs))
    return [{"id": f"E{n}", "source": d[0], "text": d[1]}
            for n, d in enumerate(order[:limit], 1)]

def answer(question, profile, generate):
    evidence = search(question, profile)
    if not evidence:
        return "NOT FOUND", "I couldn't find that in the folder."
    reply = generate(question, evidence)
    cited = set(re.findall(r"\[(E\d+)\]", reply))
    exist = {e["id"] for e in evidence}
    if not cited or cited - exist:
        return "ANSWER WITHOUT A VALID SOURCE", reply
    return "LABELS OK", reply      # labels exist, nothing more
