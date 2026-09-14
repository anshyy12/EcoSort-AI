import os
import json
import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Project paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "ecosort_knowledge_base_cleaned.csv"
)

VECTORSTORE_DIR = os.path.join(
    BASE_DIR,
    "vectorstore"
)

INDEX_PATH = os.path.join(
    VECTORSTORE_DIR,
    "faiss.index"
)

METADATA_PATH = os.path.join(
    VECTORSTORE_DIR,
    "metadata.json"
)


# -----------------------------
# 2. Embedding model
# -----------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded.")


# -----------------------------
# 3. Read knowledge base
# -----------------------------

print("Reading knowledge base...")

df = pd.read_csv(CSV_PATH)

print(f"Loaded {len(df)} knowledge records.")


# -----------------------------
# 4. Create readable documents
# -----------------------------

documents = []
metadata = []

for _, row in df.iterrows():

    document_text = f"""
Item: {row['item']}
Aliases: {row['aliases']}
Category: {row['category']}
Material: {row['material']}
Disposal Action: {row['disposal_action']}
Why: {row['why']}
Sustainability Tip: {row['sustainability_tip']}
Special Handling: {row['special_handling']}
Confidence Note: {row['confidence_note']}
Source: {row['source']}
Source URL: {row['source_url']}
""".strip()

    documents.append(document_text)

    metadata.append({
        "item": row["item"],
        "category": row["category"],
        "source": row["source"],
        "source_url": row["source_url"],
        "text": document_text
    })


print(f"Created {len(documents)} documents.")


# -----------------------------
# 5. Generate embeddings
# -----------------------------

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print(f"Embedding shape: {embeddings.shape}")


# -----------------------------
# 6. Create FAISS index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print(f"FAISS index contains {index.ntotal} vectors.")


# -----------------------------
# 7. Create vectorstore folder
# -----------------------------

os.makedirs(
    VECTORSTORE_DIR,
    exist_ok=True
)


# -----------------------------
# 8. Save FAISS index
# -----------------------------

faiss.write_index(
    index,
    INDEX_PATH
)


# -----------------------------
# 9. Save metadata
# -----------------------------

with open(
    METADATA_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )


# -----------------------------
# 10. Finished
# -----------------------------

print()
print("===================================")
print("EcoSort AI RAG ingestion complete!")
print("===================================")
print(f"FAISS index: {INDEX_PATH}")
print(f"Metadata:    {METADATA_PATH}")