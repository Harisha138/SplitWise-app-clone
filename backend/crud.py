from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from typing import List, Dict
from collections import defaultdict

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    # Add members to group
    for user_id in group.user_ids:
        db_member = models.GroupMember(group_id=db_group.id, user_id=user_id)
        db.add(db_member)
    
    db.commit()
    return db_group

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    """Get all groups with their members and expenses"""
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_expense(db: Session, group_id: int, expense: schemas.ExpenseCreate):
    # Convert enum to string value
    split_type_value = expense.split_type.value if hasattr(expense.split_type, 'value') else str(expense.split_type)
    
    db_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        paid_by=expense.paid_by,
        group_id=group_id,
        split_type=split_type_value  # Store as string
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Calculate splits
    group = get_group(db, group_id)
    member_count = len(group.members)
    
    if split_type_value == "equal":
        split_amount = expense.amount / member_count
        for member in group.members:
            db_split = models.ExpenseSplit(
                expense_id=db_expense.id,
                user_id=member.user_id,
                amount=split_amount,
                percentage=100.0 / member_count
            )
            db.add(db_split)
    else:  # PERCENTAGE
        for split in expense.splits:
            split_amount = (expense.amount * split.percentage) / 100
            db_split = models.ExpenseSplit(
                expense_id=db_expense.id,
                user_id=split.user_id,
                amount=split_amount,
                percentage=split.percentage
            )
            db.add(db_split)
    
    db.commit()
    return db_expense

def get_group_balances(db: Session, group_id: int):
    # Get all expenses and splits for the group
    expenses = db.query(models.Expense).filter(models.Expense.group_id == group_id).all()
    
    # Calculate balances
    user_balances = defaultdict(float)  # net balance for each user
    user_names = {}
    
    for expense in expenses:
        # Payer gets positive balance
        user_balances[expense.paid_by] += expense.amount
        user_names[expense.paid_by] = expense.payer.name
        
        # Each split participant gets negative balance
        for split in expense.splits:
            user_balances[split.user_id] -= split.amount
            user_names[split.user_id] = split.user.name
    
    # Convert to balance format
    balances = []
    for user_id, net_balance in user_balances.items():
        owes_to = []
        owed_by = []
        
        if net_balance < 0:  # User owes money
            # Find who they owe to (users with positive balances)
            debt = abs(net_balance)
            for creditor_id, creditor_balance in user_balances.items():
                if creditor_balance > 0 and creditor_id != user_id:
                    owe_amount = min(debt, creditor_balance)
                    if owe_amount > 0:
                        owes_to.append({
                            "user_id": creditor_id,
                            "user_name": user_names[creditor_id],
                            "amount": round(owe_amount, 2)
                        })
                        debt -= owe_amount
                        if debt <= 0:
                            break
        
        elif net_balance > 0:  # User is owed money
            credit = net_balance
            for debtor_id, debtor_balance in user_balances.items():
                if debtor_balance < 0 and debtor_id != user_id:
                    owed_amount = min(credit, abs(debtor_balance))
                    if owed_amount > 0:
                        owed_by.append({
                            "user_id": debtor_id,
                            "user_name": user_names[debtor_id],
                            "amount": round(owed_amount, 2)
                        })
                        credit -= owed_amount
                        if credit <= 0:
                            break
        
        balances.append(schemas.Balance(
            user_id=user_id,
            user_name=user_names[user_id],
            owes_to=owes_to,
            owed_by=owed_by,
            net_balance=round(net_balance, 2)
        ))
    
    return balances

def get_user_balances(db: Session, user_id: int):
    # Get all groups the user is part of
    user_groups = db.query(models.GroupMember).filter(models.GroupMember.user_id == user_id).all()
    
    group_balances = []
    total_net_balance = 0
    
    for group_member in user_groups:
        group_balance_data = get_group_balances(db, group_member.group_id)
        user_balance_in_group = next((b for b in group_balance_data if b.user_id == user_id), None)
        
        if user_balance_in_group:
            group_balances.append({
                "group_id": group_member.group_id,
                "group_name": group_member.group.name,
                "net_balance": user_balance_in_group.net_balance,
                "owes_to": user_balance_in_group.owes_to,
                "owed_by": user_balance_in_group.owed_by
            })
            total_net_balance += user_balance_in_group.net_balance
    
    user = get_user(db, user_id)
    return schemas.UserBalance(
        user_id=user_id,
        user_name=user.name,
        groups=group_balances,
        total_net_balance=round(total_net_balance, 2)
    )
