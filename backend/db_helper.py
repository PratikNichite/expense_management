from contextlib import contextmanager
import mysql.connector


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
        cursor.commit()
    
    cursor.close()
    connection.close()


# Create functions

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
    print(fetch_expenses("2024-08-01"))
