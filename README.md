# ♻️ EcoSort AI

### AI-Powered Waste Segregation & Sustainable Disposal Assistant

EcoSort AI is a **Retrieval-Augmented Generation (RAG) based waste-management assistant** that helps users identify how different types of waste should be segregated, handled, and disposed of responsibly.

The system uses a curated waste-management knowledge base, **Sentence Transformers**, **FAISS**, and **Streamlit** to provide grounded disposal recommendations.

> **Current implementation:** Local RAG using Sentence Transformers + FAISS with knowledge-based answer generation.
> **Future/optional integration:** IBM watsonx.ai and IBM Granite can be connected when access is available.

---

## 🌱 Problem Statement

Improper waste segregation and disposal can cause environmental pollution, health risks, and inefficient recycling.

People often do not know:

* Which category a waste item belongs to
* Whether it can be recycled
* Where it should be disposed of
* Whether special handling is required
* How disposal practices affect sustainability

EcoSort AI aims to provide a simple, accessible assistant for making better waste-management decisions.

---

## 🎯 Objectives

* Identify the category and material of waste.
* Recommend an appropriate disposal or recycling action.
* Explain why the recommendation is appropriate.
* Provide sustainability tips.
* Highlight special handling requirements.
* Use reliable and curated waste-management information.
* Avoid generating unsupported recommendations.
* Inform users when local waste-management rules may differ.

---

## ✨ Features

### 🔎 Waste Analysis

Users can enter natural-language questions such as:

```text
How should I dispose of a plastic bottle?
```

or:

```text
What should I do with an old mobile phone?
```

### ♻️ Waste Classification

The application provides information such as:

* Waste Category
* Material
* Recommended Action

### 💡 Explanation

EcoSort AI explains why the recommended disposal method is appropriate.

### 🌱 Sustainability Tips

Users receive simple suggestions for reducing waste and improving reuse or recycling.

### ⚠️ Special Handling

The system highlights important precautions for items such as:

* Batteries
* Electronic waste
* Broken glass
* Fluorescent bulbs
* Used cooking oil

### 📚 Source Information

Each recommendation is connected to the source used in the knowledge base.

### 🛡️ Responsible AI

If the system does not have enough reliable information about a query, it does not attempt to provide an unsupported recommendation.

---

# 🧠 How EcoSort AI Works

EcoSort AI uses a **Retrieval-Augmented Generation (RAG)** architecture.

```text
User Query
    ↓
Streamlit Interface
    ↓
Query Processing
    ↓
Sentence Transformer
(all-MiniLM-L6-v2)
    ↓
FAISS Similarity Search
    ↓
Curated Waste Knowledge Base
    ↓
Relevant Knowledge Retrieved
    ↓
Grounded Answer Generator
    ↓
Structured Recommendation
    ↓
Streamlit UI
```

The important idea is:

> Instead of relying only on a language model's memory, EcoSort AI first retrieves relevant information from its curated knowledge base and then generates a recommendation based on that information.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │        USER          │
                         │  Waste-related Query │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌────────────────────────────┐
                    │     STREAMLIT FRONTEND     │
                    │          app.py            │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │      RAG RETRIEVAL         │
                    │       rag/retrieve.py      │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │   SENTENCE TRANSFORMER     │
                    │   all-MiniLM-L6-v2         │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │       FAISS SEARCH         │
                    │   Similarity Retrieval     │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
              ┌─────────────────────────────────────────┐
              │        CURATED KNOWLEDGE BASE           │
              │ ecosort_knowledge_base_cleaned.csv      │
              └────────────────────┬────────────────────┘
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │   GROUNDED ANSWER         │
                    │   GENERATOR                │
                    │   rag/generator.py         │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │  STRUCTURED RECOMMENDATION │
                    │                            │
                    │ Category                   │
                    │ Material                   │
                    │ Recommended Action         │
                    │ Why                        │
                    │ Sustainability Tip        │
                    │ Special Handling           │
                    │ Confidence / Note          │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │      STREAMLIT UI          │
                    │   Final Recommendation     │
                    └────────────────────────────┘


     Supporting Components
     
     rag/ingest.py
          │
          ▼
     Embeddings → FAISS Index
          │
          ├── vectorstore/faiss.index
          └── vectorstore/metadata.json


     tests/test_all_items.py
          │
          ▼
     RAG Retrieval Evaluation
