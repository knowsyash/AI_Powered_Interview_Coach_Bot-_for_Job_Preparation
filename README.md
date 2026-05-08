# 🎯 VS Interviewer — AI-Powered Mock Interview Platform

> Practice technical and behavioral interviews with real-time AI feedback, built inside a VS Code-inspired interface.

**Live Demo →** [your-vercel-url.vercel.app](https://your-vercel-url.vercel.app)

---

## What is this?

VS Interviewer is a mock interview tool that feels like your actual coding environment. You pick a technology, answer questions in a VS Code-style editor, and get instant AI-powered feedback with a score out of 10.

The AI doesn't just count keywords — it uses a **semantic embedding model** (the same family of models used by Google and Meta for understanding meaning) to evaluate how well your answer actually addresses the question.

---

## What can you practice?

| Category | Topics Covered |
|---|---|
| 🌐 **Web Dev** | HTML, CSS, React, Next.js |
| 🐍 **Python** | Django, Flask, Data Science |
| ☕ **Java** | Core Java, OOP, Spring |
| ⚡ **Node.js** | React, Angular, Node, Express |
| 🗄️ **Database** | MySQL, PostgreSQL, MongoDB |
| 👥 **Behavioral** | STAR format, Leadership, Teamwork |

---

## How it works

1. **Pick a category** from the sidebar
2. **Read the question** — a timer starts automatically
3. **Type your answer** in plain text or switch to **Code Editor mode** (Monaco — same as VS Code)
4. **Submit** — the AI evaluates your answer in seconds
5. **Review feedback** — see your score, what you got right, what to improve, and a reference answer
6. **Keep going** or switch to **Session Mode** for a 5-question mock interview with a final report card

---

## Features

**Interview Experience**
- ⏱️ Per-question timer to simulate real interview pressure
- 💡 Hint system — request a hint for a −10% score penalty
- ⏭️ Skip questions you want to revisit
- 🛡️ Anti-cheat: copying the hint directly gives 0 marks
- 📝 Tab-switch detection logged in the terminal panel

**Answer Input**
- Plain text mode for explanations
- Monaco Editor for code answers (VS Code-grade, with syntax highlighting)
- Syntax validation for JavaScript answers

**Scoring & Feedback**
- AI score out of 10 based on semantic meaning, not just keywords
- Reference answer shown after evaluation
- Adjustable experience level: Junior / Mid / Senior
- Adjustable strictness: Lenient / Normal / Strict

**Analytics & Reports**
- Score history chart (persisted in your browser)
- 5-question session report with average, highest, lowest score, and a Pass/Needs Review verdict
- PDF export of your session report

**VS Code Aesthetic**
- Explorer sidebar, tabbed editor, status bar, and output terminal — all styled like VS Code dark theme
- Smooth transitions and animations throughout

---

## The AI Behind It

The scoring system uses three ML models trained on real human-scored interview data:

**1. Semantic Embedding Model** *(active in production)*
Uses `all-MiniLM-L6-v2` — a lightweight BERT-based transformer (22M parameters) that converts your answer into a mathematical representation of its meaning. A Random Forest Regressor trained on 4,000 real StackOverflow and behavioral answers then predicts a score from this representation.

**2. Random Forest Classifier** *(trained and benchmarked)*
Extracts 23 hand-engineered features from your answer — STAR format components, competency indicators, vocabulary diversity, use of numbers, action verbs, and more. Trained on 1,514 Q&A pairs.

**3. Custom TF-IDF Engine** *(trained and benchmarked)*
A from-scratch TF-IDF + cosine similarity implementation (no sklearn) that compares your answer against a reference using term frequency weighting, Jaccard keyword overlap, and length ratio scoring.

All three were benchmarked head-to-head. The semantic model won on RMSE, MAE, and within-±1.5 accuracy across the test set.

---

## Settings

| Setting | Options | What it does |
|---|---|---|
| Experience Level | Junior / Mid / Senior | Adjusts score expectations (Senior = harder grading) |
| Strictness | Lenient / Normal / Strict | Scales the raw score up or down |
| Session Mode | On / Off | Groups 5 questions into a timed mock session |

---

## Running Locally

**Backend (Python / Flask)**
```bash
cd AI_Interview_Bot
pip install -r requirements.txt
python app.py
# Runs on http://localhost:7860
```

**Frontend (Next.js)**
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

Create a `.env.local` in `/frontend`:
```
BACKEND_URL=http://localhost:7860
```

---

## Deployment

| Layer | Platform | Details |
|---|---|---|
| Frontend | **Vercel** | Next.js App Router, serverless functions as proxy |
| Backend | **Hugging Face Spaces** | Docker container, Flask on port 7860 |
| Alt Backend | **Render** | Gunicorn, 1 worker + 2 threads (free tier) |

The frontend polls `/api/health` every 2 seconds on load and shows a startup screen while the backend wakes up from cold start — common on free-tier hosting.

---

## Tech Stack

**Backend**
- Python, Flask, Gunicorn
- `sentence-transformers` — MiniLM embedding model
- `scikit-learn` — Random Forest Classifier & Regressor
- `PyTorch` (CPU build) — model runtime
- `NLTK` — tokenization, lemmatization, stopwords
- `pandas`, `numpy`, `joblib`
- Docker (for Hugging Face Spaces)

**Frontend**
- Next.js 16, React 19, TypeScript
- Framer Motion — animations
- Monaco Editor — in-browser code editor
- Recharts — score history charts
- html2pdf.js — PDF export
- Tailwind CSS v4, Radix UI, shadcn/ui, Lucide React

---

## Project Structure

```
interview_answer_analyzer/
├── AI_Interview_Bot/
│   ├── app.py                        # Flask API server
│   ├── semantic_evaluator.py         # MiniLM + RF scoring (active)
│   ├── random_forest_evaluator.py    # 23-feature RF classifier
│   ├── tfidf_evaluator.py            # Custom TF-IDF engine
│   ├── dataset_loader.py             # Smart CSV scanner + cache
│   ├── reference_answer_loader.py    # Reference Q&A organizer
│   ├── train_and_compare_semantic.py # Model benchmark script
│   ├── Dockerfile                    # For Hugging Face Spaces
│   └── real_dataset_score/
│       ├── semantic_rf_model.joblib  # 3.4MB — active model
│       ├── random_forest_model.joblib
│       ├── interview_data_with_scores.csv
│       └── stackoverflow_training_data.csv
├── frontend/
│   └── src/app/
│       ├── page.tsx                  # Main UI (VS Code interface)
│       └── api/                     # Next.js proxy routes
├── requirements.txt
├── render.yaml
└── PROJECT_REPORT.md                 # Full technical documentation
```

---

## License

MIT — feel free to use, fork, and build on top of this.

---

*Built with the goal of making interview practice feel less like studying and more like coding.*
