from rag_engine import search_knowledge


# ============================================================
# AGENT 1 — WASTE ANALYSIS
# ============================================================

def waste_analysis_agent(prediction):

    category = prediction.get(
        "category",
        "Unknown"
    )

    confidence = float(
        prediction.get(
            "confidence",
            0
        )
    )

    if confidence >= 80:

        status = (
            "High-confidence prediction"
        )

    elif confidence >= 60:

        status = (
            "Moderate-confidence prediction"
        )

    elif confidence >= 45:

        status = (
            "Low-confidence prediction"
        )

    else:

        status = (
            "Uncertain prediction"
        )

    return {

        "agent":
            "Waste Analysis Agent",

        "category":
            category,

        "confidence":
            confidence,

        "status":
            status,
    }


# ============================================================
# AGENT 2 — VERIFICATION
# ============================================================

def verification_agent(prediction):

    top_predictions = prediction.get(
        "top_predictions",
        []
    )

    if not top_predictions:

        return {

            "agent":
                "Verification Agent",

            "decision":
                "REVIEW",

            "reason":
                "No prediction results were returned.",

            "prediction_gap":
                0,
        }

    best = top_predictions[0]

    best_confidence = float(
        best.get(
            "confidence",
            0
        )
    )

    if len(top_predictions) > 1:

        second_confidence = float(
            top_predictions[1].get(
                "confidence",
                0
            )
        )

        gap = (
            best_confidence
            - second_confidence
        )

    else:

        gap = 100

    # --------------------------------------------------------
    # Decision logic
    # --------------------------------------------------------

    if best_confidence < 45:

        decision = "REVIEW"

        reason = (
            "The model confidence is below "
            "the acceptance threshold."
        )

    elif gap < 10:

        decision = "REVIEW"

        reason = (
            "The top predictions are too close "
            "to each other, indicating ambiguity."
        )

    else:

        decision = "ACCEPT"

        reason = (
            "The leading prediction has sufficient "
            "confidence and separation."
        )

    return {

        "agent":
            "Verification Agent",

        "decision":
            decision,

        "reason":
            reason,

        "prediction_gap":
            round(
                gap,
                2
            ),
    }


# ============================================================
# AGENT 3 — RECYCLING
# ============================================================

def recycling_agent(category):

    results = search_knowledge(
        category,
        top_k=2
    )

    if results:

        guidance_parts = []

        for result in results:

            guidance_parts.append(
                result.get(
                    "response",
                    ""
                ).strip()
            )

        guidance = "\n\n".join(
            part
            for part in guidance_parts
            if part
        )

    else:

        guidance = (
            "Separate the material from mixed waste "
            "and follow local waste-management rules."
        )

    return {

        "agent":
            "Recycling Agent",

        "guidance":
            guidance,
    }


# ============================================================
# AGENT 4 — ACTION PLANNING
# ============================================================

def generate_action_plan(category):

    plans = {

        "Organic / Biodegradable": [

            "Separate organic waste from dry waste.",

            "Use composting where appropriate.",

            "Keep plastic and other non-biodegradable "
            "materials out of organic waste.",

            "Use the resulting compost as a soil amendment."
        ],

        "Plastic": [

            "Separate plastic from wet waste.",

            "Empty and clean recyclable containers "
            "where practical.",

            "Identify the appropriate plastic recycling "
            "stream.",

            "Send recyclable material to a suitable "
            "collection or recycling facility."
        ],

        "Paper / Cardboard": [

            "Keep paper and cardboard dry.",

            "Remove heavily contaminated material.",

            "Flatten cardboard boxes.",

            "Place recyclable paper in the appropriate "
            "collection stream."
        ],

        "Metal": [

            "Separate metal from mixed waste.",

            "Remove contents when safe to do so.",

            "Reuse containers where practical.",

            "Send recyclable metal to an appropriate "
            "recycling channel."
        ],

        "Glass": [

            "Keep glass separate from other materials.",

            "Handle broken glass carefully.",

            "Reuse suitable glass containers.",

            "Use an appropriate glass collection system."
        ],

        "E-Waste": [

            "Do not place electronic waste in normal "
            "household waste.",

            "Keep batteries and electronics separated.",

            "Protect devices from damage during storage.",

            "Use an authorised e-waste collection or "
            "recycling channel."
        ],

        "Textile": [

            "Reuse clothing whenever possible.",

            "Donate usable clothes.",

            "Repair damaged clothing when practical.",

            "Use textile recycling where available."
        ],

        "General Waste": [

            "Check whether the item can be reused.",

            "Separate recyclable components.",

            "Keep wet and dry waste separated.",

            "Follow local disposal requirements."
        ],
    }

    actions = plans.get(
        category,
        plans["General Waste"]
    )

    return {

        "agent":
            "Action Planning Agent",

        "actions":
            actions,
    }


# ============================================================
# MASTER AGENTIC PIPELINE
# ============================================================

def run_agentic_pipeline(prediction):

    analysis = (
        waste_analysis_agent(
            prediction
        )
    )

    verification = (
        verification_agent(
            prediction
        )
    )

    # --------------------------------------------------------
    # If uncertain → manual review
    # --------------------------------------------------------

    if (
        verification["decision"]
        == "REVIEW"
    ):

        recycling = {

            "agent":
                "Recycling Agent",

            "guidance":
                (
                    "The classification is uncertain. "
                    "Verify the material before choosing "
                    "a disposal or recycling route."
                ),
        }

        action_plan = {

            "agent":
                "Action Planning Agent",

            "actions": [

                "Review the uploaded image.",

                "Compare the top model predictions.",

                "Verify the actual material.",

                "Then follow the correct disposal route."
            ],
        }

    else:

        category = prediction.get(
            "category",
            "General Waste"
        )

        recycling = (
            recycling_agent(
                category
            )
        )

        action_plan = (
            generate_action_plan(
                category
            )
        )

    return {

        "analysis":
            analysis,

        "verification":
            verification,

        "recycling":
            recycling,

        "action_plan":
            action_plan,
    }