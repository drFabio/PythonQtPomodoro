import sys
import os
from unittest.mock import MagicMock, patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from IconCycler import IconCycler
from State import State, TimeInfo

@pytest.fixture
def mock_state():
    state = MagicMock(spec=State)
    # Mock events
    state.pause_event = MagicMock()
    state.resume_event = MagicMock()
    state.stop_event = MagicMock()
    state.start_event = MagicMock()
    state.tick_event = MagicMock()
    state.cycle_ended_event = MagicMock()
    
    # Mock current_interval
    state.current_interval = MagicMock()
    state.current_interval.name = "Work"
    state.cycles_count = 0
    state.interval_index = 0
    return state

@patch('IconCycler.QTimer')
def test_initialization(mock_qtimer_cls, mock_state):
    cycler = IconCycler(mock_state)
    
    # Check if events are connected
    mock_state.pause_event.connect.assert_called_with(cycler._on_pause)
    mock_state.resume_event.connect.assert_called_with(cycler._on_resume)
    mock_state.stop_event.connect.assert_called_with(cycler._on_stop)
    mock_state.start_event.connect.assert_called_with(cycler._on_start)
    
    # Check if timer is created
    mock_qtimer_cls.assert_called_once()

@patch('IconCycler.QTimer')
def test_start(mock_qtimer_cls, mock_state):
    cycler = IconCycler(mock_state)
    mock_timer = cycler.timer
    
    cycler.start()
    
    mock_timer.start.assert_called_with(1000)

@patch('IconCycler.QTimer')
def test_pause_resume_stop(mock_qtimer_cls, mock_state):
    cycler = IconCycler(mock_state)
    mock_timer = cycler.timer
    
    # Pause
    cycler._on_pause()
    mock_timer.stop.assert_called()
    
    # Resume
    mock_timer.reset_mock()
    cycler._on_resume()
    mock_timer.start.assert_called_with(1000)
    
    # Stop
    mock_timer.reset_mock()
    cycler._on_stop()
    mock_timer.stop.assert_called()

@patch('IconCycler.QTimer')
def test_tick_remaining(mock_qtimer_cls, mock_state):
    cycler = IconCycler(mock_state)
    
    # Setup state to have remaining time
    info = TimeInfo(ellapsed=10, remaining=5, total=15, percentage=0.66)
    mock_state.getTime.return_value = info
    
    # Call private tick method
    cycler._IconCycler__tick()
    
    mock_state.tick_event.emit.assert_called()
    mock_state.next_cycle.assert_not_called()

@patch('IconCycler.QTimer')
def test_tick_finished(mock_qtimer_cls, mock_state):
    cycler = IconCycler(mock_state)
    mock_timer = cycler.timer
    
    # Setup state to have 0 remaining time
    info = TimeInfo(ellapsed=15, remaining=0, total=15, percentage=1.0)
    mock_state.getTime.return_value = info
    
    # Call private tick method
    cycler._IconCycler__tick()
    
    mock_state.tick_event.emit.assert_called()
    mock_state.next_cycle.assert_called()
    
    # _next_cycle calls _on_stop, so timer should stop
    mock_timer.stop.assert_called()
