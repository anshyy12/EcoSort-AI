import sys
import os

# Add the project root folder to Python's import path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from rag.retrieve import retrieve, is_relevant


# ============================================================
# REAL-WORLD USER QUERIES
# ============================================================

test_queries = [
    "Where can I dispose of my empty water bottle?",
    "I have an old smartphone. What should I do with it?",
    "What should I do with a dead battery?",
    "Can cardboard boxes be recycled?",
    "Where should I take my broken glass?",
    "What can I do with old clothes?",
    "How should I dispose of cooking oil?",
    "Where can I recycle an old computer?",
    "What should I do with an old keyboard?",
    "How should I dispose of a newspaper?",
    "What should I do with an aluminum drink can?",
    "Where can I dispose of a broken ceramic plate?",
    "What should I do with wooden furniture?",
    "How should I dispose of an industrial chemical?",
]


# ============================================================
# TESTING
# ============================================================

print("=" * 70)
print("EcoSort AI - Natural Language RAG Testing")
print("=" * 70)


for query in test_queries:

    print("\nQuery:", query)

    results = retrieve(
        query,
        top_k=3
    )

    if not results:

        print("No results found.")
        continue


    # --------------------------------------------------------
    # Best retrieved result
    # --------------------------------------------------------

    best = results[0]

    print(
        "Best Match:",
        best["item"]
    )

    print(
        "Category:",
        best["category"]
    )

    print(
        "Similarity:",
        round(
            best["similarity_score"],
            4
        )
    )


    # --------------------------------------------------------
    # Relevance check
    # --------------------------------------------------------

    relevant = is_relevant(
        query,
        results
    )

    print(
        "Relevant:",
        relevant
    )


    # --------------------------------------------------------
    # Show top 3 results
    # --------------------------------------------------------

    print("\nTop 3 Results:")

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"{i}. "
            f"{result['item']} "
            f"({result['similarity_score']:.4f})"
        )


    print("-" * 70)