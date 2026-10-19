from folder import words

# "Toy embedding": related words land on the same
# concept.
CONCEPTS = {
    "time": {"time", "minutes", "long", "takes"},
    "oven": {"oven", "bake", "baking", "preheat"},
    "heat": {"temperature", "degrees", "hot"},
    "cold": {"refrigerator", "refrigerated", "chilled"},
    "penalty": {"penalty", "fine", "late", "delay"},
}

def concepts(text):
    ws = set(words(text))
    return {c for c, group in CONCEPTS.items()
            if ws & group}

def meaning_search(question, docs):
    q = concepts(question)
    scores = []
    for doc in docs:
        d = concepts(doc[1])
        if q and d and q & d:
            score = len(q & d) / (len(q) * len(d)) ** .5
            scores.append((doc, score))
    return sorted(scores, key=lambda x: -x[1])
