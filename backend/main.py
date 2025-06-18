import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

try:
    import crud
    import models
    import schemas
    from database import SessionLocal, engine, get_db
    from chatbot import ChatbotService
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

# Create tables
try:
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}")

app = FastAPI(title="Splitwise API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Splitwise API is running"}

@app.get("/")
def read_root():
    return {"message": "Splitwise API is running!"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_users(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Group endpoints
@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_group(db=db, group=group)
    except Exception as e:
        print(f"Error creating group: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating group: {str(e)}")

@app.get("/groups/", response_model=List[schemas.GroupDetails])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all groups with their details"""
    try:
        groups = crud.get_groups(db, skip=skip, limit=limit)
        group_details = []
        
        for group in groups:
            total_expenses = sum(expense.amount for expense in group.expenses)
            group_detail = schemas.GroupDetails(
                id=group.id,
                name=group.name,
                created_at=group.created_at,
                members=group.members,
                expenses=group.expenses,
                total_expenses=total_expenses
            )
            group_details.append(group_detail)
        
        return group_details
    except Exception as e:
        print(f"Error fetching groups: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching groups: {str(e)}")

@app.get("/groups/{group_id}", response_model=schemas.GroupDetails)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    total_expenses = sum(expense.amount for expense in db_group.expenses)
    
    return schemas.GroupDetails(
        id=db_group.id,
        name=db_group.name,
        created_at=db_group.created_at,
        members=db_group.members,
        expenses=db_group.expenses,
        total_expenses=total_expenses
    )

# Expense endpoints
@app.post("/groups/{group_id}/expenses", response_model=schemas.Expense)
def create_expense(
    group_id: int, 
    expense: schemas.ExpenseCreate, 
    db: Session = Depends(get_db)
):
    print(f"Received expense creation request for group {group_id}: {expense}")
    
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    try:
        result = crud.create_expense(db=db, group_id=group_id, expense=expense)
        print(f"Expense created successfully: {result}")
        return result
    except Exception as e:
        print(f"Error creating expense: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating expense: {str(e)}")

# Balance endpoints
@app.get("/groups/{group_id}/balances", response_model=List[schemas.Balance])
def read_group_balances(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return crud.get_group_balances(db, group_id=group_id)

@app.get("/users/{user_id}/balances", response_model=schemas.UserBalance)
def read_user_balances(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.get_user_balances(db, user_id=user_id)

# Chatbot endpoints
@app.post("/chat")
async def chat_query(
    query_data: dict,
    db: Session = Depends(get_db)
):
    query = query_data.get("query", "")
    user_context = query_data.get("user_context", {})
    
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        chatbot = ChatbotService(db)
        response = await chatbot.process_query(query, user_context)
        
        return {
            "query": query,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"Chatbot error: {e}")
        return {
            "query": query,
            "response": "I'm sorry, I encountered an error processing your request.",
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/chat/stats")
def get_chat_stats(db: Session = Depends(get_db)):
    try:
        chatbot = ChatbotService(db)
        return chatbot.get_quick_stats()
    except Exception as e:
        print(f"Chat stats error: {e}")
        return {
            "total_users": 0,
            "total_groups": 0,
            "total_expenses": 0,
            "recent_expenses": []
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
