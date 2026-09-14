from rag.retrieve import retrieve, is_relevant
from rag.generator import generate_answer


# The question we want to test
query = "How should I dispose of a plastic bottle?"


# Step 1: Retrieve relevant knowledge from FAISS
results = retrieve(query, top_k=3)

print("\n--- FULL BEST RESULT ---")
print(results[0])


print("\n--- RETRIEVED KNOWLEDGE ---")

for result in results:
    print(f"\nItem: {result['item']}")
    print(f"Category: {result['category']}")
    print(f"Similarity: {result['similarity_score']:.4f}")


# Step 2: Check whether the retrieved
# knowledge is actually relevant
if not is_relevant(query, results):

    print("\nInsufficient relevant knowledge.")
    print(
        "Please check your local official "
        "waste-management guidance."
    )

else:

    print("\nRelevant knowledge found.")

    # Step 3: Generate an answer using
    # the retrieved knowledge
    answer = generate_answer(
        query,
        results
    )

    print("\n--- ECO SORT AI ANSWER ---")
    print(answer)
