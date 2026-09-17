# impact_engine.py


IMPACT_DATA = {

    "plastic": {
        "category": "Plastic",
        "impact_level": "Medium–High",
        "benefit": "Improved material recovery"
    },

    "organic": {
        "category": "Organic",
        "impact_level": "Medium",
        "benefit": "Supports organic-waste recovery"
    },

    "paper": {
        "category": "Paper",
        "impact_level": "Medium",
        "benefit": "Supports paper recovery"
    },

    "metal": {
        "category": "Metal",
        "impact_level": "Medium",
        "benefit": "Supports material recovery"
    },

    "e-waste": {
        "category": "E-Waste",
        "impact_level": "High",
        "benefit": "Supports safer electronic-waste handling"
    },

    "unknown": {
        "category": "Unknown",
        "impact_level": "Unknown",
        "benefit": "Manual verification recommended"
    }
}


def calculate_impact(label):

    text = str(label).lower()

    if (
        "e-waste" in text
        or "electronic" in text
    ):
        return IMPACT_DATA["e-waste"]

    if "plastic" in text:
        return IMPACT_DATA["plastic"]

    if "organic" in text:
        return IMPACT_DATA["organic"]

    if "paper" in text:
        return IMPACT_DATA["paper"]

    if "metal" in text:
        return IMPACT_DATA["metal"]

    return IMPACT_DATA["unknown"]