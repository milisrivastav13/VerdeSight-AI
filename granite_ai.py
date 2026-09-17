from rag_engine import search_knowledge


# ============================================================
# GRANITE-READY RESPONSE ENGINE
# ============================================================

def generate_granite_response(
    question,
    context=""
):

    question = str(
        question
    ).strip()

    if not question:

        return (
            "Ask me about waste, recycling, "
            "composting, segregation, sustainability, "
            "circular economy or environmental impact."
        )

    # --------------------------------------------------------
    # Search knowledge independently
    # --------------------------------------------------------

    results = search_knowledge(
        question,
        top_k=3
    )

    response_parts = []

    for result in results:

        text = result.get(
            "response",
            ""
        ).strip()

        if text:

            response_parts.append(
                text
            )

    # --------------------------------------------------------
    # Use retrieved context
    # --------------------------------------------------------

    if context.strip():

        if not response_parts:

            response_parts.append(
                context.strip()
            )

    # --------------------------------------------------------
    # Return grounded answer
    # --------------------------------------------------------

    if response_parts:

        unique_parts = []

        for part in response_parts:

            if part not in unique_parts:

                unique_parts.append(
                    part
                )

        answer = (
            "\n\n".join(
                unique_parts
            )
        )

        return (
            "### ♻️ VerdeSight AI\n\n"
            f"{answer}\n\n"
            "---\n"
            "For actual disposal decisions, "
            "follow applicable local waste-management rules."
        )

    # --------------------------------------------------------
    # General fallback
    # --------------------------------------------------------

    return """
### ♻️ VerdeSight AI

I don't currently have enough verified knowledge
to answer that specific question.

I can help with:

• Organic waste
• Plastic waste
• Paper and cardboard
• Metal
• Glass
• E-waste
• Textile waste
• Waste segregation
• Composting
• Recycling
• Sustainability
• Circular economy
• SDG 12
"""