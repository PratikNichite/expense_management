from contextlib import contextmanager
import mysql.connector

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Root@123",
        database = "expense_manager"
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

if __name__ == "__main__":
    with get_db_cursor() as cursor:
        print("Hello world")