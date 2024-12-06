import pytest
from click.testing import CliRunner
import tempfile
import shutil
from pathlib import Path
import json
import time
from datetime import datetime

from orruns.cli.commands import cli
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def runner():
    """Create CLI test runner"""
    return CliRunner()

@pytest.fixture
def temp_dir():
    """Create temporary directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def config(temp_dir):
    """Set up test configuration"""
    config = Config.get_instance()
    old_dir = config.get_data_dir()  # Save original directory
    config.set_data_dir(temp_dir)
    yield config
    config.set_data_dir(old_dir)  # Restore original directory

@pytest.fixture
def sample_experiment(temp_dir):
    """Create sample experiment data"""
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    
    # Record parameters and metrics
    params = {
        "param1": 1,
        "param2": "test"
    }
    metrics = {
        "metric1": 0.5,
        "metric2": 100
    }
    
    # Use tracker methods to record parameters and metrics
    tracker.log_params(params)
    tracker.log_metrics(metrics)
    
    # Wait for file writing to complete
    time.sleep(0.5)
    
    return tracker

def test_config_commands(runner, temp_dir):
    """Test configuration related commands"""
    # Test setting data directory
    result = runner.invoke(cli, ['config', 'data-dir', temp_dir])
    assert result.exit_code == 0
    assert f"Data directory set to: {temp_dir}" in result.output
    
    # Test showing configuration
    result = runner.invoke(cli, ['config', 'show'])
    assert result.exit_code == 0
    assert temp_dir in result.output
    assert "Version:" in result.output

def test_list_command(runner, config, sample_experiment):
    """Test list experiments command"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    # Test brief list
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    
    # Test detailed list
    result = runner.invoke(cli, ['list', '--detailed'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    # Check if parameters are in output, using more flexible checks
    output = result.output.replace(" ", "")
    assert any(x in output for x in [
        "'param1':1",
        "param1:1",
        '"param1":1',
        "{'param1':1"
    ])
    
    # Test pattern matching
    result = runner.invoke(cli, ['list', '--pattern', 'test_*'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    
    # Test non-existent pattern
    result = runner.invoke(cli, ['list', '--pattern', 'nonexistent_*'])
    assert result.exit_code == 0
    assert "No experiments found matching pattern 'nonexistent_*'" in result.output

def test_info_command(runner, config, sample_experiment):
    """Test view experiment info command"""
    time.sleep(0.1)
    
    # Test viewing experiment overview
    result = runner.invoke(cli, ['info', 'test_exp'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    assert "Total Runs" in result.output
    
    # Check parameters and metrics, using more flexible checks
    output = result.output.replace(" ", "")
    assert any(x in output for x in [
        "'param1':1",
        "param1:1",
        '"param1":1',
        "{'param1':1"
    ])
    
    # Test viewing specific run
    result = runner.invoke(cli, ['info', 'test_exp', '--run-id', sample_experiment.run_id])
    assert result.exit_code == 0
    assert sample_experiment.run_id in result.output
    output = result.output.replace(" ", "")
    assert "param1:1" in output

def test_delete_command(runner, config, sample_experiment):
    """Test delete command"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    # Test delete confirmation
    result = runner.invoke(cli, ['delete', 'test_exp'], input='n\n')
    assert result.exit_code == 0
    assert "Operation cancelled" in result.output
    
    # Test force delete
    result = runner.invoke(cli, ['delete', 'test_exp', '--force'])
    assert result.exit_code == 0
    assert "Deleted experiment" in result.output
    
    # Verify experiment was deleted
    result = runner.invoke(cli, ['list'])
    assert "test_exp" not in result.output
    
    # Test deleting non-existent experiment
    result = runner.invoke(cli, ['delete', 'nonexistent', '--force'])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()

def test_error_handling(runner):
    """Test error handling"""
    config = Config.get_instance()
    old_dir = config.get_data_dir()  # Save original directory
    
    try:
        # Use non-existent directory
        nonexistent_dir = str(Path(tempfile.mkdtemp()) / "nonexistent")
        shutil.rmtree(nonexistent_dir, ignore_errors=True)  # Ensure directory doesn't exist
        config.set_data_dir(nonexistent_dir)
        
        result = runner.invoke(cli, ['list'])
        assert "No experiments found" in result.output
        
    finally:
        # Restore original directory
        config.set_data_dir(old_dir)

def test_format_helpers(runner, config, sample_experiment):
    """Test formatting helper functions"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    result = runner.invoke(cli, ['info', 'test_exp'])
    assert result.exit_code == 0
    
    # Verify time formatting
    assert "20" in result.output  # Year
    assert ":" in result.output   # Time separator
    
    # Verify metric formatting, using more flexible checks
    output = result.output.replace(" ", "")
    assert any(x in output for x in ["metric1:0.5", "metric1=0.5"])
    assert any(x in output for x in ["metric2:100", "metric2=100"])