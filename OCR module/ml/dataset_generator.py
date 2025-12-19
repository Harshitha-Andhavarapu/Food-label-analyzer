import json
import random
import pandas as pd

# ---------- LOAD INGREDIENT RISK DATA ----------
with open("data/ingredient_risk.json") as f:
    INGREDIENT_RISK = json.load(f)

HIGH_RISK = [k for k, v in INGREDIENT_RISK.items() if v["risk"] == "high"]
MEDIUM_RISK = [k for k, v in INGREDIENT_RISK.items() if v["risk"] == "medium"]
LOW_RISK = [k for k, v in INGREDIENT_RISK.items() if v["risk"] == "low"]

# ---------- FEATURE EXTRACTION ----------
def extract_features(ingredients, nutrition):
    features = {
        "high_risk_count": 0,
        "medium_risk_count": 0,
        "low_risk_count": 0,
        "sugar_present": 0,
        "oil_present": 0,
        "additives_count": 0,

        # ✅ POSITIVE FEATURES
        "protein_sources": 0,
        "spice_count": 0,
        "natural_ingredient_count": 0,

        # nutrition
        "total_fat": nutrition["fat"],
        "sodium": nutrition["sodium"],
        "protein": nutrition["protein"]
    }

    for ing in ingredients:
        ing = ing.lower()

        if ing in INGREDIENT_RISK:
            risk = INGREDIENT_RISK[ing]["risk"]

            if risk == "high":
                features["high_risk_count"] += 1
            elif risk == "medium":
                features["medium_risk_count"] += 1
            else:
                features["low_risk_count"] += 1
                features["natural_ingredient_count"] += 1

            benefit = INGREDIENT_RISK[ing].get("benefit")

            if benefit in ["protein", "protein_fat"]:
             features["protein_sources"] += 1
        elif benefit in ["antioxidant", "digestive"]:
             features["spice_count"] += 1

        else:
            features["additives_count"] += 1

        if "sugar" in ing:
            features["sugar_present"] = 1
        if "oil" in ing:
            features["oil_present"] = 1

    return features

# ---------- RULE-BASED HEALTH SCORE ----------
def rule_based_score(features):
    score = 70

    # penalties (lighter)
    score -= features["high_risk_count"] * 12
    score -= features["medium_risk_count"] * 5
    score -= features["additives_count"] * 4

    if features["sugar_present"]:
        score -= 8
    if features["oil_present"]:
        score -= 4
    if features["total_fat"] > 20:
        score -= 5
    if features["sodium"] > 500:
        score -= 5

    # rewards (stronger)
    score += features["protein_sources"] * 12
    score += features["spice_count"] * 5
    score += features["natural_ingredient_count"] * 3

    return max(0, min(score, 100))

# ---------- DATASET GENERATION ----------
def generate_dataset(samples=150):
    rows = []

    PROTEIN = ["groundnut", "peanuts", "besan"]
    SPICES = ["turmeric", "black pepper", "ginger", "cumin"]

    for _ in range(samples):
        ingredients = (
            random.sample(HIGH_RISK, random.randint(0, 1)) +
            random.sample(MEDIUM_RISK, random.randint(0, 2)) +
            random.sample(LOW_RISK, min(len(LOW_RISK), random.randint(1, 3)))+
            random.sample(PROTEIN, random.randint(0, 2)) +
            random.sample(SPICES, random.randint(0, 3))
        )

        nutrition = {
            "fat": random.randint(0, 25),
            "sodium": random.randint(10, 700),
            "protein": random.randint(0, 10)
        }

        features = extract_features(ingredients, nutrition)
        score = rule_based_score(features)
        features["health_score"] = score

        rows.append(features)

    return pd.DataFrame(rows)

# ---------- RUN ----------
if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("data/health_dataset.csv", index=False)

    print("✅ health_dataset.csv created successfully!")
    print(df.head())
