import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

INDEX_PATH = VECTORSTORE_DIR / "faiss.index"
METADATA_PATH = VECTORSTORE_DIR / "metadata.json"


# --------------------------------------------------
# 2. Configuration
# --------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

DEFAULT_TOP_K = 3

DEFAULT_SIMILARITY_THRESHOLD = 0.30


# --------------------------------------------------
# 3. Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

print("Embedding model loaded.")


# --------------------------------------------------
# 4. Load FAISS index and metadata
# --------------------------------------------------

if not INDEX_PATH.exists():
    raise FileNotFoundError(
        f"FAISS index not found at: {INDEX_PATH}\n"
        "Please run: python rag/ingest.py"
    )

if not METADATA_PATH.exists():
    raise FileNotFoundError(
        f"Metadata file not found at: {METADATA_PATH}\n"
        "Please run: python rag/ingest.py"
    )


print("Loading FAISS index...")

index = faiss.read_index(str(INDEX_PATH))

print(
    f"FAISS index loaded with {index.ntotal} vectors."
)


print("Loading metadata...")

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:

    metadata = json.load(file)

print(
    f"Loaded {len(metadata)} metadata records."
)


# --------------------------------------------------
# 5. Retrieval function
# --------------------------------------------------

def retrieve(query, top_k=DEFAULT_TOP_K):
    """
    Retrieve the most relevant waste-management
    knowledge records.

    Exact item or alias matches are given priority.
    If multiple exact matches exist, the longest
    and most specific match is selected.

    If no exact match exists, FAISS semantic
    similarity search is used.
    """

    if not query or not query.strip():
        return []

    query_lower = query.lower().strip()

    # --------------------------------------------------
    # Step 1: Find exact item / alias matches
    # --------------------------------------------------

    exact_matches = []

    for record in metadata:

        item = record.get(
            "item",
            ""
        ).lower().strip()

        text = record.get(
            "text",
            ""
        ).lower()

        aliases = []

        # Extract aliases from stored knowledge text
        for line in text.splitlines():

            if line.startswith("aliases:"):

                alias_text = line.replace(
                    "aliases:",
                    "",
                    1
                ).strip()

                aliases = [
                    alias.strip().lower()
                    for alias in alias_text.split(";")
                ]

        # Check exact item match
        if item and item in query_lower:

            exact_matches.append(
                (len(item), record)
            )

        # Check exact alias matches
        for alias in aliases:

            if alias and alias in query_lower:

                exact_matches.append(
                    (len(alias), record)
                )

    # --------------------------------------------------
    # Step 2: Select most specific exact match
    # --------------------------------------------------

    if exact_matches:

        # Longer phrase = more specific match
        exact_matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        added_items = set()

        for _, record in exact_matches:

            item_name = record.get(
                "item",
                ""
            )

            # Avoid duplicate records
            if item_name in added_items:
                continue

            added_items.add(item_name)

            results.append({
                "text": record.get(
                    "text",
                    ""
                ),
                "item": item_name,
                "category": record.get(
                    "category",
                    ""
                ),
                "source": record.get(
                    "source",
                    ""
                ),
                "source_url": record.get(
                    "source_url",
                    ""
                ),
                "similarity_score": 1.0
            })

            if len(results) >= top_k:
                break

        return results

    # --------------------------------------------------
    # Step 3: Semantic FAISS search
    # --------------------------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx < 0 or idx >= len(metadata):
            continue

        record = metadata[idx]

        results.append({
            "text": record.get(
                "text",
                ""
            ),
            "item": record.get(
                "item",
                ""
            ),
            "category": record.get(
                "category",
                ""
            ),
            "source": record.get(
                "source",
                ""
            ),
            "source_url": record.get(
                "source_url",
                ""
            ),
            "similarity_score": float(score)
        })

    return results


# --------------------------------------------------
# 6. Check whether retrieval is reliable enough
# --------------------------------------------------

def is_relevant(
    query,
    results,
    threshold=DEFAULT_SIMILARITY_THRESHOLD
):
    """
    Check whether retrieved knowledge is reliable
    enough to answer the user's query.

    We use:
    1. similarity score
    2. keyword overlap
    """

    if not results:
        return False

    best_result = results[0]

    best_score = best_result[
        "similarity_score"
    ]

    # Check similarity threshold
    if best_score < threshold:
        return False

    item = best_result.get(
        "item",
        ""
    ).lower()

    aliases = best_result.get(
        "text",
        ""
    ).lower()

    query_words = set(
        word.lower().strip(".,?!")
        for word in query.split()
        if len(word) > 2
    )

    matched_words = [
        word
        for word in query_words
        if word in item or word in aliases
    ]

    return len(matched_words) > 0


# --------------------------------------------------
# 7. Command-line testing
# --------------------------------------------------

if __name__ == "__main__":

    print("\nEcoSort AI Retrieval Test")
    print("-------------------------")

    query = input(
        "\nEnter your waste-related question: "
    ).strip()

    results = retrieve(query)

    if not results:

        print(
            "\nNo relevant knowledge was retrieved."
        )

    else:

        print("\nRetrieved Knowledge:\n")

        for i, result in enumerate(
            results,
            start=1
        ):

            print(f"Result {i}")
            print("-" * 40)

            print(
                f"Item: {result['item']}"
            )

            print(
                f"Category: {result['category']}"
            )

            print(
                f"Similarity Score: "
                f"{result['similarity_score']:.4f}"
            )

            print(
                f"Source: {result['source']}"
            )

            print(
                f"Source URL: "
                f"{result['source_url']}"
            )

            print(
                f"Text: {result['text']}"
            )

            print()

        if is_relevant(query, results):

            print(
                "Sufficient relevant knowledge found."
            )

        else:

            print(
                "Insufficient information in the "
                "EcoSort knowledge base."
            )

            print(
                "Please check your local official "
                "waste-management guidance."
            )