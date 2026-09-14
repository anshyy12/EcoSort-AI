import pandas as pd
import re

input_file = "data/ecosort_knowledge_base.csv"
output_file = "data/ecosort_knowledge_base_cleaned.csv"

df = pd.read_csv(input_file)

print("Original records:", len(df))

text_columns = [
    "item",
    "aliases",
    "category",
    "material",
    "disposal_action",
    "why",
    "sustainability_tip",
    "special_handling",
    "confidence_note",
    "source",
    "source_url"
]


def clean_text(text):
    """Clean unwanted and missing spaces."""

    if pd.isna(text):
        return ""

    text = str(text).strip()

    # Convert multiple spaces into one
    text = re.sub(r"\s+", " ", text)

    # Add missing spaces between common words
    patterns = {
        r"fromdry": "from dry",
        r"Emptyand": "Empty and",
        r"emptyand": "empty and",
        r"andsegregate": "and segregate",
        r"recyclingavailability": "recycling availability",
        r"channelizedthrough": "channelized through",
        r"separatefrom": "separate from",
        r"Keepseparate": "Keep separate",
        r"foodwaste": "food waste",
        r"suitablefood": "suitable food",
        r"localcollection": "local collection",
        r"currentlocal": "current local",
        r"Followcurrent": "Follow current",
        r"authorizedwaste": "authorized waste",
        r"wastemanagement": "waste management",
        r"recyclingfacilities": "recycling facilities",
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text)

    return text


# Clean every text column
for column in text_columns:
    if column in df.columns:
        df[column] = df[column].apply(clean_text)


df.to_csv(output_file, index=False)

print("Cleaned records:", len(df))
print("Saved cleaned knowledge base to:", output_file)