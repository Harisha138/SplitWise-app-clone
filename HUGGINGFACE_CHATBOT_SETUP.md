# Hugging Face AI Chatbot Setup Guide

## Overview

This chatbot implementation uses **Hugging Face** instead of OpenAI, offering:
- **Free tier available** (no credit card required for basic usage)
- **Multiple AI models** to choose from
- **Cost-effective** paid tiers
- **Open-source models** option

## Setup Options

### Option 1: Free Usage (No API Key Required)

The chatbot will work **without any API key** using Hugging Face's free inference API, but with limitations:
- Rate limiting (slower responses)
- Model loading delays
- Basic functionality

**To use for free:**
1. No setup required - just start the application
2. The chatbot will use fallback responses when the API is rate-limited

### Option 2: Free Hugging Face Account (Recommended)

1. **Create a free account** at [Hugging Face](https://huggingface.co/)
2. **Generate an API token**:
   - Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Choose "Read" access
   - Copy the token

3. **Set the environment variable**:
   \`\`\`bash
   export HUGGINGFACE_API_KEY=your_hf_token_here
   \`\`\`

4. **Start the application**:
   \`\`\`bash
   docker-compose up --build
   \`\`\`

### Option 3: Hugging Face Pro ($9/month)

For better performance and higher rate limits:
- Faster model loading
- Higher request limits
- Priority access to models

## Available AI Models

The chatbot is configured to use these models (you can change them in \`backend/chatbot.py\`):

### Text Generation Models:
- **mistralai/Mistral-7B-Instruct-v0.1** (Default) - Best quality
- **microsoft/DialoGPT-large** - Good for conversations
- **facebook/blenderbot-400M-distill** - Faster responses
- **google/flan-t5-large** - Good instruction following

### How to Change Models:

Edit \`backend/chatbot.py\`:
\`\`\`python
# Change this line to use a different model
self.text_generation_url = "https://api-inference.huggingface.co/models/MODEL_NAME_HERE"
\`\`\`

## Setup Instructions

### Method 1: Using Environment Variables (Recommended)

1. **Create a \`.env\` file** in your project root:
   \`\`\`bash
   touch .env
   \`\`\`

2. **Add your Hugging Face token** (optional but recommended):
   \`\`\`
   HUGGINGFACE_API_KEY=your_hf_token_here
   \`\`\`

3. **Start the application**:
   \`\`\`bash
   docker-compose up --build
   \`\`\`

### Method 2: Export Environment Variable

\`\`\`bash
export HUGGINGFACE_API_KEY=your_hf_token_here
docker-compose up --build
\`\`\`

### Method 3: No API Key (Free with Limitations)

\`\`\`bash
# Just start without any API key
docker-compose up --build
\`\`\`

## Testing the Chatbot

1. **Open the application** at http://localhost:3000
2. **Click the blue chat button** in the bottom-right corner (with "HF" badge)
3. **Try these example queries**:
   - "What are the current balances?"
   - "Show me recent expenses"
   - "What's the total expenses?"
   - "List all groups"
   - "Who owes money in Weekend Trip?"

## Features & Capabilities

### Smart Fallback System
- **AI-powered responses** when Hugging Face API is available
- **Rule-based responses** when API is rate-limited or unavailable
- **Seamless switching** between AI and fallback modes

### Supported Query Types
- **Balance queries**: "How much does Alice owe?"
- **Expense queries**: "Show me recent expenses"
- **Group queries**: "List all groups"
- **Total calculations**: "What's the total expenses?"
- **User-specific queries**: "Who paid the most?"

### Context Awareness
- Understands current page context
- Provides relevant suggestions
- Maintains conversation history

## Troubleshooting

### "Model is loading" Messages
- **Cause**: Hugging Face models need to "warm up" when not used recently
- **Solution**: Wait 30-60 seconds and try again
- **Prevention**: Use a Hugging Face Pro account for faster model loading

### Rate Limiting
- **Free tier**: Limited requests per hour
- **Solution**: Wait a few minutes between requests
- **Upgrade**: Get Hugging Face Pro for higher limits

### Fallback Responses
- **When**: API is unavailable or rate-limited
- **What**: Rule-based responses using your actual data
- **Quality**: Still helpful, just not AI-generated

### No Responses
- **Check backend logs**: \`docker-compose logs backend\`
- **Verify API token**: Make sure it's set correctly
- **Try different model**: Edit \`chatbot.py\` to use a different model

## Cost Comparison

| Service | Free Tier | Paid Tier | Notes |
|---------|-----------|-----------|-------|
| **Hugging Face** | ✅ Available | $9/month | Best value |
| **OpenAI** | $5 trial credit | Pay per use | More expensive |

### Hugging Face Pricing:
- **Free**: Rate-limited, model loading delays
- **Pro ($9/month)**: Higher limits, faster loading, priority access
- **Enterprise**: Custom pricing for high volume

## Advanced Configuration

### Using Local Models (Advanced)

For completely free usage, you can run models locally:

1. **Install Ollama** or **Hugging Face Transformers**
2. **Download models locally**
3. **Modify the chatbot service** to use local inference

### Custom Models

You can use any Hugging Face model by changing the URL in \`chatbot.py\`:

\`\`\`python
# Example: Using a different model
self.text_generation_url = "https://api-inference.huggingface.co/models/your-custom-model"
\`\`\`

## Security Notes

- **API tokens**: Keep them secure, don't commit to version control
- **Rate limiting**: Implement additional rate limiting for production
- **Data privacy**: Hugging Face processes your queries (check their privacy policy)

## Performance Tips

1. **Use Pro account** for better performance
2. **Choose appropriate models** (smaller = faster, larger = better quality)
3. **Implement caching** for common queries
4. **Use fallback responses** as backup

This setup gives you a powerful AI chatbot with much lower costs than OpenAI while maintaining good functionality!
\`\`\`
\`\`\`

Update the main README to reflect the Hugging Face integration:

```typescriptreact file="README.md"
[v0-no-op-code-block-prefix]# Splitwise Clone

A simplified expense splitting application built with FastAPI (Python) backend and React (TypeScript) frontend.

## Features

- **Group Management**: Create groups and add users
- **Expense Tracking**: Add expenses with equal or percentage-based splitting
- **Balance Calculation**: View who owes whom in each group
- **User Balances**: See personal balance summary across all groups
- **Clean UI**: Modern interface built with React and TailwindCSS

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database for persistence
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization

### Frontend
- **React 18**: UI framework with TypeScript
- **TailwindCSS**: Utility-first CSS framework
- **React Router**: Client-side routing

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation & Setup

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd splitwise-clone
   \`\`\`

2. **Start the application**
   \`\`\`bash
   docker-compose up --build
   \`\`\`

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

The application will automatically:
- Set up PostgreSQL database
- Install all dependencies
- Start both frontend and backend services
- Enable hot reloading for development

## API Documentation

### Users
- \`POST /users/\` - Create a new user
- \`GET /users/\` - Get all users
- \`GET /users/{user_id}\` - Get user by ID

### Groups
- \`POST /groups/\` - Create a new group
- \`GET /groups/{group_id}\` - Get group details with expenses

### Expenses
- \`POST /groups/{group_id}/expenses\` - Add expense to group
  - Supports equal and percentage splitting
  - Automatically calculates individual amounts

### Balances
- \`GET /groups/{group_id}/balances\` - Get group balance summary
- \`GET /users/{user_id}/balances\` - Get user's balance across all groups

## Usage Guide

### 1. Create Users
- Navigate to "Users" tab
- Click "Add User" to create new users
- Users need to exist before creating groups

### 2. Create Groups
- Click "Create Group" 
- Enter group name and select members
- Groups require at least one member

### 3. Add Expenses
- Go to a group's detail page
- Click "Add Expense"
- Choose between equal split or percentage split
- For percentage split, ensure percentages add up to 100%

### 4. View Balances
- Group balances show who owes whom within that group
- User balances show overall financial position across all groups
- Positive balance = owed money, Negative balance = owes money

## AI Chatbot Feature

The application includes an AI-powered chatbot that can answer natural language questions about your expenses and balances.

### Setup
1. **Optional**: Get a free Hugging Face token from [Hugging Face](https://huggingface.co/settings/tokens)
2. **Optional**: Set the environment variable:
   \`\`\`bash
   export HUGGINGFACE_API_KEY=your_hf_token_here
   \`\`\`
3. Start the application with Docker Compose (works without API key too!)

### Usage
- Click the green chat button in the bottom-right corner
- Ask questions like:
  - "How much does Alice owe in Weekend Trip?"
  - "Show me the latest 3 expenses"
  - "Who paid the most in Office Lunch?"
  - "What's my total balance?"

### Features
- **Free to use**: Works without any API key (with basic functionality)
- **Multiple AI models**: Uses Hugging Face's open-source models
- **Smart fallback**: Provides rule-based responses when AI is unavailable
- **Cost-effective**: Free tier available, Pro tier only $9/month

See [HUGGINGFACE_CHATBOT_SETUP.md](HUGGINGFACE_CHATBOT_SETUP.md) for detailed setup instructions.

## Project Structure

\`\`\`
splitwise-clone/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # Database configuration
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend container config
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API service layer
│   │   ├── App.tsx      # Main application component
│   │   └── index.tsx    # Application entry point
│   ├── package.json     # Node.js dependencies
│   └── Dockerfile       # Frontend container config
├── docker-compose.yml   # Multi-container setup
└── README.md           # This file
\`\`\`

## Development

### Running Locally (without Docker)

#### Backend
\`\`\`bash
cd backend
pip install -r requirements.txt
# Set up PostgreSQL and update DATABASE_URL in database.py
uvicorn main:app --reload
\`\`\`

#### Frontend
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`

### Database Schema

The application uses the following main entities:
- **Users**: Basic user information
- **Groups**: Expense groups with members
- **Expenses**: Individual expenses with split information
- **ExpenseSplits**: How each expense is divided among users

## Assumptions Made

1. **No Authentication**: Users are identified by ID only
2. **No Payment Processing**: Only tracks balances, no actual payments
3. **Simple User Management**: Users must be created before adding to groups
4. **Equal Split Default**: When creating equal splits, amounts are divided evenly
5. **Percentage Precision**: Percentages must add up to exactly 100%
6. **No Expense Editing**: Expenses cannot be modified after creation
7. **No Group Deletion**: Groups persist once created
8. **Currency**: All amounts assumed to be in USD

## Future Enhancements

- User authentication and authorization
- Expense editing and deletion
- Group management (add/remove members)
- Payment settlement tracking
- Multiple currency support
- Mobile responsive improvements
- Real-time updates with WebSockets
- Expense categories and tags
- Receipt image uploads
- Export functionality (PDF, CSV)

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL container is running
   - Check DATABASE_URL environment variable

2. **Frontend API Calls Failing**
   - Verify backend is running on port 8000
   - Check CORS configuration in main.py

3. **Docker Build Issues**
   - Run \`docker-compose down -v\` to clean up
   - Rebuild with \`docker-compose up --build\`

### Logs
\`\`\`bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes and is not intended for commercial use.
