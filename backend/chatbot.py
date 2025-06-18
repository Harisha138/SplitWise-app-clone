import requests
import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
import crud
import models
import os

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.hf_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        # Alternative models you can use:
        # "microsoft/DialoGPT-medium" - Faster, less accurate
        # "facebook/blenderbot-400M-distill" - Good for conversations
        # "microsoft/DialoGPT-large" - Better quality responses
        
        # For more advanced responses, you can use:
        self.text_generation_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    
    def get_context_data(self, user_id: int = None, group_id: int = None) -> Dict[str, Any]:
        """Gather relevant context data from the database"""
        context = {
            "users": [],
            "groups": [],
            "expenses": [],
            "balances": []
        }
        
        # Get all users
        users = crud.get_users(self.db, limit=100)
        context["users"] = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in users
        ]
        
        # Get groups and their details
        groups_query = self.db.query(models.Group).all()
        for group in groups_query:
            group_data = {
                "id": group.id,
                "name": group.name,
                "members": [
                    {
                        "id": member.user.id,
                        "name": member.user.name
                    }
                    for member in group.members
                ],
                "expenses": [],
                "total_expenses": 0
            }
            
            # Get expenses for this group
            for expense in group.expenses:
                expense_data = {
                    "id": expense.id,
                    "description": expense.description,
                    "amount": expense.amount,
                    "paid_by": expense.payer.name,
                    "paid_by_id": expense.paid_by,
                    "split_type": expense.split_type.value,
                    "created_at": expense.created_at.isoformat(),
                    "splits": [
                        {
                            "user_name": split.user.name,
                            "user_id": split.user_id,
                            "amount": split.amount
                        }
                        for split in expense.splits
                    ]
                }
                group_data["expenses"].append(expense_data)
                group_data["total_expenses"] += expense.amount
            
            # Get balances for this group
            try:
                balances = crud.get_group_balances(self.db, group.id)
                group_data["balances"] = [
                    {
                        "user_name": balance.user_name,
                        "user_id": balance.user_id,
                        "net_balance": balance.net_balance,
                        "owes_to": balance.owes_to,
                        "owed_by": balance.owed_by
                    }
                    for balance in balances
                ]
            except:
                group_data["balances"] = []
            
            context["groups"].append(group_data)
        
        return context
    
    def create_prompt(self, context: Dict[str, Any], query: str) -> str:
        """Create a comprehensive prompt for Hugging Face models"""
        
        # Summarize the context for the prompt
        context_summary = f"""
You are a helpful assistant for a Splitwise expense tracking application.

Current Data:
- Users: {len(context['users'])} users
- Groups: {len(context['groups'])} groups

Groups and Expenses:
"""
        
        for group in context['groups']:
            context_summary += f"\n{group['name']} Group:"
            context_summary += f"\n  Members: {', '.join([m['name'] for m in group['members']])}"
            context_summary += f"\n  Total Expenses: ${group['total_expenses']:.2f}"
            
            if group['expenses']:
                context_summary += f"\n  Recent Expenses:"
                for expense in group['expenses'][-3:]:  # Last 3 expenses
                    context_summary += f"\n    - {expense['description']}: ${expense['amount']:.2f} (paid by {expense['paid_by']})"
            
            if group['balances']:
                context_summary += f"\n  Balances:"
                for balance in group['balances']:
                    if balance['net_balance'] != 0:
                        status = "owes" if balance['net_balance'] < 0 else "is owed"
                        context_summary += f"\n    - {balance['user_name']}: {status} ${abs(balance['net_balance']):.2f}"
        
        # Create the full prompt
        full_prompt = f"""
{context_summary}

Instructions: Answer the user's question about expenses and balances based on the data above. 
Be helpful, concise, and format monetary amounts with $ symbol. If the requested information 
doesn't exist, explain what information is available instead.

User Question: {query}

Assistant Response:"""
        
        return full_prompt
    
    def query_huggingface_api(self, prompt: str) -> str:
        """Query Hugging Face API for text generation"""
        headers = {}
        if self.hf_api_key:
            headers["Authorization"] = f"Bearer {self.hf_api_key}"
        
        # Try the text generation model first
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                self.text_generation_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    return generated_text.strip()
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"].strip()
            
            # If the model is loading, try a simpler approach
            elif response.status_code == 503:
                return "The AI model is currently loading. Please try again in a moment."
                
        except Exception as e:
            print(f"Hugging Face API error: {e}")
        
        # Fallback to rule-based responses if API fails
        return self.get_fallback_response(prompt)
    
    def get_fallback_response(self, prompt: str) -> str:
        """Provide rule-based responses when API is unavailable"""
        query_lower = prompt.lower()
        
        # Get context data for fallback responses
        context = self.get_context_data()
        
        if "balance" in query_lower or "owe" in query_lower:
            # Find balance information
            response = "Here are the current balances:\n\n"
            for group in context['groups']:
                if group['balances']:
                    response += f"{group['name']} Group:\n"
                    for balance in group['balances']:
                        if balance['net_balance'] != 0:
                            if balance['net_balance'] < 0:
                                response += f"  • {balance['user_name']} owes ${abs(balance['net_balance']):.2f}\n"
                            else:
                                response += f"  • {balance['user_name']} is owed ${balance['net_balance']:.2f}\n"
                    response += "\n"
            return response
        
        elif "expense" in query_lower or "latest" in query_lower or "recent" in query_lower:
            # Show recent expenses
            all_expenses = []
            for group in context['groups']:
                for expense in group['expenses']:
                    expense['group_name'] = group['name']
                    all_expenses.append(expense)
            
            # Sort by date and get recent ones
            all_expenses.sort(key=lambda x: x['created_at'], reverse=True)
            recent_expenses = all_expenses[:5]
            
            if recent_expenses:
                response = "Here are the recent expenses:\n\n"
                for expense in recent_expenses:
                    response += f"• {expense['description']}: ${expense['amount']:.2f}\n"
                    response += f"  Paid by {expense['paid_by']} in {expense['group_name']}\n\n"
                return response
            else:
                return "No expenses found in the system."
        
        elif "total" in query_lower:
            # Calculate totals
            total_expenses = sum(group['total_expenses'] for group in context['groups'])
            response = f"Total expenses across all groups: ${total_expenses:.2f}\n\n"
            
            response += "Breakdown by group:\n"
            for group in context['groups']:
                response += f"• {group['name']}: ${group['total_expenses']:.2f}\n"
            
            return response
        
        elif "group" in query_lower:
            # List groups
            if context['groups']:
                response = "Here are your groups:\n\n"
                for group in context['groups']:
                    response += f"• {group['name']}\n"
                    response += f"  Members: {', '.join([m['name'] for m in group['members']])}\n"
                    response += f"  Total expenses: ${group['total_expenses']:.2f}\n\n"
                return response
            else:
                return "No groups found. Create a group to start tracking expenses!"
        
        else:
            return """I can help you with questions about your expenses and balances. Try asking:
            
• "What are the current balances?"
• "Show me recent expenses"
• "What's the total expenses?"
• "List all groups"
• "How much does [name] owe in [group]?"

Note: The AI model might be loading. For best results, try again in a moment."""
    
    async def process_query(self, query: str, user_context: Dict[str, Any] = None) -> str:
        """Process a natural language query and return a response"""
        try:
            # Get context data
            context = self.get_context_data()
            
            # Add user context if provided
            if user_context:
                context.update(user_context)
            
            # Create prompt
            prompt = self.create_prompt(context, query)
            
            # Query Hugging Face API
            response = self.query_huggingface_api(prompt)
            
            return response
            
        except Exception as e:
            return f"I encountered an error processing your request. Please try again. Error: {str(e)}"
    
    def get_quick_stats(self) -> Dict[str, Any]:
        """Get quick statistics for the chatbot"""
        context = self.get_context_data()
        
        stats = {
            "total_users": len(context["users"]),
            "total_groups": len(context["groups"]),
            "total_expenses": sum(group["total_expenses"] for group in context["groups"]),
            "recent_expenses": []
        }
        
        # Get recent expenses across all groups
        all_expenses = []
        for group in context["groups"]:
            for expense in group["expenses"]:
                expense["group_name"] = group["name"]
                all_expenses.append(expense)
        
        # Sort by date and get recent ones
        all_expenses.sort(key=lambda x: x["created_at"], reverse=True)
        stats["recent_expenses"] = all_expenses[:5]
        
        return stats
