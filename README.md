# 🚀 Startup Idea Evaluator API

A scalable, JWT-secured backend built with **FastAPI**, designed to evaluate user-submitted startup ideas using **OpenAI's GPT API**. It allows authenticated users to submit ideas and receive structured AI feedback scored across five categories. Ideal for product validation, ideation tools, or investor pitch pre-analysis.

---

## ✨ Features

* 🔐 **JWT Authentication** (SignUp & Login with scoped access)
* 💡 **AI-Powered Startup Evaluation**

  * Creativity
  * Demand
  * Uniqueness
  * Scalability
  * Investment readiness
* 🧠 **OpenAI GPT Integration** via `gpt-4o-mini`
* 📦 **Database Storage** of evaluated ideas per user
* 📈 **Scalable Architecture** – future-ready to add premium usage limits or analytics
* 🗃️ **Usage History** – fetch user-specific past evaluations
* 🛡️ **Custom Free Usage Control** (usage tracking logic ready)
* 🔌 **Modular FastAPI Router Design**

---

## 🔧 Tech Stack

* **Framework**: FastAPI (with APIRouter modular structure)
* **Auth**: JWT via OAuth2 with token-based flow
* **Database**: SQLAlchemy ORM + PostgreSQL / SQLite
* **AI API**: OpenAI GPT via `openai` Python SDK
* **Env Management**: `python-dotenv`
* **Schema Validation**: Pydantic

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Asthraris/AI-StartUp-Idea-Validator.git
cd startup-evaluator-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup `.env`

```env
OPENAI_KEY=sk-xxxxxxxxxxxxxxxxxx
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Run the server

```bash
uvicorn app.main:app 
```

---

## 📑 API Routes Overview

### 🔐 Auth Routes

| Method | Route          | Description         |
| ------ | -------------- | ------------------- |
| POST   | `/auth/signup` | Register new user   |
| POST   | `/auth/login`  | Login and get token |

> Each route returns a **JWT token** to be used in Authorization header:
> `Authorization: Bearer <token>`

---

### 💡 Idea Routes

| Method | Route            | Description                              |
| ------ | ---------------- | ---------------------------------------- |
| POST   | `/ideas`         | Submit a startup idea and get evaluation |
| GET    | `/ideas/history` | View your previously submitted ideas     |

> **Note:** Auth required for both routes.

---

## 🧠 Example AI Output Format

```json
{
  "startup_idea": "AI-powered mental health assistant for teens",
  "evaluation": {
    "creativity": {
      "sentence": "Unique blend of AI and mental wellness tools.",
      "score": 8
    },
    "demand": {
      "sentence": "High demand due to rising teen mental health issues.",
      "score": 9
    },
    ...
  }
}
```

---

## 🔐 JWT Auth Flow

* After login/signup, you get a token.
* Include it in your request headers:

```http
Authorization: Bearer <your_token>
```

---

## 📡 Scalable Usage Control (Pluggable)

The system is structured to support **per-user usage limits** (e.g., 3 free evaluations). This logic can be extended to support:

* Tiered API access
* Premium unlocks
* Billing integration

---

## 📦 Future Roadmap

* [ ] Rate limiting & quota management
* [ ] Admin dashboard with analytics
* [ ] User-defined evaluation criteria
* [ ] Support for team-based accounts
* [ ] Export results as PDF/CSV
* [ ] Frontend integration (Next.js/Flutter/React)

---

## 🪪 License

MIT – free to use and extend.

---

## 👨‍💻 Author

**Aman Gupta**
*Inspired by innovation, powered by AI.*