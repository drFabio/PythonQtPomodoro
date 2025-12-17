import sys
import os
import time
from unittest.mock import MagicMock, patch
import pytest
from PyQt6.QtGui import QColor

# Add src to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from State import State, Status
from TimeSection import TimeSection

# Mock time to control flow
@pytest.fixture
def mock_time():
    with patch('time.time') as mock:
        yield mock

@pytest.fixture
def sample_intervals():
    return [
        TimeSection(name="Work", duration=1500, color=QColor("red")),
        TimeSection(name="Break", duration=300, color=QColor("green"))
    ]

def test_initial_state(sample_intervals):
    state = State(sample_intervals)
    assert state.status == Status.STOPPED
    assert state.interval_index == -1
    assert state.current_interval is None

def test_start(sample_intervals, mock_time):
    mock_time.return_value = 1000
    state = State(sample_intervals)
    
    # Mock signal
    state.start_event = MagicMock()
    
    interval = state.start()
    
    assert state.status == Status.RUNNING
    assert state.start_time == 1000
    assert state.current_interval == sample_intervals[0]
    assert interval == sample_intervals[0]
    assert state.interval_index == 0
    state.start_event.emit.assert_called_once()

def test_pause(sample_intervals, mock_time):
    mock_time.return_value = 1000
    state = State(sample_intervals)
    state.start()
    
    # Advance time by 100 seconds
    mock_time.return_value = 1100
    
    state.pause_event = MagicMock()
    state.pause()
    
    assert state.status == Status.PAUSED
    assert state.ellapsed_time == 100
    state.pause_event.emit.assert_called_once()

def test_resume(sample_intervals, mock_time):
    mock_time.return_value = 1000
    state = State(sample_intervals)
    state.start()
    
    # Pause at 100s
    mock_time.return_value = 1100
    state.pause()
    
    # Resume at 1200s
    mock_time.return_value = 1200
    state.resume_event = MagicMock()
    state.resume()
    
    assert state.status == Status.RUNNING
    assert state.start_time == 1200
    state.resume_event.emit.assert_called_once()
    
    # Check get_time after resume
    # Elapsed should be previous elapsed (100) + (1250 - 1200) = 150
    mock_time.return_value = 1250
    info = state.getTime()
    assert info.ellapsed == 150
    assert info.total == 1500 # Work duration
    assert info.remaining == 1350
    assert info.percentage == 0.9

def test_stop(sample_intervals, mock_time):
    state = State(sample_intervals)
    state.start()
    
    state.stop_event = MagicMock()
    state.stop()
    
    assert state.status == Status.STOPPED
    assert state.current_interval is None
    state.stop_event.emit.assert_called_once()

def test_next_cycle(sample_intervals, mock_time):
    mock_time.return_value = 1000
    state = State(sample_intervals)
    state.start()
    
    state.cycle_ended_event = MagicMock()
    # We mock start_event because start() is called inside next_cycle
    state.start_event = MagicMock() 
    
    # Move to next cycle
    mock_time.return_value = 2500
    state.next_cycle()
    
    # Should be "Break" now
    assert state.current_interval.name == "Break"
    assert state.interval_index == 1
    state.cycle_ended_event.emit.assert_called_once()
    
    # Check payload of cycle_ended signal
    args, _ = state.cycle_ended_event.emit.call_args
    payload = args[0]
    assert payload['name'] == "Work" # The one that ended
    assert payload['end'] == 2500

def test_cycle_loop(sample_intervals, mock_time):
    state = State(sample_intervals)
    state.start() # Index 0
    state.next_cycle() # Index 1
    state.next_cycle() # Index 0 again
    
    assert state.interval_index == 0
    assert state.current_interval.name == "Work"
    assert state.cycles_count == 1
