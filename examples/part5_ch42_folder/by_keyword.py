from folder import words, math, Counter

def keyword_search(question, docs, k1=1.5, b=0.75):
    """Simplified BM25, only over the allowed chunks."""
    texts = [words(d[1]) for d in docs]
    if not texts:
        return []
    avg = sum(map(len, texts)) / len(texts)
    df = Counter(w for t in texts for w in set(t))
    n, scores = len(texts), []
    for doc, t in zip(docs, texts):
        tf, score = Counter(t), 0.0
        for w in words(question):
            if tf[w]:
                idf = math.log(1 + (n - df[w] + .5)
                               / (df[w] + .5))
                norm = 1 - b + b * len(t) / avg
                score += (idf * tf[w] * (k1 + 1)
                          / (tf[w] + k1 * norm))
        if score > 0:
            scores.append((doc, score))
    return sorted(scores, key=lambda x: -x[1])
