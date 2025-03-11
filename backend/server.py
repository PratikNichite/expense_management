# dependencies
from fastapi import FastAPI
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

# api
app = FastAPI()

# response model
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

# get routes
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses(expense_date)
    return expenses