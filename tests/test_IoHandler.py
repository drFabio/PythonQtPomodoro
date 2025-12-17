import sys
import os
from unittest.mock import MagicMock
import pytest
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import QCoreApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from IoHandler import IoHandler
from State import State

# Create QCoreApplication to handle Qt event loop if necessary, 
# though QSqlDatabase might work without it, it's safer to have one singleton.
# We'll use a fixture.

@pytest.fixture(scope="session")
def qapp():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    yield app

@pytest.fixture
def mock_state():
    state = MagicMock(spec=State)
    state.cycle_ended_event = MagicMock()
    return state

@pytest.fixture
def db_connection():
    # Setup in-memory DB
    connection_name = "test_connection"
    if QSqlDatabase.contains(connection_name):
        QSqlDatabase.removeDatabase(connection_name)
    
    # Clean up any existing connection
    yield connection_name
    
    if QSqlDatabase.contains(connection_name):
        QSqlDatabase.removeDatabase(connection_name)

def test_initialization_and_schema(qapp, mock_state, db_connection):
    # Use :memory: for in-memory database
    handler = IoHandler(mock_state, db_path=":memory:", connection_name=db_connection)
    
    # Initialize schema explicitly
    assert handler._ensure_schema()
    
    # Check if connected
    db = QSqlDatabase.database(db_connection)
    assert db.isOpen()
    
    # Check if table exists
    assert "pomodoro_cycles" in db.tables()

def test_save_cycle(qapp, mock_state, db_connection):
    handler = IoHandler(mock_state, db_path=":memory:", connection_name=db_connection)
    
    cycle_info = {
        "name": "Work",
        "end": "2023-10-27T10:30:00",
        "start": "2023-10-27T10:00:00",
        "uuid": "test-uuid-123",
        "cycle_count": 1
    }
    
    handler._on_cycle_end(cycle_info)
    
    # Verify data in DB
    db = QSqlDatabase.database(db_connection)
    query = QSqlQuery(db)
    query.exec("SELECT * FROM pomodoro_cycles")
    
    assert query.next()
    assert query.value("interval_label") == "Work"
    assert query.value("uuid") == "test-uuid-123"
    assert query.value("cycle_count") == 1
    
    # Check conversions (though we passed strings, they should be stored)
    assert query.value("start_time") == "2023-10-27T10:00:00"

def test_ensure_connection_reconnect(qapp, mock_state, db_connection):
    handler = IoHandler(mock_state, db_path=":memory:", connection_name=db_connection)
    
    # Close connection manually
    db = QSqlDatabase.database(db_connection)
    db.close()
    
    # Try to save, should reconnect
    success = handler.save_cycle("start", "end", "test")
    assert success
    
    # Refresh db object
    db = QSqlDatabase.database(db_connection)
    assert db.isOpen()
