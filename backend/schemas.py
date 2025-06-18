from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SplitType(str, Enum):
    EQUAL = "equal"
    PERCENTAGE = "percentage"

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GroupMemberCreate(BaseModel):
    user_id: int

class GroupMember(BaseModel):
    id: int
    user_id: int
    user: User
    
    class Config:
        from_attributes = True

class GroupCreate(BaseModel):
    name: str
    user_ids: List[int]

class Group(BaseModel):
    id: int
    name: str
    created_at: datetime
    members: List[GroupMember]
    
    class Config:
        from_attributes = True

class ExpenseSplitCreate(BaseModel):
    user_id: int
    percentage: Optional[float] = None

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    paid_by: int
    split_type: SplitType
    splits: Optional[List[ExpenseSplitCreate]] = None

class ExpenseSplit(BaseModel):
    id: int
    user_id: int
    amount: float
    percentage: Optional[float]
    user: User
    
    class Config:
        from_attributes = True

class Expense(BaseModel):
    id: int
    description: str
    amount: float
    paid_by: int
    split_type: SplitType
    created_at: datetime
    payer: User
    splits: List[ExpenseSplit]
    
    class Config:
        from_attributes = True

class GroupDetails(Group):
    expenses: List[Expense]
    total_expenses: float

class Balance(BaseModel):
    user_id: int
    user_name: str
    owes_to: List[dict]  # [{"user_id": int, "user_name": str, "amount": float}]
    owed_by: List[dict]  # [{"user_id": int, "user_name": str, "amount": float}]
    net_balance: float

class UserBalance(BaseModel):
    user_id: int
    user_name: str
    groups: List[dict]  # Group balances across all groups
    total_net_balance: float
