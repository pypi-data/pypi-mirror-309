import pytest
import tempfile
import shutil
from pathlib import Path
import time
import json
from datetime import datetime
import pandas as pd

from orruns.api.experiment import ExperimentAPI
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def temp_dir():
    """Create temporary directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def api(temp_dir):
    """Create API instance"""
    config = Config.get_instance()
    config.set_data_dir(temp_dir)
    return ExperimentAPI()

@pytest.fixture
def sample_experiment(api):
    """Create sample experiment"""
    tracker = ExperimentTracker("test_exp", base_dir=api.config.get_data_dir())
    
    # Record parameters
    tracker.log_params({
        "learning_rate": 0.01,
        "batch_size": 32,
        "model": {
            "type": "cnn",
            "layers": [64, 32]
        }
    })
    
    # Record metrics
    tracker.log_metrics({
        "accuracy": 0.85,
        "loss": 0.15,
        "validation": {
            "accuracy": 0.83,
            "loss": 0.17
        }
    })
    
    # Record CSV file
    csv_content = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", csv_content, artifact_type="data")
    
    # Record image file
    tracker.log_artifact("plot.png", b"fake_image_data", artifact_type="figure")
    
    # Wait for file writing to complete
    time.sleep(0.1)
    
    return tracker

def test_list_experiments(api, sample_experiment):
    """Test listing experiments"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    experiments = api.list_experiments()
    assert len(experiments) > 0
    
    # Verify experiment information
    exp = next(e for e in experiments if e["name"] == "test_exp")
    assert len(exp["runs"]) == 1
    assert "params" in exp["runs"][0]
    assert "metrics" in exp["runs"][0]

def test_list_experiments_with_pattern(api, sample_experiment):
    """Test listing experiments with pattern matching"""
    # Create additional experiments
    tracker2 = ExperimentTracker("test_exp_2", base_dir=api.config.get_data_dir())
    tracker2.log_params({"test": True})
    tracker2._save_experiment_info()  # Ensure saving
    
    tracker3 = ExperimentTracker("other_exp", base_dir=api.config.get_data_dir())
    tracker3.log_params({"test": True})
    tracker3._save_experiment_info()  # Ensure saving
    
    # Increase wait time
    time.sleep(0.2)  # Increase wait time
    
    # Use pattern matching
    experiments = api.list_experiments(pattern="test_*")
    names = [exp["name"] for exp in experiments]
    assert "test_exp" in names
    assert "test_exp_2" in names
    assert "other_exp" not in names

def test_get_experiment(api, sample_experiment):
    """Test getting experiment details"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    exp_info = api.get_experiment("test_exp")
    
    # Verify basic information
    assert exp_info["name"] == "test_exp"
    assert len(exp_info["runs"]) == 1
    
    # Verify parameters and metrics
    latest_run = exp_info["latest_run"]
    assert latest_run["params"]["learning_rate"] == 0.01
    assert latest_run["metrics"]["accuracy"] == 0.85

def test_get_run(api, sample_experiment):
    """Test getting run details"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    run_info = api.get_run("test_exp", sample_experiment.run_id)
    
    # Verify run information
    assert run_info["run"]["run_id"] == sample_experiment.run_id
    assert run_info["parameters"]["learning_rate"] == 0.01
    assert run_info["metrics"]["accuracy"] == 0.85

def test_query_experiments(api, sample_experiment):
    """Test querying experiments"""
    # Create a new experiment and record explicit test data
    tracker = ExperimentTracker("test_exp_query", base_dir=api.config.get_data_dir())
    
    # Record parameters and save
    tracker.log_params({
        "learning_rate": 0.01,
        "batch_size": 32
    })
    tracker._save_experiment_info()  # Ensure saving
    
    # Record metrics and save
    tracker.log_metrics({
        "accuracy": 0.85,
        "loss": 0.15
    })
    tracker._save_experiment_info()  # Save again to update metrics
    
    # Increase wait time
    time.sleep(0.2)
    
    # Parameter filtering
    results = api.query_experiments(
        parameter_filters={
            "learning_rate__eq": 0.01  # Use __eq operator for exact matching
        }
    )
    assert len(results) > 0
    assert results[0]["parameters"]["learning_rate"] == 0.01

    # Metric filtering
    results = api.query_experiments(
        metric_filters={
            "accuracy__gte": 0.8  # Use same format as parameter filters
        }
    )
    assert len(results) > 0
    assert results[0]["metrics"]["accuracy"] >= 0.8

def test_get_artifacts(api, sample_experiment):
    """Test getting artifact list"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    artifacts = api.get_artifacts("test_exp", sample_experiment.run_id)
    
    # Verify file list
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]

def test_get_artifact_path(api, sample_experiment):
    """Test getting artifact path"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    # Get data file path
    data_path = api.get_artifact_path(
        "test_exp",
        sample_experiment.run_id,
        "data.csv",
        artifact_type="data"
    )
    assert data_path.exists()
    with open(data_path, 'r', encoding='utf-8') as f:
        assert f.read() == "col1,col2\n1,2\n3,4"
    
    # Get image file path
    figure_path = api.get_artifact_path(
        "test_exp",
        sample_experiment.run_id,
        "plot.png",
        artifact_type="figure"
    )
    assert figure_path.exists()
    with open(figure_path, 'rb') as f:
        assert f.read() == b"fake_image_data"

def test_load_artifact(api, sample_experiment):
    """Test loading artifacts"""
    # Wait for file writing to complete
    time.sleep(0.1)
    
    # Load CSV file
    data = api.load_artifact(
        "test_exp",
        sample_experiment.run_id,
        "data.csv",
        artifact_type="data"
    )
    # Check if it's a DataFrame
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["col1", "col2"]

def test_error_handling(api):
    """Test error handling"""
    # Test non-existent experiment
    with pytest.raises(FileNotFoundError):
        api.get_experiment("nonexistent")

    # Test non-existent run
    with pytest.raises(FileNotFoundError):
        api.get_run("nonexistent", "nonexistent_run")

    # Test non-existent artifact
    with pytest.raises(FileNotFoundError):
        api.get_artifact_path(
            "nonexistent",
            "nonexistent_run",
            "nonexistent.txt"
        )

    # Test invalid query conditions
    with pytest.raises(ValueError):
        api.query_experiments(
            parameter_filters={"learning_rate__invalid": 0.1}
        )