```

---

# 📂 Project Structure

```text
EcoSort-AI/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── test_rag.py
│
├── data/
│   ├── ecosort_knowledge_base.csv
│   └── ecosort_knowledge_base_cleaned.csv
│
├── rag/
│   ├── __init__.py
│   ├── ingest.py
│   ├── retrieve.py
│   └── generator.py
│
├── vectorstore/
│   ├── faiss.index
│   └── metadata.json
│
└── tests/
    ├── clean_knowledge_base.py
    ├── test_all_items.py
    └── test_retrieval.py
```

---

# 🔧 Technologies Used

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Core programming language      |
| Streamlit             | Web application interface      |
| Pandas                | Knowledge-base data processing |
| Sentence Transformers | Text embeddings                |
| all-MiniLM-L6-v2      | Embedding model                |
| FAISS                 | Vector similarity search       |
| python-dotenv         | Environment configuration      |
| CSV                   | Knowledge-base storage         |
| Git/GitHub            | Version control                |

### Future / Optional

| Technology     | Purpose                              |
| -------------- | ------------------------------------ |
| IBM watsonx.ai | Enterprise AI platform               |
| IBM Granite    | Generative AI model                  |
| LangChain      | Optional RAG/orchestration framework |

---

# 📚 Knowledge Base

The current knowledge base contains curated information about different waste items, including:

* Organic waste
* Paper
* Cardboard
* Plastic
* Glass
* Metal
* E-waste
* Batteries
* Fluorescent bulbs
* Used cooking oil
* Textiles
* Furniture
* Ceramic waste

Each knowledge-base record contains fields such as:

```text
item
aliases
category
material
disposal_action
why
sustainability_tip
special_handling
confidence_note
source
source_url
```

---

# 🔍 RAG Pipeline

## 1. Knowledge Ingestion

`rag/ingest.py` reads the curated CSV knowledge base.

The records are converted into searchable text documents.

---

## 2. Text Embedding

The Sentence Transformer model:

```text
all-MiniLM-L6-v2
```

converts text into numerical vectors.

The current embedding dimension is:

```text
384
```

---

## 3. FAISS Indexing

The generated vectors are stored in a FAISS index.

```text
vectorstore/faiss.index
```

Metadata is stored separately:

```text
vectorstore/metadata.json
```

---

## 4. Retrieval

When a user asks a question, EcoSort AI:

1. Checks for exact item/alias matches.
2. If no exact match is found, performs semantic similarity search.
3. Retrieves the most relevant knowledge records.
4. Checks whether the retrieved information is sufficiently relevant.

---

## 5. Grounded Answer Generation

The retrieved knowledge is converted into a structured recommendation containing:

```text
Waste Category
Material
Recommended Action
Why
Sustainability Tip
Special Handling
Confidence / Note
AI Explanation
```

This reduces the chance of unsupported recommendations.

---

# 🛡️ Responsible AI

EcoSort AI follows a simple responsible-AI approach.

### Grounded Responses

Recommendations are based on the curated knowledge base rather than unrestricted generation.

### Insufficient Information Handling

If a query is not sufficiently supported by the knowledge base, the system returns:

```text
Insufficient information
```

instead of presenting an unsupported disposal recommendation.

### Local Variation

Waste-management systems and recycling facilities can differ between locations.

Therefore, users are advised to verify local requirements.

### Hazardous Waste

For hazardous, unusual, or unsupported waste, users should consult appropriate local authorities or authorized waste-management services.

---

# 🧪 Testing

EcoSort AI includes a retrieval evaluation test:

```text
tests/test_all_items.py
```

The current curated evaluation contains:

```text
Total tests : 30
Passed      : 30
Failed      : 0
Accuracy    : 100.00%
```

### Important Note

The 100% figure represents **retrieval accuracy on the current curated 30-query evaluation set**.

It should not be interpreted as 100% accuracy for every possible real-world waste query.

---

# 💻 Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd EcoSort-AI
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Build the Vector Store

Run:

```bash
python rag/ingest.py
```

Expected output:

```text
Loaded 30 knowledge records.
Created 30 documents.
Embedding shape: (30, 384)
FAISS index contains 30 vectors.
EcoSort AI RAG ingestion complete!
```

---

# ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🧪 Example Queries

Try queries such as:

```text
How should I dispose of a plastic bottle?
```

```text
What should I do with an old mobile phone?
```

```text
How should I dispose of a lithium-ion battery?
```

```text
Can paper be recycled?
```

```text
What should I do with an old newspaper?
```

```text
Where can I recycle an old computer?
```

For unsupported queries such as:

```text
How should I dispose of an industrial chemical?
```

the system should avoid giving an unsupported recommendation and display an insufficient-information message.

---

# 📊 Example Output

### User Query

```text
How should I dispose of a plastic bottle?
```

### EcoSort AI

**Waste Category:**
Plastic Waste

**Material:**
Plastic/PET

**Recommended Action:**
Empty and segregate for the appropriate local plastic-waste or recycling channel.

**Why:**
Plastic packaging can be collected and channelized through waste-management systems.

**Sustainability Tip:**
Reuse suitable containers when appropriate and recycle when accepted.

**Special Handling:**
Do not burn plastic waste.

---

# 🌍 Sustainability Impact

EcoSort AI supports **UN Sustainable Development Goal 12 — Responsible Consumption and Production**.

It can also contribute to:

### SDG 11 — Sustainable Cities and Communities

Better waste segregation can support cleaner and more sustainable communities.

### SDG 13 — Climate Action

Improved reuse, recycling, and responsible disposal can help reduce the environmental impact associated with waste.

---

# 🚀 Future Scope

Future versions of EcoSort AI can include:

* 🤖 IBM Granite integration through IBM watsonx.ai
* 📸 Image-based waste classification
* 🗺️ Location-based recycling-center recommendations
* 🌐 Multilingual waste-management assistance
* 📱 Mobile application
* 📈 Waste-generation analytics
* 🏫 School and college waste-management dashboards
* 🏢 Organization-level waste tracking
* 🔄 Automatic knowledge-base updates
* 🧠 Improved hybrid retrieval
* 🗣️ Voice-based waste queries

---

# 🤖 IBM Granite Integration

The project architecture is designed so that IBM Granite can be integrated into the generation layer in the future.

Current:

```text
User Query
     ↓
