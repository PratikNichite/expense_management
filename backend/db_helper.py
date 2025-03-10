from contextlib import contextmanager
import mysql.connector

# main database cursor
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pralinn@123",
        database="expense_manager"
    )
    
    if connection.is_connected():
        print("connected!")
    else:
        print("failed to connect!")
    
    cursor = connection.cursor(dictionary=True)
    yield cursor
    
    if commit:
        connection.commit()
    
    cursor.close()
    connection.close()
    print("disconnected!")


# fetch code
def fetch_all():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        return expenses
    
def fetch_expenses_for_date(date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date=%s", (date,))
        expenses = cursor.fetchall()
        return expenses

def fetch_expense_summary(start_date, end_date):
    with get_db_cursor() as cursor:
        query = '''SELECT category, SUM(amount) as total 
                    FROM expenses 
                    WHERE expense_date 
                    BETWEEN %s AND %s
                    GROUP BY category;'''
        cursor.execute(query, (start_date, end_date))
        expenses = cursor.fetchall()
        return expenses

# insert code
def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        query = "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (expense_date, amount, category, notes))

# delete code
def delete_expense(expense_date):
    with get_db_cursor(commit=True) as cursor:
        query = "DELETE FROM expenses WHERE expense_date=%s"
        cursor.execute(query, (expense_date,))


if __name__ == "__main__":
    print(fetch_all())
    print("*"*20)
    
    insert_expense("2025-01-01", 50, "food", "burgerking")
    print("*"*20)
    
    print(fetch_all())
    print("*"*20)
    
    delete_expense("2025-01-01")
    print("*"*20)
    
    print(fetch_all())
    
    print("*"*20)
    print(fetch_expense_summary("2024-08-01", "2024-08-03"))