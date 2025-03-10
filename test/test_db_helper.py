import pytest
from backend import db_helper

def test_db_connection():
    try:
        with db_helper.get_db_cursor() as cursor:
            assert cursor is not None
            assert cursor._connection.is_connected()
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")