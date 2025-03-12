# dependencies
from fastapi import FastAPI
from datetime import date
import db_helper
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd

# api
app = FastAPI()

# response model
class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    category: str
    notes: Optional[str] = None

# request model
class DateRange(BaseModel):
    start_date: date
    end_date: date


# get routes
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses(expense_date)
    return expenses

@app.get("/month/expenses")
def get_category_summary():
    expenses = db_helper.fetch_month_summary()
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

@app.post("/category/expenses/")
def get_category_summary(date_range: DateRange):
    expenses = db_helper.fetch_category_summary(date_range.start_date, date_range.end_date)
    
    expense_summary = {
        "category": [item["category"] for item in expenses],
        "total": [item["total"] for item in expenses]
    }
    
    df_expense_summary = pd.DataFrame(expense_summary)
    df_expense_summary["percentage"] = (df_expense_summary["total"] / df_expense_summary["total"].sum()) * 100
    return df_expense_summary

# patch routes
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