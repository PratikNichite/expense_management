from backend import db_helper

def test_database_connection():
    with db_helper.get_db_cursor() as cursor:
        assert cursor is not None
        assert cursor._connection.is_connected()

def test_fetch_expenses_by_date():
    date = "2025-03-10"
    expenses = db_helper.fetch_expenses(date)
    assert isinstance(expenses, list)
    for expense in expenses:
        assert "expense_date" in expense
        assert expense["expense_date"] == date

def test_create_expense():
    date = "1600-01-01"
    amount = 100
    category = "Entertainment"
    notes = "Movie"
    
    db_helper.create_expense(date, amount, category, notes)
    
    expenses = db_helper.fetch_expenses(date)
    assert any(exp["amount"] == amount and exp["category"] == category and exp["notes"] == notes for exp in expenses)