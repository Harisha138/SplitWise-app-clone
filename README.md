

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
### ** WHAT PROBLEM DOES IT SOLVE?**

**Real-World Problem:**

- Friends go on trips together and share expenses
- Someone buys groceries, someone pays for gas, someone books the hotel
- At the end, who owes whom? How much? It gets complicated quickly


**Example Scenario:**

```plaintext
Trip with 3 friends: Alice, Bob, Charlie
- Alice pays $300 for hotel (split equally)
- Bob pays $60 for groceries (split equally)
- Charlie pays $90 for gas (split percentage-based)

Who owes whom? The calculations become complex with multiple expenses 
and different split methods.
```

**Solution:** Splitwise automates this completely and accurately.

---

### ** CORE FEATURES**

#### **Feature 1: User Management**

- Create users with names and email
- View user profiles
- Track individual balance across all groups


#### **Feature 2: Group Management**

- Create expense groups (e.g., "Weekend Trip", "Roommate Expenses")
- Add multiple members to each group
- Track total expenses per group


#### **Feature 3: Expense Tracking**

- Add expenses with description and amount
- Specify who paid for the expense
- Two split types:

- **Equal Split**: Divides expense equally among group members
- **Percentage Split**: Custom percentages for each person





#### **Feature 4: Balance Calculation**

- Automatic calculation of who owes whom
- Shows net balances between group members
- Prevents over-payment scenarios
- Accurate to the cent (no rounding errors)


#### **Feature 5: AI Chatbot**

- Ask natural language questions about expenses
- Example queries:

- "How much does Alice owe in Weekend Trip?"
- "Show me my latest 3 expenses"
- "Who paid the most in Office Lunch?"



- Fallback responses ensure reliability


---

## ** TECHNICAL ARCHITECTURE**

### **Frontend (React + TypeScript)**

- Modern, responsive UI with TailwindCSS
- Type-safe development with TypeScript
- Component-based architecture
- Real-time state management
- Interactive forms with validation


### **Backend (FastAPI + Python)**

- RESTful API with automatic OpenAPI documentation
- Pydantic for data validation
- SQLAlchemy ORM for database operations
- Complex business logic for balance calculations
- Integration with Hugging Face AI models


### **Database (PostgreSQL)**

- Relational design for data integrity
- ACID compliance for financial data
- Normalized schema preventing data duplication
- Supports complex queries for balance calculations


### **Infrastructure (Docker)**

- Multi-container setup (Frontend, Backend, Database)
- Consistent development and production environment
- Easy scaling and deployment
- Environment-agnostic configuration


---

## ** IMPRESSIVE TECHNICAL ASPECTS**


### **AI Integration**

- Integrated Hugging Face API for natural language processing
- Built intelligent fallback system for reliability
- Demonstrates understanding of modern AI/ML
- Context-aware responses using actual database data


### **API Design**

- RESTful principles followed correctly
- Automatic API documentation (Swagger/OpenAPI)
- Proper error handling and validation
- CORS configuration for cross-origin requests


### **Data Integrity**

- Handles edge cases (refunds, adjustments, rounding)
- Prevents inconsistent states
- Validates all inputs at multiple levels
- Uses database constraints for enforcement
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
