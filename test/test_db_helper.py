import pytest
from backend import db_helper

def test_db_connection():
    try:
        with db_helper.get_db_cursor() as cursor:
            assert cursor is not None
            assert cursor._connection.is_connected()
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
        

def test_fetch_expenses():
    try:
        assert len(db_helper.fetch_expenses("2024-08-01")) >= 1
    except Exception as e:
        pytest.fail(f"Fetch error: {e}")