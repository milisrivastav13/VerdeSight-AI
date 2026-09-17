# sustainability.py


def get_sustainability_score(actions_completed):
    """Calculate GreenScore."""

    return int(actions_completed) * 10


def get_sdg_mapping(label):

    text = str(label).lower()

    sdgs = [
        "SDG 12 — Responsible Consumption and Production"
    ]

    if (
        "plastic" in text
        or "organic" in text
        or "paper" in text
        or "metal" in text
    ):

        sdgs.append(
            "SDG 11 — Sustainable Cities and Communities"
        )

    if (
        "plastic" in text
        or "organic" in text
    ):

        sdgs.append(
            "SDG 13 — Climate Action"
        )

    return sdgs


def get_green_challenges():

    return [

        {
            "title": "Waste Sorting",
            "description": (
                "Identify and correctly separate five waste items."
            ),
            "points": 20
        },

        {
            "title": "Reduce Single-Use Plastic",
            "description": (
                "Avoid one unnecessary single-use plastic item today."
            ),
            "points": 15
        },

        {
            "title": "Organic Waste",
            "description": (
                "Separate organic waste from dry recyclable waste."
            ),
            "points": 15
        },

        {
            "title": "Recycle Paper",
            "description": (
                "Collect clean and dry recyclable paper separately."
            ),
            "points": 10
        },

        {
            "title": "E-Waste Awareness",
            "description": (
                "Learn the appropriate disposal route for "
                "one electronic item."
            ),
            "points": 20
        }
    ]