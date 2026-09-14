import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from rag.retrieve import retrieve, is_relevant


test_cases = [
    ("Where should I dispose of a banana peel?", "Banana peel"),
    ("What should I do with vegetable peels?", "Vegetable peels"),
    ("How should I dispose of leftover food?", "Food leftovers"),
    ("Can paper be recycled?", "Paper"),
    ("What should I do with an old newspaper?", "Newspaper"),
    ("Where can I recycle cardboard boxes?", "Cardboard"),
    ("How should I dispose of an empty water bottle?", "Plastic bottle"),
    ("What should I do with a plastic container?", "Plastic container"),
    ("How should I dispose of a plastic bag?", "Plastic bag"),
    ("Where should I dispose of a plastic wrapper?", "Plastic wrapper"),
    ("What should I do with a glass bottle?", "Glass bottle"),
    ("How should I dispose of broken glass?", "Broken glass"),
    ("Can I recycle an aluminum can?", "Aluminum can"),
    ("What should I do with a steel can?", "Steel can"),
    ("Where should I take my old mobile phone?", "Old mobile phone"),
    ("How should I dispose of an old phone charger?", "Phone charger"),
    ("Where can I recycle an old computer?", "Computer"),
    ("What should I do with an old keyboard?", "Keyboard"),
    ("How should I dispose of an old mouse?", "Mouse"),
    ("What should I do with old earphones?", "Earphones"),
    ("Where should I dispose of a used battery?", "Battery"),
    ("How should I dispose of a lithium-ion battery?", "Lithium-ion battery"),
    ("What should I do with a fluorescent bulb?", "Fluorescent bulb"),
    ("How should I dispose of used cooking oil?", "Used cooking oil"),
    ("What can I do with old clothes?", "Old clothes"),
    ("How should I dispose of old shoes?", "Shoes"),
    ("What should I do with old wooden furniture?", "Wooden furniture"),
    ("Where should I dispose of metal utensils?", "Metal utensils"),
    ("How should I dispose of a broken ceramic plate?", "Ceramic plate"),
    ("What should I do with old electronic accessories?", "Electronic accessories"),
]


passed = 0
failed = 0


print("\n===================================")
print("EcoSort AI - Full RAG Evaluation")
print("===================================\n")


for query, expected_item in test_cases:

    results = retrieve(query, top_k=3)

    relevant = is_relevant(query, results)

    if results:
        top_item = results[0]["item"]
        score = results[0]["similarity_score"]
    else:
        top_item = "No result"
        score = 0

    if top_item == expected_item and relevant:
        print(f"PASS | {expected_item}")
        print(f"     Query: {query}")
        print(f"     Score: {score:.4f}\n")
        passed += 1

    else:
        print(f"FAIL | Expected: {expected_item}")
        print(f"     Query: {query}")
        print(f"     Got: {top_item}")
        print(f"     Score: {score:.4f}")
        print(f"     Relevant: {relevant}\n")
        failed += 1


print("===================================")
print("Evaluation Complete")
print("===================================")

print(f"Total tests : {len(test_cases)}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")

accuracy = (passed / len(test_cases)) * 100

print(f"Accuracy    : {accuracy:.2f}%")