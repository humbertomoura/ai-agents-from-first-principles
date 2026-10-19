import math
import re
import unicodedata
from collections import Counter

# Words that show up everywhere and don't help the search
STOP_WORDS = {"a", "an", "the", "of", "in", "on", "at", "to", "for",
              "is", "are", "was", "does", "do", "if", "and", "or",
              "by", "per", "be", "it", "there", "who", "what",
              "how", "before"}

def words(text):
    """Lowercase, no accents, most punctuation removed
    (hyphens inside codes like FX-200 stay), no stop words."""
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode().lower()
    return [w for w in re.findall(r"\w+(?:[.-]\w+)*", t)
            if w not in STOP_WORDS]

# Rosa's folder, already cut into chunks
FOLDER = [
    ("carrot-recipe",
     "Carrot cake: bake for 40 minutes at 350 degrees Fahrenheit.",
     "everyone"),
    ("oven-manual",
     "Preheat the FX-200 oven for 15 minutes before baking.",
     "everyone"),
    ("food-code",
     "Eggs must be kept refrigerated, per the FDA Food Code.",
     "everyone"),
    ("flour-contract",
     "Late flour deliveries carry a 2% penalty.",
     "manager"),
]

def allowed(profile):
    """Access filter: runs before any scoring."""
    return [d for d in FOLDER
            if d[2] == "everyone" or profile == "manager"]
