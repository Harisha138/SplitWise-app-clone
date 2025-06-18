# 💰 Splitwise Clone - Expense Splitting Made Easy

A modern expense splitting application built with **FastAPI**, **React**, and **PostgreSQL**, featuring an **AI-powered chatbot** for natural language queries.

![Splitwise Demo](https://img.shields.io/badge/Demo-Live-green) ![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20PostgreSQL-blue) ![AI Powered](https://img.shields.io/badge/AI-Hugging%20Face-orange)

## 🚀 Features

- **👥 Group Management** - Create groups and manage members
- **💸 Smart Expense Splitting** - Equal or percentage-based splits
- **📊 Balance Tracking** - See who owes whom at a glance
- **🤖 AI Chatbot** - Ask questions in natural language
- **📱 Responsive Design** - Works on desktop and mobile
- **🐳 Docker Ready** - One-command deployment

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Robust database
- **SQLAlchemy** - Powerful ORM
- **Pydantic** - Data validation

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe JavaScript
- **TailwindCSS** - Utility-first styling
- **React Router** - Client-side routing

### AI & DevOps
- **Hugging Face** - AI-powered chatbot
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation
\`\`\`bash
# Clone the repository
git clone https://github.com/Harisha138/SplitWise-app-clone.git
cd splitwise-clone

# Start the application
docker-compose up --build

# Access the app
open http://localhost:3000
\`\`\`

That's it! The app will be running with sample data.

## 🤖 AI Chatbot Setup (Optional)

1. Get a free API key from [Hugging Face](https://huggingface.co/settings/tokens)
2. Create a `.env` file:
   \`\`\`bash
   HUGGINGFACE_API_KEY=your_api_key_here
   \`\`\`
3. Restart the application

The chatbot works without an API key too (with basic functionality).

## 📖 Usage Guide

### 1. Create Users
- Navigate to "Users" tab
- Add users who will participate in expense splitting

### 2. Create Groups
- Click "Create Group"
- Add members and give it a name

### 3. Add Expenses
- Go to a group's detail page
- Click "Add Expense"
- Choose equal or percentage split

### 4. Check Balances
- View group balances to see who owes whom
- Check individual user balances across all groups

### 5. Ask the AI
- Click the chat button (bottom-right)
- Ask questions like "How much does Alice owe?"

## 🏗️ Architecture

\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   FastAPI       │    │  PostgreSQL     │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
│   Port 3000     │    │   Port 8000     │    │   Port 5432     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Hugging Face   │
                    │   (AI Models)   │
                    └─────────────────┘
\`\`\`

## 🔧 Development

### Local Development
\`\`\`bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
\`\`\`

### Database Management
\`\`\`bash
# View logs
docker-compose logs db

# Access database
docker-compose exec db psql -U user -d splitwise

# Reset database
docker-compose down -v
docker-compose up --build
\`\`\`

## 📊 API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Key Endpoints
- `POST /users/` - Create user
- `POST /groups/` - Create group
- `POST /groups/{id}/expenses` - Add expense
- `GET /groups/{id}/balances` - Get balances
- `POST /chat` - AI chatbot query

## 🧪 Testing

\`\`\`bash
# Test backend connectivity
python scripts/test_backend.py

# Check all services
bash scripts/check_services.sh

# View service status
docker-compose ps
\`\`\`

## 🚀 Deployment

### Docker Production
\`\`\`bash
# Build for production
docker-compose -f docker-compose.prod.yml up --build

# Or deploy to cloud platforms:
# - Vercel (Frontend)
# - Railway/Render (Backend)
# - Supabase/Neon (Database)
\`\`\`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [Splitwise](https://splitwise.com) for inspiration
- [Hugging Face](https://huggingface.co) for AI models
- [FastAPI](https://fastapi.tiangolo.com) for the amazing framework
- [React](https://reactjs.org) team for the UI library


---

⭐ **Star this repo if you found it helpful!**
\`\`\`

## 📸 Screenshots

<img src="./Screenshot 2025-06-18 204747.png" width="100%">
<img src="./Screenshot 2025-06-18 204737.png" width="100%">
<img src="./Screenshot (152).png" width="100%">
<img src="./Screenshot 2025-06-18 205310.png" width="100%">
<img src="./Screenshot 2025-06-18 204810.png" width="100%">