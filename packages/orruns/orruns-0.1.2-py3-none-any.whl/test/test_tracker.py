import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import json
import pytest
from pathlib import Path
from orruns.tracker import ExperimentTracker
from orruns import ExperimentTracker
from orruns.core.config import Config
import time

@pytest.fixture
def temp_dir():
    """Create temporary directory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def tracker(temp_dir):
    """Create experiment tracker instance"""
    return ExperimentTracker("test_experiment", base_dir=temp_dir)

def test_init(tracker, temp_dir):
    """Test initialization"""
    assert tracker.experiment_name == "test_experiment"
    assert tracker.base_dir == Path(temp_dir)
    assert tracker.run_dir.exists()
    assert tracker.params_dir.exists()
    assert tracker.metrics_dir.exists()
    assert tracker.artifacts_dir.exists()

def test_log_params(tracker):
    """Test parameter logging, including nested dictionaries"""
    # Test basic parameters
    params = {
        "learning_rate": 0.001,
        "batch_size": 32
    }
    tracker.log_params(params)
    
    # Verify basic parameters
    saved_params = tracker.get_params()
    assert saved_params == params
    
    # Test nested dictionaries
    nested_params = {
        "optimizer": {
            "name": "adam",
            "settings": {
                "beta1": 0.9,
                "beta2": 0.999
            }
        },
        "scheduler": {
            "name": "cosine",
            "settings": {
                "T_max": 100,
                "eta_min": 1e-6
            }
        }
    }
    tracker.log_params(nested_params)
    
    # Verify nested parameters
    saved_params = tracker.get_params()
    assert saved_params["optimizer"]["name"] == "adam"
    assert saved_params["optimizer"]["settings"]["beta1"] == 0.9
    assert saved_params["scheduler"]["settings"]["T_max"] == 100
    
    # Test using prefix
    prefixed_params = {
        "weight_decay": 0.01,
        "momentum": 0.9
    }
    tracker.log_params(prefixed_params, prefix="optimizer.settings")
    
    # Verify prefixed parameters
    saved_params = tracker.get_params()
    assert saved_params["optimizer"]["settings"]["weight_decay"] == 0.01
    assert saved_params["optimizer"]["settings"]["momentum"] == 0.9
    
    # Verify file saving
    params_file = tracker.params_dir / "params.json"
    assert params_file.exists()
    
    # Verify file content
    with open(params_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data["optimizer"]["settings"]["weight_decay"] == 0.01

def test_log_metrics(tracker):
    """Test metric logging, including nested metrics"""
    # Test single record
    metrics = {
        "loss": 0.5,
        "accuracy": 0.95
    }
    tracker.log_metrics(metrics)
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["loss"] == 0.5
    assert saved_metrics["accuracy"] == 0.95
    
    # Test nested metrics
    nested_metrics = {
        "train": {
            "loss": 0.4,
            "metrics": {
                "accuracy": 0.96,
                "f1_score": 0.94
            }
        },
        "val": {
            "loss": 0.45,
            "metrics": {
                "accuracy": 0.93,
                "f1_score": 0.92
            }
        }
    }
    tracker.log_metrics(nested_metrics)
    
    # Verify nested metrics
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["train"]["loss"] == 0.4
    assert saved_metrics["train"]["metrics"]["accuracy"] == 0.96
    assert saved_metrics["val"]["metrics"]["f1_score"] == 0.92
    
    # Test recording with steps
    tracker.log_metrics({"train": {"loss": 0.3}}, step=1)
    tracker.log_metrics({"train": {"loss": 0.2}}, step=2)
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["train"]["loss"]["steps"] == [1, 2]
    assert saved_metrics["train"]["loss"]["values"] == [0.3, 0.2]
    
    # Test nested metrics with prefix
    tracker.log_metrics(
        {"accuracy": 0.97, "f1_score": 0.95},
        prefix="train.metrics",
        step=3
    )
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["train"]["metrics"]["accuracy"]["steps"] == [3]
    assert saved_metrics["train"]["metrics"]["accuracy"]["values"] == [0.97]

def test_invalid_metrics(tracker):
    """Test invalid metric value handling"""
    # Test non-numeric type
    with pytest.raises(ValueError):
        tracker.log_metrics({"invalid": "not a number"})
    
    # Test non-numeric type in nested dictionary
    with pytest.raises(ValueError):
        tracker.log_metrics({
            "train": {
                "metrics": {
                    "invalid": ["not", "a", "number"]
                }
            }
        })
    
    # Test non-numeric type with prefix
    with pytest.raises(ValueError):
        tracker.log_metrics(
            {"invalid": {"nested": "not a number"}},
            prefix="train"
        )

def test_deep_update(tracker):
    """Test deep update functionality"""
    # Initial parameters
    initial_params = {
        "model": {
            "layers": [64, 32],
            "activation": "relu"
        }
    }
    tracker.log_params(initial_params)
    
    # Update partial parameters
    update_params = {
        "model": {
            "layers": [128, 64, 32],
            "dropout": 0.5
        }
    }
    tracker.log_params(update_params)
    
    # Verify update results
    saved_params = tracker.get_params()
    assert saved_params["model"]["layers"] == [128, 64, 32]
    assert saved_params["model"]["activation"] == "relu"
    assert saved_params["model"]["dropout"] == 0.5

def test_log_artifact(tracker):
    """Test file artifact logging"""
    # Test CSV file
    data = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", data, artifact_type="data")
    
    # Verify CSV file
    csv_path = tracker.data_dir / "data.csv"
    assert csv_path.exists(), f"CSV file not found at {csv_path}"
    with open(csv_path, 'r', encoding='utf-8') as f:
        assert f.read() == data
    
    # Test image file
    image_data = b"fake_image_data"
    tracker.log_artifact("plot.png", image_data, artifact_type="figure")
    
    # Verify image file
    png_path = tracker.figures_dir / "plot.png"
    assert png_path.exists(), f"PNG file not found at {png_path}"
    with open(png_path, 'rb') as f:
        assert f.read() == image_data
    
    # Verify file list
    artifacts = tracker.get_artifacts()  # Use instance method
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]

@pytest.mark.parametrize("experiment_name,expected_runs", [
    ("test_exp_1", 2),
    ("test_exp_2", 1),
])
def test_list_experiments(temp_dir, experiment_name, expected_runs):
    """Test experiment listing"""
    # Create test experiments
    for _ in range(expected_runs):
        tracker = ExperimentTracker(experiment_name, base_dir=temp_dir)
        tracker.log_params({"test": True})
    
    experiments = ExperimentTracker.list_experiments(base_dir=temp_dir)
    exp = next(e for e in experiments if e["name"] == experiment_name)
    assert len(exp["runs"]) == expected_runs

def test_query_experiments(temp_dir):
    """Test experiment querying"""
    # Create test data
    tracker1 = ExperimentTracker("exp1", base_dir=temp_dir)
    tracker1.log_params({"learning_rate": 0.1})
    tracker1.log_metrics({"accuracy": 0.9})
    
    tracker2 = ExperimentTracker("exp2", base_dir=temp_dir)
    tracker2.log_params({"learning_rate": 0.01})
    tracker2.log_metrics({"accuracy": 0.95})
    
    # Wait for file writing to complete
    time.sleep(0.1)
    
    # Test parameter filtering
    results = ExperimentTracker.query_experiments(
        base_dir=temp_dir,
        parameter_filters={"learning_rate__gt": 0.05}
    )
    assert len(results) == 1
    assert results[0]["parameters"]["learning_rate"] == 0.1

def test_get_experiment(temp_dir):
    """Test getting experiment details"""
    # Create test experiment
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    tracker.log_params({"param1": 1})
    tracker.log_metrics({"metric1": 0.5})
    
    # Get experiment details
    exp_info = ExperimentTracker.get_experiment("test_exp", base_dir=temp_dir)
    assert exp_info["name"] == "test_exp"
    assert exp_info["parameters"] == {"param1": 1}
    assert exp_info["metrics"] == {"metric1": 0.5}

def test_get_artifacts(temp_dir):
    """Test getting file artifacts"""
    # Create test experiment and files
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    
    # Create test files
    csv_content = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", csv_content, artifact_type="data")
    
    png_content = b"fake_image_data"
    tracker.log_artifact("plot.png", png_content, artifact_type="figure")
    
    # Wait for file writing to complete
    time.sleep(0.1)
    
    # Get file list
    artifacts = tracker.get_artifacts()  # Use instance method
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]
    
    # Can also use class method
    artifacts = ExperimentTracker.list_artifacts(
        "test_exp",
        tracker.run_id,
        base_dir=temp_dir
    )
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]
    
    # Verify file contents
    data_path = tracker.data_dir / "data.csv"
    with open(data_path, 'r', encoding='utf-8') as f:
        assert f.read() == csv_content
        
    figure_path = tracker.figures_dir / "plot.png"
    with open(figure_path, 'rb') as f:
        assert f.read() == png_content

def test_error_handling(temp_dir):
    """Test error handling"""
    # Test non-existent experiment
    with pytest.raises(FileNotFoundError):
        ExperimentTracker.get_experiment("nonexistent", base_dir=temp_dir)
    
    # Test invalid metric format
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    with pytest.raises(ValueError):
        tracker.log_metrics({"metric": "invalid"})  # Should be a number