from contextlib import contextmanager
import mysql.connector
from pydantic import BaseModel
from logging_setup import setup_logger

# logging setup
logger = setup_logger("db_logger", "server.log")

# database connection
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
    logger.info(f"create_expense called with {date}, {amount}, {category}, {notes}")
    with get_db_cursor(commit=True) as cursor:
        query = "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (date, amount, category, notes))

# Read functions
def fetch_expenses(date):
    logger.info(f"fetch_expenses called with {date}")
    with get_db_cursor() as cursor:
        query = "SELECT * FROM expenses WHERE expense_date=%s"
        cursor.execute(query, (date,))
        expenses = cursor.fetchall()
        return expenses

def fetch_category_summary(start_date, end_date):
    logger.info(f"fetch_category_summary called with {start_date}, {end_date}")
    with get_db_cursor() as cursor:
        query = '''
            SELECT category, SUM(amount) AS total 
            FROM expenses
            WHERE expense_date
            BETWEEN %s and %s
            GROUP BY category
            ORDER BY total DESC
        '''
        
        cursor.execute(query, (start_date, end_date))
        expenses = cursor.fetchall()
        return expenses

def fetch_month_summary():
    with get_db_cursor() as cursor:
        query = '''
        SELECT 
        DATE_FORMAT(expense_date, '%Y-%m') AS date,
        SUM(amount) AS total
        FROM expenses
        GROUP BY date
        ORDER BY date
        '''
        cursor.execute(query)
        expenses = cursor.fetchall()
        return expenses

# Update functions
def update_expenses(date, id, amount, category, notes):
    logger.info(f"update_expenses called with {date}, {id}")
    with get_db_cursor(commit=True) as cursor:
        query = '''UPDATE expenses
                    SET 
                    amount = %s, 
                    category = %s, 
                    notes = %s
                    WHERE id = %s And expense_date = %s
                    '''
        cursor.execute(query, (amount, category, notes, id, date))

# Delete functions


if __name__ == "__main__":
    # create_expense(date="2025-04-01", amount=50, category="Food", notes="BurgerKing")
    # print(fetch_expenses("2025-01-01"))
    print(fetch_month_summary())
