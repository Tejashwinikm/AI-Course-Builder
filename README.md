# AI Course Builder

**Stack: React + Flask + Python + LangChain + SQLite**

Type a topic → AI generates a structured course → YouTube videos embedded →
Quizzes generated → AI study notes → AI mentor chatbot → Progress tracked.

---

## Folder Structure

```
ai-course-builder-v2/
├── backend/
│   ├── app.py                        ← Flask entry point
│   ├── requirements.txt
│   ├── .env.example                  ← Copy to .env
│   ├── routes/
│   │   ├── course_routes.py          ← POST /api/course/generate
│   │   ├── quiz_routes.py            ← POST /api/quiz/generate
│   │   ├── video_routes.py           ← GET  /api/video/search
│   │   ├── notes_routes.py           ← POST /api/notes/generate
│   │   ├── progress_routes.py        ← GET/POST /api/progress/
│   │   └── mentor_routes.py          ← POST /api/mentor/ask
│   └── services/
│       ├── ai_service.py             ← LangChain + Claude (mock/live)
│       ├── youtube_service.py        ← YouTube search (mock/live)
│       ├── course_service.py         ← Main pipeline orchestrator
│       ├── notes_service.py          ← Transcript RAG notes
│       ├── progress_service.py       ← SQLite progress tracking
│       └── mentor_service.py         ← AI mentor chatbot
│
└── frontend/
    ├── package.json
    ├── public/index.html
    └── src/
        ├── App.js                    ← Screen manager
        ├── index.js
        ├── pages/
        │   ├── HomePage.js           ← Topic input + generate
        │   ├── CoursePage.js         ← All modules + progress bar
        │   └── LessonPage.js         ← Video + notes + mentor
        ├── components/
        │   ├── Navbar.js
        │   ├── ModuleCard.js
        │   ├── LessonRow.js
        │   ├── QuizPlayer.js         ← Interactive quiz + scoring
        │   ├── NotesPanel.js         ← AI notes generation
        │   ├── MentorChat.js         ← AI chatbot
        │   └── ProgressBar.js        ← Course progress tracker
        ├── utils/
        │   └── api.js                ← All axios calls to Flask
        └── styles/
            └── global.css
```

---

## Quick Start (Windows)

### Terminal 1 — Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Flask runs at: http://localhost:5000

### Terminal 2 — Frontend

```bash
cd frontend
npm install
npm start
```

React runs at: http://localhost:3000

---

## Mock Mode vs Live Mode

| Setting         | What happens                                    |
|-----------------|-------------------------------------------------|
| USE_MOCK=true   | No API keys needed — realistic mock data        |
| USE_MOCK=false  | Real Claude AI + real YouTube search            |

---
## API Keys

This project uses the following APIs:

1. **Google Gemini API**
   - Get your API key from: https://aistudio.google.com/apikey

2. **YouTube Data API v3**
   - Create an API key through Google Cloud Console:
     https://console.cloud.google.com/

Add the keys to `backend/.env`:

GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

## API Endpoints

| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| POST   | /api/course/generate      | Generate full course from topic    |
| POST   | /api/quiz/generate        | Generate quiz for a lesson         |
| GET    | /api/video/search?q=...   | Search YouTube videos              |
| POST   | /api/notes/generate       | Generate AI study notes            |
| POST   | /api/progress/register    | Register course for tracking       |
| POST   | /api/progress/complete    | Mark lesson/quiz complete          |
| GET    | /api/progress/<id>        | Get course progress                |
| POST   | /api/mentor/ask           | Ask AI mentor a question           |
| GET    | /api/health               | Health check + mode                |

---

## Features Built

- Prompt-to-course: type any topic → full structured course
- YouTube video embedding (50+ topic pools, 6-level matching)
- Topic-specific AI quizzes with scoring and feedback
- AI study notes (RAG: transcript → Claude → grounded notes)
- AI mentor chatbot (context-aware: lesson + progress)
- Progress tracking (SQLite: lessons done, quiz scores, % complete)
- Hallucination handling: retry + schema validation + fallback
- Mock/live mode toggle: develop without API keys

---

## Resume Bullets (accurate, defensible)

AI Course Builder — Prompt-to-Course Learning Platform
React, Flask, Python, LangChain, YouTube API, Anthropic Claude

• Developed a prompt-to-course platform that automatically generates
  structured learning modules from user-defined topics using LangChain
  to orchestrate Claude API calls via PromptTemplates and LCEL chains.

• Integrated YouTube Data API v3 with semantic topic-matching to embed
  relevant tutorial videos per lesson, and implemented transcript-based
  AI note generation (RAG pattern) using youtube-transcript-api + Claude.

• Built a Flask REST API (6 blueprints) with LLM hallucination handling
  (retry logic, JSON schema validation, graceful fallback), an AI mentor
  chatbot grounded in lesson context, and SQLite-backed progress tracking.
