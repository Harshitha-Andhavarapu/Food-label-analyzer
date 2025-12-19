import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

STOP_WORDS = [
    "nutrition", "nutritional", "allergy", "contains",
    "storage", "manufactured", "best before"
]

def extract_ingredients(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Resize (VERY IMPORTANT for small text)
    # Resize aggressively
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

# Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Strong denoising
    gray = cv2.fastNlMeansDenoising(gray, h=30)

# Adaptive threshold
    thresh = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    15, 3
    )

    # OCR config for dense text
    config = "--oem 3 --psm 6"

    text = pytesseract.image_to_string(thresh, config=config)
    text = text.lower()

    # DEBUG (DO NOT REMOVE)
    print("\n----- OCR TEXT -----\n")
    print(text)

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    ingredients_lines = []
    collecting = False

    for line in lines:
        if "ingredient" in line:
            collecting = True
            line = re.sub(r"ingredients?\s*[:\-]?", "", line)
            if line:
                ingredients_lines.append(line)
            continue

        if collecting and any(word in line for word in STOP_WORDS):
            break

        if collecting:
            ingredients_lines.append(line)

    if not ingredients_lines:
        return []

    ingredients_text = " ".join(ingredients_lines)

    # Remove brackets like (E621)
    ingredients_text = re.sub(r"\([^)]*\)", "", ingredients_text)

    ingredients = ingredients_text.split(",")

    ingredients = [
        re.sub(r"[^a-z\s]", "", ing).strip()
        for ing in ingredients
        if len(ing.strip()) > 2
    ]

    return ingredients


if __name__ == "__main__":
    result = extract_ingredients("images/nuts.png")
    print("\nExtracted Ingredients:")
    for ing in result:
        print("-", ing)

def run_ocr(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found or invalid path")

    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, h=30)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        15, 3
    )

    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(thresh, config=config)

    return text
