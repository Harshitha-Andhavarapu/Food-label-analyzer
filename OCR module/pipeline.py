import pickle
import pandas as pd

from ocr_engine import run_ocr
from nlp.ingredient_nlp import clean_ingredients
from ml.ingredient_normalizer import normalize_ingredients
from ml.dataset_generator import extract_features, rule_based_score

# --------------------------------------------------
# 1️⃣ OCR (CHANGE IMAGE HERE)
# --------------------------------------------------
image_path = "images/lays.jpeg"   # change to nuts.png when needed
ocr_text = run_ocr(image_path)

# --------------------------------------------------
# 2️⃣ NLP CLEANING
# --------------------------------------------------
nlp_ingredients = clean_ingredients([ocr_text])

# --------------------------------------------------
# 3️⃣ NORMALIZATION
# --------------------------------------------------
ingredients = normalize_ingredients(nlp_ingredients)

# --------------------------------------------------
# 4️⃣ NUTRITION VALUES (TEMP)
# --------------------------------------------------
nutrition = {
    "fat": 18,
    "sodium": 520,
    "protein": 1
}

# --------------------------------------------------
# 5️⃣ FEATURE EXTRACTION
# --------------------------------------------------
features = extract_features(ingredients, nutrition)

# --------------------------------------------------
# 6️⃣ RULE SCORE
# --------------------------------------------------
rule_score = rule_based_score(features)

# --------------------------------------------------
# 7️⃣ LOAD MODEL
# --------------------------------------------------
with open("ml/model.pkl", "rb") as f:
    model = pickle.load(f)

X = pd.DataFrame([features])
ml_score = model.predict(X)[0]

# --------------------------------------------------
# 8️⃣ LABEL
# --------------------------------------------------
def label(score):
    if score >= 80:
        return "Healthy"
    elif score >= 50:
        return "Moderately Healthy"
    else:
        return "Unhealthy"

# --------------------------------------------------
# 9️⃣ OUTPUT
# --------------------------------------------------
print("\n--- PIPELINE OUTPUT ---")
print("IMAGE:", image_path)
print("\nRAW OCR TEXT:\n", ocr_text)
print("\nNLP INGREDIENTS:", nlp_ingredients)
print("\nNORMALIZED INGREDIENTS:", ingredients)
print("\nFEATURES:", features)
print("\nRule-based score:", rule_score)
print("ML predicted score:", round(ml_score, 2))
print("Final label:", label(ml_score))
