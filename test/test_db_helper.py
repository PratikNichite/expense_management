from backend import db_helper

def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_all()
    
    assert len(expenses) > 1