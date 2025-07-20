# Fashion Recommendation Website 👗

🎬 Demo Video:  
[![Watch the demo](https://img.youtube.com/vi/AkL_Kw3-PtA/hqdefault.jpg)](https://youtu.be/AkL_Kw3-PtA?si=uUlF4NGBy1SsVJFg)

## 📚 Overview

Fashion Recommendation Website is a modern web application for fashion discovery. Users can upload a clothing image or enter a product description, and the system will recommend visually and semantically similar products using deep learning, multilingual embeddings, and GPT-4o smart descriptions.

---

## ✨ Features

- 🖼️ **Image-based Search:** Upload a photo to find visually similar fashion products.
- 📝 **Text-based Search:** Enter a product description to get recommended items.
- 🔍 **Top-4 Recommendations:** Always shows the top 4 most relevant results.
- 🌐 **Multilingual Embedding:** Supports many languages (intfloat/multilingual-e5-base).
- 🤖 **Smart Descriptions:** Detailed explanations via GPT-4o.

---

## 🛠️ Tech Stack

- **Frontend:** Next.js, Tailwind CSS
- **Backend:** FastAPI (Python) , Langchain (Python)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/)
- **Database:** SQLite
- **Embedding Model:** [intfloat/multilingual-e5-base](https://huggingface.co/intfloat/multilingual-e5-base)
- **LLM:** GPT-4o (Azure OpenAI API)

---

## 🧩 Project Structure

```bash
RECOMENTATION_SYSTEM/
├── backend/
│   ├── .venv/
│   ├── app/
│   │   ├── api.py
│   │   ├── classify_fashion_search.py
│   │   ├── database_query.py
│   │   ├── generate_description.py
│   │   └── retriver.py
│   ├── data/
│   ├── database/
│   ├── datalake/
│   ├── prepare/
│   ├── vector_db/
│   ├── .env
│   ├── .python-version
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── uv.lock
├── frontend/
│   ├── .next/
│   ├── app/
│   ├── node_modules/
│   ├── public/
│   ├── Dockerfile
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── tsconfig.json
├── .dockerignore
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## 🚦 Getting Started

### 0. Prepare .env files

```bash
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_API_VERSION=2024-XX-XX           # Example: 2024-03-01-preview
AZURE_DEPLOYMENT_NAME=your_deployment_name
```

### 1. Clone the repo

```bash
git clone https://github.com/Pd011161/Fashion-Recommendation-Website.git
cd Fashion-Recommendation-Website
```

### 2. Run the Backend (Requires Python 3.8+)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Vector store is handled by ChromaDB (with SQLite backend).


### 3. Run the Frontend (Requires Node.js (v18+))

```bash
cd ../frontend
npm install
npm run dev
```

- Web app: http://localhost:3000

---

## 🧑‍💻 Example Usage

1. Image Search:

- Go to the main page.
- Upload a clothing photo.
- Instantly see the top 4 visually similar fashion products with descriptions.

2. Text Search:

- Enter a description (e.g., "white linen pants, wide leg, minimal style").
- View the best-matched items, even with non-English queries.

3. Product Details:

- Click on any recommended item to see more details, smart descriptions, and possibly purchase info.

---

##  📝 Notes

- The embedding model supports multiple languages (Thai, English, etc).
- GPT-4o is used for generating smart, detailed product descriptions.
- For best results, prepare your own product image/metadata collection and pre-compute embeddings with the provided scripts.
- You can deploy the backend and frontend separately (Docker, cloud, etc).
- If using a public-facing URL, ensure your .env and API URLs are set correctly.

---

## ⚡ Quick Summary
Fashion Recommendation Website is a full-stack AI-driven solution for smart fashion discovery, supporting both image and text search, multilingual queries, and beautiful recommendations.

---

## 🔗 Recommended Integration
For even more accurate and versatile fashion recommendations, we suggest integrating the logic from the [Demo_fashion_recommend_find-and-match_logic repository](https://github.com/Pd011161/Demo_fashion_recommend_find-and-match_logic) 
This enables the system to:
- Find items that stylistically match each other (e.g., find pants that go well with a specific shirt, or vice versa)
- Enhance search precision using advanced matching logic and pairing rules
- Support style-based set recommendations (shirt + pants, full look, etc.)
