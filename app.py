import streamlit as st

from rag.retrieve import retrieve, is_relevant
from rag.generator import generate_answer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("♻️ EcoSort AI")

st.subheader(
    "AI-Powered Waste Segregation & Sustainable Disposal Assistant"
)

st.write(
    "Enter a waste item or ask a question to get a "
    "knowledge-based disposal recommendation."
)


# ============================================================
# USER INPUT
# ============================================================

st.header("🔎 Analyze Your Waste")

query = st.text_input(
    "What waste do you want to dispose of?",
    placeholder="Example: How should I dispose of a plastic bottle?"
)

st.caption(
    "Try: plastic bottle • old mobile phone • used battery"
)


# ============================================================
# FIELD EXTRACTION
# ============================================================

def extract_field(text, field_name):
    """
    Extract a field from the generated answer.

    It supports both:

    Field: value

    and:

    Field:
    value
    """

    lines = text.splitlines()

    prefix = field_name + ":"

    for i, line in enumerate(lines):

        line = line.strip()

        if line.startswith(prefix):

            # Check whether the value is
            # present on the same line.
            value = line[
                len(prefix):
            ].strip()

            if value:
                return value

            # Otherwise search for the
            # next non-empty line.
            for next_line in lines[i + 1:]:

                next_line = next_line.strip()

                if next_line:
                    return next_line

    return "Not specified."


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "♻️ Analyze Waste",
    use_container_width=True
):

    # --------------------------------------------------------
    # Empty input check
    # --------------------------------------------------------

    if not query.strip():

        st.warning(
            "Please enter a waste-related question."
        )


    else:

        # ----------------------------------------------------
        # RETRIEVAL
        # ----------------------------------------------------

        with st.spinner(
            "🔍 Searching EcoSort knowledge base..."
        ):

            results = retrieve(
                query,
                top_k=3
            )

            relevant = is_relevant(
                query,
                results
            )


        # ====================================================
        # UNKNOWN / UNSUPPORTED WASTE
        # ====================================================

        if not relevant:

            st.error(
                "⚠️ Insufficient information"
            )

            st.write(
                "EcoSort AI does not have enough reliable "
                "information about this waste item."
            )

            st.info(
                "Please check your local official "
                "waste-management guidance."
            )


        # ====================================================
        # SUPPORTED WASTE
        # ====================================================

        else:

            # ------------------------------------------------
            # Generate answer
            # ------------------------------------------------

            answer = generate_answer(
                query,
                results
            )


            # ------------------------------------------------
            # Extract fields
            # ------------------------------------------------

            category = extract_field(
                answer,
                "Waste Category"
            )

            material = extract_field(
                answer,
                "Material"
            )

            action = extract_field(
                answer,
                "Recommended Action"
            )

            why = extract_field(
                answer,
                "Why"
            )

            tip = extract_field(
                answer,
                "Sustainability Tip"
            )

            handling = extract_field(
                answer,
                "Special Handling"
            )

            confidence = extract_field(
                answer,
                "Confidence/Note"
            )

            explanation = extract_field(
                answer,
                "AI Explanation"
            )


            # =================================================
            # RECOMMENDATION
            # =================================================

            st.header("🌱 EcoSort AI Recommendation")


            # -------------------------------------------------
            # Category
            # -------------------------------------------------

            st.subheader("🗑️ Waste Category")

            st.info(category)


            # -------------------------------------------------
            # Material
            # -------------------------------------------------

            st.subheader("🧱 Material")

            st.info(material)


            # -------------------------------------------------
            # Recommended Action
            # -------------------------------------------------

            st.subheader("♻️ Recommended Action")

            st.success(action)


            # -------------------------------------------------
            # Why
            # -------------------------------------------------

            st.subheader("💡 Why?")

            st.write(why)


            # -------------------------------------------------
            # Sustainability Tip
            # -------------------------------------------------

            st.subheader("🌱 Sustainability Tip")

            st.write(tip)


            # -------------------------------------------------
            # Special Handling
            # -------------------------------------------------

            st.subheader("⚠️ Special Handling")

            st.warning(handling)


            # -------------------------------------------------
            # Confidence / Note
            # -------------------------------------------------

            st.subheader("📌 Confidence / Note")

            st.write(confidence)


            # -------------------------------------------------
            # AI Explanation
            # -------------------------------------------------

            st.subheader("🤖 AI Explanation")

            st.write(explanation)


            # =================================================
            # RETRIEVED KNOWLEDGE
            # =================================================

            with st.expander(
                "📚 View Retrieved Knowledge"
            ):

                for result in results:

                    st.write(
                        f"**Item:** {result['item']}"
                    )

                    st.write(
                        f"**Category:** {result['category']}"
                    )

                    st.write(
                        f"**Similarity Score:** "
                        f"{result['similarity_score']:.4f}"
                    )

                    st.divider()


            # =================================================
            # SOURCE
            # =================================================

            st.header("📖 Source")

            st.write(
                results[0]["source"]
            )

            st.link_button(
                "View Official Source",
                results[0]["source_url"]
            )


# ============================================================
# RESPONSIBLE AI NOTICE
# ============================================================

st.divider()

st.subheader("🤖 Responsible AI Notice")

st.write(
    "EcoSort AI provides waste-management recommendations "
    "based on its curated knowledge base. Recommendations "
    "may vary depending on local collection systems, "
    "recycling facilities, and applicable regulations."
)

st.write(
    "For hazardous, unusual, or unsupported waste, "
    "always consult appropriate local authorities or "
    "authorized waste-management services."
)
