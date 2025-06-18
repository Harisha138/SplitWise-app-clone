#!/usr/bin/env python3
import os
import sys
import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def wait_for_db():
    """Wait for database to be ready"""
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/splitwise")
    
    print("Waiting for database to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            engine = create_engine(db_url)
            connection = engine.connect()
            connection.close()
            print("Database is ready!")
            return True
        except OperationalError as e:
            retry_count += 1
            print(f"Database not ready (attempt {retry_count}/{max_retries}): {e}")
            time.sleep(2)
    
    print("Database failed to become ready!")
    return False

def main():
    print("Starting Splitwise Backend...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Check if database is ready
    if not wait_for_db():
        sys.exit(1)
    
    # Import and start the application
    try:
        import uvicorn
        print("Starting uvicorn server...")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
