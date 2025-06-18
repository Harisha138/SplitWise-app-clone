#!/usr/bin/env python3
"""Test script to verify backend can start"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        import fastapi
        print(f"✓ FastAPI: {fastapi.__version__}")
        
        import uvicorn
        print(f"✓ Uvicorn: {uvicorn.__version__}")
        
        import sqlalchemy
        print(f"✓ SQLAlchemy: {sqlalchemy.__version__}")
        
        import psycopg2
        print(f"✓ psycopg2: {psycopg2.__version__}")
        
        import pydantic
        print(f"✓ Pydantic: {pydantic.__version__}")
        
        # Test local imports
        import models
        print("✓ models module")
        
        import schemas
        print("✓ schemas module")
        
        import crud
        print("✓ crud module")
        
        import database
        print("✓ database module")
        
        import chatbot
        print("✓ chatbot module")
        
        print("All imports successful!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_app_creation():
    """Test if FastAPI app can be created"""
    try:
        print("\nTesting app creation...")
        import main
        app = main.app
        print("✓ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        return False

def main():
    print("Backend Startup Test")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print()
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_app_creation():
        success = False
    
    if success:
        print("\n✓ All tests passed! Backend should start successfully.")
        return 0
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
