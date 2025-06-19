

---

# 💰 Splitwise Clone - Expense Splitting Made Easy

A modern expense-splitting app built with **FastAPI**, **React**, **PostgreSQL**, and an **AI-powered chatbot**.

![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20PostgreSQL-blue) ![AI Powered](https://img.shields.io/badge/AI-Hugging%20Face-orange)

---

## 🚀 Features

* 👥 Group Management
* 💸 Smart Expense Splitting
* 📊 Balance Tracking
* 🤖 AI Chatbot
* 📱 Responsive Design
* 🐳 Docker Ready (1-command deploy)

---

## 🛠️ Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, Pydantic
**Frontend:** React 18, TypeScript, TailwindCSS, React Router
**AI & DevOps:** Hugging Face, Docker, Docker Compose

---

## 🚀 Quick Start

### Prerequisites

* Docker & Docker Compose
* Git

### Installation

```bash
# Clone repo
git clone https://github.com/Harisha138/SplitWise-app-clone.git
cd splitwise-app-clone

# Start app
docker-compose up --build
```

App runs at: [http://localhost:3000](http://localhost:3000)

---

## 🤖 AI Chatbot Setup (Optional)

1️⃣ Get free API key from [Hugging Face](https://huggingface.co/settings/tokens)
2️⃣ Create `.env`:

```env
HUGGINGFACE_API_KEY=your_api_key_here
```

3️⃣ Restart app:

```bash
docker-compose up --build
```

---

## 🏗️ Architecture

```
React (3000)  ⇄  FastAPI (8000)  ⇄  PostgreSQL (5432)
                     ⇣
               Hugging Face (AI)
```

---

## 📖 Usage

1️⃣ Create Users
2️⃣ Create Groups
3️⃣ Add Expenses
4️⃣ View Balances
5️⃣ Ask AI (chat button)

---

## 📊 API Docs

Visit:

* [http://localhost:8000/docs](http://localhost:8000/docs)
* [http://localhost:8000/redoc](http://localhost:8000/redoc)

**Key Endpoints:**

* `POST /users/`
* `POST /groups/`
* `POST /groups/{id}/expenses`
* `GET /groups/{id}/balances`
* `POST /chat`

---

## 🔧 Dev Tips

### Local Dev

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

### DB Management

```bash
docker-compose exec db psql -U user -d splitwise
docker-compose logs db
docker-compose down -v && docker-compose up --build
```

---

## 🧪 Testing

```bash
docker-compose ps
docker-compose logs backend
```

---

## 🚀 Deployment

```bash
docker-compose -f docker-compose.prod.yml up --build
```

---

## 🤝 Contributing

1️⃣ Fork repo
2️⃣ Create branch
3️⃣ Commit + push
4️⃣ PR 🚀

---

## 🙏 Acknowledgments

* [Splitwise](https://splitwise.com) (inspiration)
* [Hugging Face](https://huggingface.co)
* [FastAPI](https://fastapi.tiangolo.com)
* [React](https://reactjs.org)

---

⭐ **Star this repo if you found it helpful!**

---

## 📸 Screenshots

<img src="./Screenshot%202025-06-18%20204747.png" width="100%">
<img src="./Screenshot%202025-06-18%20204737.png" width="100%">
<img src="./Screenshot%20(152).png" width="100%">
<img src="./Screenshot%202025-06-18%20205310.png" width="100%">
<img src="./Screenshot%202025-06-18%20204810.png" width="100%">

---
