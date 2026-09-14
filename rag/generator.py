def extract_field(text, field_name):
    """
    Extract one field from the retrieved knowledge text.
    """

    # Example:
    # field_name = "Material"
    # We search for:
    # Material: Plastic/PET

    prefix = field_name + ":"

    for line in text.splitlines():

        if line.startswith(prefix):

            return line[len(prefix):].strip()

    return "Not specified in the knowledge base."


def generate_answer(query, retrieved_results):
    """
    Generate a grounded EcoSort response.

    The factual information comes directly
    from the retrieved knowledge base.
    """

    # Safety check
    if not retrieved_results:
        return (
            "Insufficient information is available in the "
            "EcoSort knowledge base.\n\n"
            "Please check your local official "
            "waste-management guidance."
        )

    # Use the best retrieved result
    knowledge = retrieved_results[0]

    # Get the complete knowledge text
    text = knowledge["text"]

    # Extract factual fields
    item = extract_field(text, "Item")
    category = extract_field(text, "Category")
    material = extract_field(text, "Material")
    disposal_action = extract_field(text, "Disposal Action")
    why = extract_field(text, "Why")

    sustainability_tip = extract_field(
        text,
        "Sustainability Tip"
    )

    special_handling = extract_field(
        text,
        "Special Handling"
    )

    confidence_note = extract_field(
        text,
        "Confidence Note"
    )

    # Create a simple grounded explanation
    explanation = (
        f"{disposal_action}. "
        f"This is recommended because {why.lower()}."
    )

    # Build the final answer using
    # the trusted knowledge-base fields.
    answer = f"""
Waste Category: {category}

Material: {material}

Recommended Action:
{disposal_action}

Why:
{why}

Sustainability Tip:
{sustainability_tip}

Special Handling:
{special_handling}

Confidence/Note:
{confidence_note}

AI Explanation:
{explanation}
"""

    return answer