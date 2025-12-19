def normalize_ingredients(ingredients):
    normalized = []

    for ing in ingredients:
        ing = ing.lower()

        # --- SUGARS ---
        if "sugar" in ing or "dextrose" in ing or "maltodextrin" in ing:
            normalized.append("sugar")

        # --- OILS ---
        elif "palm" in ing and "oil" in ing:
            normalized.append("palm oil")
        elif "vegetable oil" in ing:
            normalized.append("vegetable oil")

        # --- ADDITIVES ---
        elif "flavour" in ing:
            normalized.append("flavourings")
        elif "anticaking" in ing or "anti caking" in ing:
            normalized.append("anticaking agent")
        elif "colour" in ing or "color" in ing:
            normalized.append("colour")
        elif "acidity" in ing or "regulator" in ing or "ins" in ing:
            normalized.append("acidity regulator")

        # --- BASE INGREDIENTS ---
        elif "potato" in ing:
            normalized.append("potato")
        elif "groundnut" in ing or "peanut" in ing:
            normalized.append("groundnut")
        elif "besan" in ing or "bengal gram" in ing:
            normalized.append("besan")

        # --- SPICES ---
        elif "turmeric" in ing:
            normalized.append("turmeric")
        elif "pepper" in ing:
            normalized.append("black pepper")
        elif "ginger" in ing:
            normalized.append("ginger")
        elif "cumin" in ing:
            normalized.append("cumin")

    return list(set(normalized))
