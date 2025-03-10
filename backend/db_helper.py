from contextlib import contextmanager
import mysql.connector
from pydantic import BaseModel
import datetime


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="expense_manager"
    )
    
    if connection.is_connected():
        print("Connection established!")
    else:
        print("Failed to connect database!")
    
    cursor = connection.cursor(dictionary=True)
    
    yield cursor
    
    if commit:
        connection.commit()
    
    cursor.close()
    connection.close()


# Create functions
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

def create_expense(date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        query = "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (date, amount, category, notes))

# Read functions
def fetch_expenses(date):
    with get_db_cursor() as cursor:
        query = "SELECT * FROM expenses WHERE expense_date=%s"
        cursor.execute(query, (date,))
        expenses = cursor.fetchall()
        return expenses

# Update functions

# Delete functions


if __name__ == "__main__":
    create_expense(date="2025-01-01", amount=50, category="Food", notes="BurgerKing")
    print(fetch_expenses("2025-01-01"))
