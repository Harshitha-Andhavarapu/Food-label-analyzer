def rule_based_score(features):
    score = 70  # better neutral baseline

    # penalties (reduced)
    score -= features["high_risk_count"] * 12
    score -= features["medium_risk_count"] * 5
    score -= features["additives_count"] * 4

    if features["sugar_present"]:
        score -= 8
    if features["oil_present"]:
        score -= 4
    if features["total_fat"] > 15:
        score -= 8
    if features["sodium"] > 400:
        score -= 8

    # rewards (stronger & meaningful)
    score += features["protein_sources"] * 10
    score += features["spice_count"] * 4
    score += features["natural_ingredient_count"] * 3

    return max(0, min(score, 100))
