import re


# ============================================================
# KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = {

    "organic": {

        "keywords": [
            "organic",
            "biodegradable",
            "banana",
            "banana peel",
            "apple",
            "apple core",
            "orange peel",
            "vegetable",
            "vegetable waste",
            "food waste",
            "food scraps",
            "fruit",
            "fruit waste",
            "kitchen waste",
            "compost",
        ],

        "response": """
Organic or biodegradable waste includes food scraps,
fruit and vegetable peels, leaves and other materials
that can naturally decompose.

Examples:
• Banana peels
• Apple cores
• Vegetable scraps
• Food leftovers
• Leaves

Recommended approach:
1. Separate organic waste from dry waste.
2. Compost suitable organic material.
3. Keep plastic and other contaminants away from compost.
4. Follow local waste-management rules.

Banana peels are biodegradable organic waste and are
commonly suitable for composting.
""",
    },


    "plastic": {

        "keywords": [
            "plastic",
            "plastic waste",
            "bottle",
            "plastic bottle",
            "wrapper",
            "polybag",
            "polythene",
            "pet",
            "container",
        ],

        "response": """
Plastic waste should generally be separated from wet
organic waste.

Examples include:
• Plastic bottles
• Packaging
• Wrappers
• Containers
• Plastic bags

Where practical, empty and clean recyclable containers
before sending them through an appropriate recycling
collection system.
""",
    },


    "paper": {

        "keywords": [
            "paper",
            "paper waste",
            "cardboard",
            "newspaper",
            "book",
            "carton",
            "box",
        ],

        "response": """
Paper and cardboard are commonly recyclable when they
are clean and dry.

Recommended approach:
• Keep paper dry.
• Remove heavily contaminated material.
• Flatten cardboard.
• Separate paper from wet waste.
""",
    },


    "metal": {

        "keywords": [
            "metal",
            "metal waste",
            "aluminium",
            "aluminum",
            "steel",
            "tin",
            "can",
            "metal can",
        ],

        "response": """
Metal waste can often be recycled.

Examples include aluminium cans, steel containers
and other recyclable metal objects.

Keep metal separate from wet waste and use an
appropriate recycling channel.
""",
    },


    "glass": {

        "keywords": [
            "glass",
            "glass waste",
            "glass bottle",
            "jar",
            "glass jar",
        ],

        "response": """
Glass containers can generally be recycled through
appropriate collection systems.

Keep glass separate from other waste and handle broken
glass carefully.
""",
    },


    "ewaste": {

        "keywords": [
            "e-waste",
            "ewaste",
            "electronic waste",
            "electronics",
            "electronic",
            "phone",
            "mobile",
            "laptop",
            "computer",
            "charger",
            "battery",
        ],

        "response": """
Electronic waste includes discarded electronic devices,
components, chargers and batteries.

Do not put e-waste into ordinary household waste.

Use an appropriate authorised e-waste collection or
recycling channel.
""",
    },


    "textile": {

        "keywords": [
            "textile",
            "cloth",
            "clothes",
            "clothing",
            "fabric",
            "shirt",
            "jeans",
            "dress",
        ],

        "response": """
Textile waste includes unwanted clothes, fabrics and
other textile materials.

Usable clothing can be reused or donated. Damaged
textiles may be suitable for textile recycling depending
on available facilities.
""",
    },


    "segregation": {

        "keywords": [
            "segregation",
            "segregate",
            "separate",
            "separation",
            "wet waste",
            "dry waste",
            "bin",
            "waste management",
        ],

        "response": """
Waste segregation means separating waste according to
its material and disposal pathway.

A basic approach is:
• Wet / organic waste
• Dry recyclable waste
• E-waste and hazardous materials separately

Local municipal rules can differ.
""",
    },


    "composting": {

        "keywords": [
            "compost",
            "composting",
            "compostable",
            "kitchen compost",
            "food compost",
            "organic compost",
        ],

        "response": """
Composting converts suitable biodegradable materials
into an organic soil amendment.

Suitable inputs can include fruit and vegetable scraps,
leaves and other biodegradable material.

Avoid plastics, batteries, chemicals and other
unsuitable materials.
""",
    },


    "recycling": {

        "keywords": [
            "recycle",
            "recycling",
            "recyclable",
            "recycler",
            "recycled",
        ],

        "response": """
Recycling involves collecting, sorting and processing
materials so that useful material can re-enter production.

Whether a particular item is recyclable depends on its
material, condition and the facilities available locally.
""",
    },


    "sustainability": {

        "keywords": [
            "sustainability",
            "sustainable",
            "environment",
            "environmental",
            "eco",
            "green",
            "pollution",
            "carbon",
        ],

        "response": """
Sustainable waste management focuses on preventing waste,
reusing products, repairing items, recycling suitable
materials and responsibly disposing of unavoidable waste.

A useful hierarchy is:

Reduce → Reuse → Repair → Recycle → Dispose
""",
    },


    "circular_economy": {

        "keywords": [
            "circular economy",
            "circular",
            "reuse",
            "repair",
            "refurbish",
            "resource",
        ],

        "response": """
A circular economy aims to keep products and materials
in use for as long as possible.

It emphasizes:
• Reduce
• Reuse
• Repair
• Refurbish
• Recycle

The objective is to reduce resource extraction and waste.
""",
    },


    "sdg12": {

        "keywords": [
            "sdg 12",
            "sdg12",
            "responsible consumption",
            "responsible production",
        ],

        "response": """
SDG 12 focuses on responsible consumption and production.

Waste reduction, resource efficiency, sustainable
consumption and responsible management of materials
support this goal.
""",
    },
}


# ============================================================
# NORMALIZE
# ============================================================

def normalize(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s-]",
        " ",
        text
    )

    return text


# ============================================================
# SEARCH
# ============================================================

def search_knowledge(
    query,
    top_k=5
):

    query = normalize(
        query
    )

    query_words = set(
        query.split()
    )

    results = []

    for topic, data in (
        KNOWLEDGE_BASE.items()
    ):

        score = 0

        for keyword in (
            data["keywords"]
        ):

            keyword_normalized = (
                normalize(
                    keyword
                )
            )

            # Exact phrase
            if (
                keyword_normalized
                in query
            ):

                score += 5

            keyword_words = set(
                keyword_normalized.split()
            )

            overlap = (
                query_words
                .intersection(
                    keyword_words
                )
            )

            score += len(
                overlap
            )

        if score > 0:

            results.append({

                "topic":
                    topic,

                "score":
                    score,

                "response":
                    data["response"],
            })

    results.sort(
        key=lambda item:
        item["score"],
        reverse=True
    )

    return results[:top_k]