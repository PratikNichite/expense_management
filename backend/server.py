# dependencies
from fastapi import FastAPI
from datetime import date
import db_helper
from typing import List, Optional
from pydantic import BaseModel

# api
app = FastAPI()

# response model
class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    category: str
    notes: Optional[str] = None

# get routes
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses(expense_date)
    return expenses

# post routes
@app.post("/expenses/{expense_date}")
def add_expense(expense_date: date, expense: Expense):
    db_helper.create_expense(
        expense_date, 
        expense.amount,
        expense.category,
        expense.notes
    )
    
    return {"message": "Expense added successfully!"}

@app.patch("/expenses/{expense_date}")
def update_expenses(expense_date: date, expenses: List[Expense]):
    for expense in expenses:
        db_helper.update_expenses(
            expense_date,
            expense.id,
            expense.amount,
            expense.category,
            expense.notes
        )
        
    return {"message": "Expenses updated successfully!"}