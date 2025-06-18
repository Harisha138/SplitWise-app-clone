#!/usr/bin/env python3
import requests
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("Testing backend connectivity...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False
    
    # Test users endpoint
    try:
        response = requests.get(f"{base_url}/users/")
        print(f"Users endpoint: {response.status_code} - Found {len(response.json())} users")
    except Exception as e:
        print(f"Users endpoint failed: {e}")
        return False
    
    # Test CORS preflight
    try:
        response = requests.options(f"{base_url}/users/", headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        })
        print(f"CORS preflight: {response.status_code}")
        print(f"CORS headers: {dict(response.headers)}")
    except Exception as e:
        print(f"CORS preflight failed: {e}")
    
    print("Backend test completed!")
    return True

if __name__ == "__main__":
    test_backend()
