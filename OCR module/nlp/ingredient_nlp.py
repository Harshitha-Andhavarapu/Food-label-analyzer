import re

# Simple correction dictionary (you can expand later)
CORRECTIONS = {
    "giucote": "glucose",
    "oeatrose": "dextrose",
    "modifed": "modified",
    "tapoca": "tapioca",
    "staren": "starch",
    "lactc": "lactic",
    "acia": "acid",
    "acdity": "acidity",
    "requtator": "regulator",
    "celing": "gelling",
    "flavounngs": "flavourings",
    "paprina": "paprika",
    "estract": "extract",
    "coconus": "coconut",
    "patm": "palm",
    "ornel": "kernel"
}

KNOWN_PHRASES = [
    "glucose syrup",
    "invert sugar syrup",
    "modified tapioca starch",
    "modified potato starch",
    "citric acid",
    "lactic acid",
    "acidity regulator",
    "palm kernel oil",
    "coconut oil",
    "paprika extract",
    "fruit and plant concentrates"
]

def correct_words(text):
    words = text.split()
    fixed = []
    for w in words:
        fixed.append(CORRECTIONS.get(w, w))
    return " ".join(fixed)

def clean_ingredients(ocr_ingredients):
    combined = " ".join(ocr_ingredients).lower()
    combined = re.sub(r"[^a-z\s]", " ", combined)
    combined = re.sub(r"\s+", " ", combined)

    # Spell correction
    combined = correct_words(combined)

    final_ingredients = []

    # Phrase extraction
    for phrase in KNOWN_PHRASES:
        if phrase in combined:
            final_ingredients.append(phrase)
            combined = combined.replace(phrase, "")

    # Remaining single ingredients
    leftovers = combined.split()
    for word in leftovers:
        if len(word) > 3 and word not in final_ingredients:
            final_ingredients.append(word)

    return list(set(final_ingredients))
