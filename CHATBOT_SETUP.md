# AI Chatbot Setup Guide

## Prerequisites

1. **OpenAI API Key**: You need an OpenAI API key to use the chatbot feature.
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Create an API key in your dashboard
   - Make sure you have credits available

## Setup Instructions

### Method 1: Using Environment Variables (Recommended)

1. **Create a `.env` file** in your project root:
   \`\`\`bash
   touch .env
   \`\`\`

2. **Add your OpenAI API key** to the `.env` file:
   \`\`\`
   OPENAI_API_KEY=your_openai_api_key_here
   \`\`\`

3. **Start the application**:
   \`\`\`bash
   docker-compose up --build
   \`\`\`

### Method 2: Export Environment Variable

1. **Export the API key** in your terminal:
   \`\`\`bash
   export OPENAI_API_KEY=your_openai_api_key_here
   \`\`\`

2. **Start the application**:
   \`\`\`bash
   docker-compose up --build
   \`\`\`

### Method 3: Inline with Docker Compose

\`\`\`bash
OPENAI_API_KEY=your_openai_api_key_here docker-compose up --build
\`\`\`

## Testing the Chatbot

1. **Open the application** at http://localhost:3000
2. **Click the chat button** in the bottom-right corner (green circle with chat icon)
3. **Try these example queries**:
   - "How much does Alice owe in Weekend Trip?"
   - "Show me the latest 3 expenses"
   - "Who paid the most in Office Lunch?"
   - "What's the total expenses across all groups?"
   - "List all users and their balances"

## Chatbot Features

### Context Awareness
- The chatbot understands which page you're on
- Provides contextual suggestions based on current view
- Maintains conversation history during your session

### Natural Language Queries
- Ask questions in plain English
- Supports complex queries about balances, expenses, and groups
- Provides formatted, easy-to-read responses

### Smart Suggestions
- Context-aware quick questions
- Different suggestions based on current page
- Easy-to-click suggested queries

## Troubleshooting

### "API key not configured" Error
- Make sure your OpenAI API key is set correctly
- Verify the environment variable is loaded: \`echo $OPENAI_API_KEY\`
- Restart the Docker containers after setting the API key

### "Rate limit exceeded" Error
- You've hit OpenAI's rate limits
- Wait a few minutes before trying again
- Consider upgrading your OpenAI plan for higher limits

### "Insufficient credits" Error
- Your OpenAI account is out of credits
- Add credits to your OpenAI account
- Check your usage at https://platform.openai.com/usage

### Chatbot not responding
- Check backend logs: \`docker-compose logs backend\`
- Verify the backend is running on port 8000
- Make sure the database has data to query

## Customization

### Adding New Query Types
Edit \`backend/chatbot.py\` to add new query patterns or improve responses.

### Modifying UI
Edit \`frontend/src/components/ChatbotAdvanced.tsx\` to customize the chat interface.

### Changing AI Model
In \`backend/chatbot.py\`, you can change the model from \`gpt-3.5-turbo\` to \`gpt-4\` for better responses (higher cost).

## Cost Considerations

- GPT-3.5-turbo: ~$0.002 per 1K tokens
- Each query typically uses 200-500 tokens
- Monitor your usage at https://platform.openai.com/usage

## Security Notes

- Never commit your API key to version control
- Use environment variables for API keys
- Consider implementing rate limiting for production use
- The chatbot has access to all expense data - ensure proper access controls in production
\`\`\`

</QuickEdit>

Now let's update the main README to include chatbot information:

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
1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Set the environment variable:
   \`\`\`bash
   export OPENAI_API_KEY=your_api_key_here
   \`\`\`
3. Start the application with Docker Compose

### Usage
- Click the green chat button in the bottom-right corner
- Ask questions like:
  - "How much does Alice owe in Weekend Trip?"
  - "Show me the latest 3 expenses"
  - "Who paid the most in Office Lunch?"
  - "What's my total balance?"

### Features
- **Context-aware**: Understands which page you're viewing
- **Natural language**: Ask questions in plain English
- **Smart suggestions**: Provides relevant quick questions
- **Real-time data**: Always uses current expense and balance data

See [CHATBOT_SETUP.md](CHATBOT_SETUP.md) for detailed setup instructions.

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