FAISS Retrieval
     ↓
Retrieved Knowledge
     ↓
Grounded Local Generator
     ↓
Answer
```

Future:

```text
User Query
     ↓
FAISS Retrieval
     ↓
Retrieved Knowledge
     ↓
IBM Granite
     ↓
Grounded Answer
     ↓
Streamlit
```

IBM Granite should be described as a **future/optional integration** unless the project is actually connected to IBM watsonx.ai.

---

# 👩‍💻 Project Context

**Project:** EcoSort AI
**Program:** 1M1B AI for Sustainability Virtual Internship
**Technology Partner:** IBM SkillsBuild
**Focus:** Artificial Intelligence + Sustainability
**Primary SDG:** SDG 12 — Responsible Consumption and Production

---

# 📌 Limitations

EcoSort AI currently has some limitations:

* The knowledge base covers a limited number of waste categories and items.
* Local waste-management rules may differ.
* Recycling availability varies by location.
* The system should not be treated as a substitute for official hazardous-waste guidance.
* The current evaluation is based on a curated test set.
* Image-based waste recognition is not currently implemented.
* IBM Granite is not part of the current local implementation.

---

# 📜 Responsible Use

EcoSort AI is intended to provide educational and practical guidance for common waste-management situations.

For hazardous, unusual, medical, chemical, radioactive, or otherwise specialized waste, users should consult the relevant local authority or an authorized waste-management service.

---

# ⭐ Project Highlights

* Retrieval-Augmented Generation architecture
* Semantic search using Sentence Transformers
* FAISS vector database
* Curated waste-management knowledge base
* Source-grounded recommendations
* Unsupported-query protection
* Responsible AI messaging
* Streamlit-based interactive interface
* 30/30 curated retrieval tests passed

---

## ♻️ EcoSort AI

**Making better waste decisions, one item at a time.**
