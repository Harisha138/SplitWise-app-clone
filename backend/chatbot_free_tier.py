import requests
import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
import crud
import models
import os
import time

class FreeTierChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # Use faster, smaller models for free tier
        self.models = [
            "microsoft/DialoGPT-medium",  # Faster than large
            "distilgpt2",                 # Very fast
            "facebook/blenderbot-400M-distill"  # Good for chat
        ]
        self.current_model = 0
        
        # Cache for common responses
        self.response_cache = {}
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 2  # 2 seconds between requests
    
    def get_current_model_url(self):
        model_name = self.models[self.current_model]
        return f"https://api-inference.huggingface.co/models/{model_name}"
    
    def switch_to_next_model(self):
        """Switch to next model if current one fails"""
        self.current_model = (self.current_model + 1) % len(self.models)
        print(f"Switching to model: {self.models[self.current_model]}")
    
    def respect_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            print(f"Rate limiting: waiting {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def query_huggingface_api(self, prompt: str) -> str:
        """Query HF API with free tier optimizations"""
        
        # Check cache first
        cache_key = prompt[:100]  # Use first 100 chars as key
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        # Respect rate limits
        self.respect_rate_limit()
        
        headers = {}
        if self.hf_api_key:
            headers["Authorization"] = f"Bearer {self.hf_api_key}"
        
        # Optimized payload for free tier
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100,  # Reduced from 200
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "return_full_text": False
            },
            "options": {
                "wait_for_model": True,  # Wait for model to load
                "use_cache": True        # Use cached results
            }
        }
        
        max_retries = len(self.models)
        
        for attempt in range(max_retries):
            try:
                model_url = self.get_current_model_url()
                print(f"Trying model: {self.models[self.current_model]}")
                
                response = requests.post(
                    model_url,
                    headers=headers,
                    json=payload,
                    timeout=30  # Reduced timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "")
                        # Cache the response
                        self.response_cache[cache_key] = generated_text.strip()
                        return generated_text.strip()
                
                elif response.status_code == 503:
                    print("Model loading, trying next model...")
                    self.switch_to_next_model()
                    time.sleep(5)  # Wait before trying next model
                    continue
                
                elif response.status_code == 429:
                    print("Rate limited, waiting...")
                    time.sleep(10)
                    continue
                
                else:
                    print(f"API error: {response.status_code}")
                    self.switch_to_next_model()
                    continue
                    
            except Exception as e:
                print(f"Request failed: {e}")
                self.switch_to_next_model()
                continue
        
        # All models failed, use fallback
        return self.get_fallback_response(prompt)
    
    def get_fallback_response(self, prompt: str) -> str:
        """Enhanced fallback responses for free tier"""
        query_lower = prompt.lower()
        
        # Get context data for fallback responses
        context = self.get_context_data()
        
        if "balance" in query_lower or "owe" in query_lower:
            response = "💰 **Current Balances:**\n\n"
            for group in context['groups']:
                if group['balances']:
                    response += f"**{group['name']} Group:**\n"
                    for balance in group['balances']:
                        if balance['net_balance'] != 0:
                            if balance['net_balance'] < 0:
                                response += f"  • {balance['user_name']} owes ${abs(balance['net_balance']):.2f}\n"
                            else:
                                response += f"  • {balance['user_name']} is owed ${balance['net_balance']:.2f}\n"
                    response += "\n"
            return response
        
        elif "expense" in query_lower or "latest" in query_lower:
            all_expenses = []
            for group in context['groups']:
                for expense in group['expenses']:
                    expense['group_name'] = group['name']
                    all_expenses.append(expense)
            
            all_expenses.sort(key=lambda x: x['created_at'], reverse=True)
            recent_expenses = all_expenses[:5]
            
            if recent_expenses:
                response = "📋 **Recent Expenses:**\n\n"
                for expense in recent_expenses:
                    response += f"• **{expense['description']}**: ${expense['amount']:.2f}\n"
                    response += f"  Paid by {expense['paid_by']} in {expense['group_name']}\n\n"
                return response
        
        elif "total" in query_lower:
            total_expenses = sum(group['total_expenses'] for group in context['groups'])
            response = f"📊 **Total expenses across all groups**: ${total_expenses:.2f}\n\n"
            response += "**Breakdown by group:**\n"
            for group in context['groups']:
                response += f"• {group['name']}: ${group['total_expenses']:.2f}\n"
            return response
        
        else:
            return """🤖 **I'm your Splitwise assistant!** 

I can help you with:
• "What are the current balances?"
• "Show me recent expenses"  
• "What's the total expenses?"
• "List all groups"

*Note: Using free AI tier - responses may be slower but I'm always here to help with your expense data!*"""
    
    # ... rest of the methods remain the same ...
