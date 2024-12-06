import json
import os
import re
import random
import shutil
from datetime import datetime, timedelta
from typing import Union, Dict, List, Any, Optional, Tuple
import pathlib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import os
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .core.config import Config

class ExperimentTracker:
    """
    ORruns's core tracking class, used to manage the parameters and metrics of operations research experiments.
    
    Args:
        experiment_name: Name of the experiment
        base_dir: Base directory for storing experiment data
    """
    def __init__(self, experiment_name: str, base_dir: str = "./orruns_experiments"):
        self.experiment_name = experiment_name
        self.config = Config.get_instance()
        self.base_dir = pathlib.Path(base_dir).resolve()
        
        # Generate a unique run ID
        # 生成唯一的运行ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        random_suffix = str(random.randint(1000, 9999))
        self.run_id = f"{timestamp}_{random_suffix}"
        
        # Create the main run directory
        # 创建主要的运行目录
        self.run_dir = self.base_dir / experiment_name / self.run_id
        
        # Create directories for parameters, metrics, and artifacts
        # 创建参数、指标和工件的目录
        self.params_dir = self.run_dir / "params"
        self.metrics_dir = self.run_dir / "metrics"
        self.artifacts_dir = self.run_dir / "artifacts"
        self.figures_dir = self.artifacts_dir / "figures"
        self.data_dir = self.artifacts_dir / "data"
        
        # Create all necessary directories
        # 创建所有必要的目录
        for directory in [self.params_dir, self.metrics_dir, 
                         self.figures_dir, self.data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        self._params = {}
        self._metrics = {}

    def _deep_update(self, source: Dict, updates: Dict) -> Dict:
        """Deeply update nested dictionaries
        深度更新嵌套字典
        """
        for key, value in updates.items():
            if key in source and isinstance(source[key], dict) and isinstance(value, dict):
                self._deep_update(source[key], value)
            else:
                source[key] = value
        return source
        
    def _process_nested_input(self, data: Dict, prefix: Optional[str] = None) -> Dict:
        """Process nested input data with an optional prefix
        处理带有可选前缀的嵌套输入数据
        """
        if prefix:
            nested_data = {}
            current = nested_data
            parts = prefix.split('.')
            for part in parts[:-1]:
                current[part] = {}
                current = current[part]
            current[parts[-1]] = data
            return nested_data
        return data

    def _save_experiment_info(self):
        """Save experiment information to summary.json
        将实验信息保存到summary.json
        """
        summary = {
            "name": self.experiment_name,
            "run_id": self.run_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parameters": self._params,
            "metrics": self._metrics,
            "status": "completed"  # Add status field
            # 添加状态字段
        }
        
        # Ensure the directory exists
        # 确保目录存在
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as dictionary format
        # 以字典格式保存
        summary_path = self.run_dir / "summary.json"
        with open(summary_path, "w", encoding='utf-8') as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

    def log_params(self, params: Dict[str, Any], prefix: Optional[str] = None) -> None:
        """Log parameters to the params directory
        将参数记录到params目录
        """
        params = self._process_nested_input(params, prefix)
        self._params = self._deep_update(self._params, params)
        
        with open(self.params_dir / "params.json", "w", encoding='utf-8') as f:
            json.dump(self._params, f, indent=4, ensure_ascii=False)
        
        # Save experiment information
        # 保存实验信息
        self._save_experiment_info()

    def _validate_metrics(self, metrics: Dict[str, Any], path: str = "") -> None:
        """Recursively validate metric values
        递归验证指标值"""
        for key, value in metrics.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                self._validate_metrics(value, current_path)
            elif not isinstance(value, (float, int)):
                raise ValueError(
                    f"Invalid metric value for {current_path}: must be float or int"
                )

    def _get_current_metric(self, path: List[str]) -> Any:
        """Get the metric value for the current path
        获取当前路径的指标值"""
        current = self._metrics
        for p in path:
            if p not in current:
                return None
            current = current[p]
        return current

    def _process_metric_value(self, path: List[str], value: Union[float, int], step: Optional[int] = None) -> Dict:
        """Process a single metric value
        处理单个指标值"""
        if step is not None:
            current_metric = self._get_current_metric(path)
            if current_metric is None:
                return {"steps": [step], "values": [value]}
            elif isinstance(current_metric, dict) and "steps" in current_metric:
                return {
                    "steps": current_metric["steps"] + [step],
                    "values": current_metric["values"] + [value]
                }
            else:
                return {"steps": [step], "values": [value]}
        return value

    def _process_nested_metrics(self, metrics: Dict, current_path: List[str] = None, step: Optional[int] = None) -> Dict:
        """Recursively process nested metrics
        递归处理嵌套指标"""
        if current_path is None:
            current_path = []
            
        result = {}
        for key, value in metrics.items():
            path = current_path + [key]
            if isinstance(value, dict):
                result[key] = self._process_nested_metrics(value, path, step)
            else:
                result[key] = self._process_metric_value(path, value, step)
        return result

    def log_metrics(self, metrics: Dict[str, Union[float, int, dict]], 
                   prefix: Optional[str] = None, 
                   step: Optional[int] = None) -> None:
        """Log metrics to the metrics directory
        记录指标到metrics目录"""
        # Validate metric values
        # 验证指标值
        self._validate_metrics(metrics)
        
        # Process prefix
        # 处理前缀
        if prefix:
            parts = prefix.split('.')
            for part in reversed(parts):
                metrics = {part: metrics}
        
        # Process metric values
        # 处理指标值
        processed_metrics = self._process_nested_metrics(metrics, step=step)
        
        # Update stored metrics
        # 更新存储的指标
        self._metrics = self._deep_update(self._metrics, processed_metrics)
        
        # Save to file
        # 保存到文件
        with open(self.metrics_dir / "metrics.json", "w", encoding='utf-8') as f:
            json.dump(self._metrics, f, indent=4, ensure_ascii=False)
            
        # Save experiment information
        # 保存实验信息
        self._save_experiment_info()

    def log_artifact(self, filename: str, content: Union[str, bytes, Figure, pd.DataFrame], artifact_type: Optional[str] = None) -> None:
        """Log file artifact
        
        Args:
            filename: Name of the file
            content: Content of the file, can be a string, bytes, matplotlib figure, or pandas DataFrame
            artifact_type: Type of the file, optional values include "csv", "data", "figure", etc.
        """
        # Determine target directory based on file type and extension
        # 根据文件类型和扩展名确定目标目录
        file_ext = Path(filename).suffix.lower()
        
        if artifact_type in ["csv", "data"] or file_ext in [".csv", ".json", ".txt"]:
            target_dir = self.data_dir
        elif artifact_type in ["figure", "png", "jpg"] or file_ext in [".png", ".jpg", ".jpeg", ".svg"]:
            target_dir = self.figures_dir
        else:
            target_dir = self.artifacts_dir
        
        # Ensure the target directory exists
        # 确保目标目录存在
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / filename

        try:
            if isinstance(content, Figure):
                content.savefig(file_path)
                plt.close(content)
                
            elif isinstance(content, pd.DataFrame):
                content.to_csv(file_path, index=False)
                
            elif isinstance(content, dict):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
                    
            else:
                is_binary = isinstance(content, bytes) or file_ext in [".png", ".jpg", ".jpeg"]
                mode = 'wb' if is_binary else 'w'
                encoding = None if is_binary else 'utf-8'
                
                with open(file_path, mode, encoding=encoding) as f:
                    f.write(content)
                    f.flush()
                    os.fsync(f.fileno())
                        
        except Exception as e:
            raise IOError(f"Failed to write artifact {filename}: {e}")



    @classmethod
    def delete_experiment(cls, 
                         experiment_name: str, 
                         base_dir: str = "./orruns_experiments",
                         run_id: Optional[str] = None) -> None:
        """
        Delete the specified experiment or a specific run within the experiment

        Args:
            experiment_name: Name of the experiment to delete
            base_dir: Base directory where experiment data is stored 
            run_id: Optional run ID. If specified, only delete that run; if None, delete the entire experiment

        Raises:
            FileNotFoundError: When the specified experiment or run does not exist
        """
        base_path = pathlib.Path(base_dir)
        exp_path = base_path / experiment_name

        if not exp_path.exists():
            raise FileNotFoundError(f"Experiment '{experiment_name}' not found in {base_dir}")

        if run_id is not None:
            # 删除特定运行
            # Delete specific run
            run_path = exp_path / run_id
            if not run_path.exists():
                raise FileNotFoundError(f"Run '{run_id}' not found in experiment '{experiment_name}'")
            shutil.rmtree(run_path)
            # 如果实验目录为空，删除它
            # If the experiment directory is empty, delete it
            if not any(exp_path.iterdir()):
                exp_path.rmdir()
        else:
            # 删除整个实验
            # Delete the entire experiment
            shutil.rmtree(exp_path)

    @classmethod
    def delete_all_experiments(cls, base_dir: str = "./orruns_experiments") -> None:
        """
        Delete all experiment data

        Args:
            base_dir: Base directory where experiment data is stored
        """
        base_path = pathlib.Path(base_dir)
        if base_path.exists():
            shutil.rmtree(base_path)

    @classmethod
    def list_experiments(cls, base_dir: str = "./orruns_experiments") -> List[dict]:
        """
        List all experiments and their run information

        Args:
            base_dir: Base directory where experiment data is stored

        Returns:
            List[dict]: A list of dictionaries containing experiment information
        """
        base_path = pathlib.Path(base_dir)
        if not base_path.exists():
            return []

        experiments = []
        for exp_path in base_path.iterdir():
            if exp_path.is_dir():
                runs = []
                for run_path in exp_path.iterdir():
                    if run_path.is_dir():
                        # 尝试读取实验信息
                        # Try to read experiment information
                        try:
                            # 首先尝试读取 summary.json
                            # First try to read summary.json
                            summary_path = run_path / "summary.json"
                            if summary_path.exists():
                                with open(summary_path, 'r', encoding='utf-8') as f:
                                    run_info = json.load(f)
                                    runs.append({
                                        "run_id": run_path.name,
                                        "timestamp": run_path.name.split("_")[0],
                                        "params": run_info.get("parameters", {}),
                                        "metrics": run_info.get("metrics", {})
                                    })
                            else:
                                # 尝试分别读取参数和指标文件
                                # Try to read parameter and metric files separately
                                params = {}
                                metrics = {}
                                params_file = run_path / "params" / "params.json"
                                metrics_file = run_path / "metrics" / "metrics.json"
                                
                                if params_file.exists():
                                    with open(params_file, 'r', encoding='utf-8') as f:
                                        params = json.load(f)
                                if metrics_file.exists():
                                    with open(metrics_file, 'r', encoding='utf-8') as f:
                                        metrics = json.load(f)
                                        
                                runs.append({
                                    "run_id": run_path.name,
                                    "timestamp": run_path.name.split("_")[0],
                                    "params": params,
                                    "metrics": metrics
                                })
                                
                        except json.JSONDecodeError:
                            # 如果文件读取失败，添加一个基本的运行记录
                            # If file reading fails, add a basic run record
                            runs.append({
                                "run_id": run_path.name,
                                "timestamp": run_path.name.split("_")[0],
                                "params": {},
                                "metrics": {}
                            })

                if runs:  # 只添加有运行记录的实验
                    # Only add experiments with run records
                    experiments.append({
                        "name": exp_path.name,
                        "runs": sorted(runs, key=lambda x: x["timestamp"], reverse=True)
                    })

        return experiments
    
    @classmethod
    def query_experiments(cls, 
                         base_dir: str = "./orruns_experiments",
                         parameter_filters: Optional[Dict[str, Any]] = None,
                         metric_filters: Optional[List[Dict[str, Any]]] = None,
                         sort_by: Optional[str] = None,
                         sort_ascending: bool = True,
                         limit: Optional[int] = None) -> List[Dict]:
        """查询实验
        Query experiments"""
        def parse_filter_key(key: str) -> Tuple[str, str]:
            """解析过滤器键
            Parse filter key"""
            if "__" in key:
                field, op = key.split("__")
                return field, op
            return key, "eq"

        def match_value(value: Any, filter_value: Any, op: str) -> bool:
            """匹配值
            Match value"""
            if op == "eq":
                return value == filter_value
            elif op == "gt":
                return value > filter_value
            elif op == "lt":
                return value < filter_value
            elif op == "gte":
                return value >= filter_value
            elif op == "lte":
                return value <= filter_value
            return False

        def match_filters(exp: Dict, filters: Dict[str, Any], data_key: str) -> bool:
            """匹配过滤器
            Match filters"""
            if not filters:
                return True
                
            for key, filter_value in filters.items():
                field, op = parse_filter_key(key)
                exp_data = exp.get(data_key, {})
                if field not in exp_data:
                    return False
                if not match_value(exp_data[field], filter_value, op):
                    return False
            return True

        # 获取所有实验
        # Get all experiments
        experiments = []
        base_path = pathlib.Path(base_dir)
        if not base_path.exists():
            return []

        # 遍历所有实验目录
        # Traverse all experiment directories
        for exp_dir in base_path.iterdir():
            if not exp_dir.is_dir():
                continue
                
            # 历实验下的所有运行
            # Traverse all runs under the experiment
            for run_dir in exp_dir.iterdir():
                if not run_dir.is_dir():
                    continue
                    
                # 读取实验信息
                # Read experiment information
                summary_file = run_dir / "summary.json"
                if not summary_file.exists():
                    continue
                    
                try:
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        exp_info = json.load(f)
                        
                    # 应用过滤器
                    # Apply filters
                    if parameter_filters and not match_filters(exp_info, parameter_filters, "parameters"):
                        continue
                    if metric_filters and not match_filters(exp_info, metric_filters, "metrics"):
                        continue
                        
                    experiments.append(exp_info)
                except Exception as e:
                    print(f"Warning: Failed to load experiment file {summary_file}: {e}")

        # 排序
        # Sort
        if sort_by:
            def get_sort_value(exp: Dict) -> Any:
                if sort_by.startswith('parameters.'):
                    param_name = sort_by.split('.')[1]
                    return exp.get('parameters', {}).get(param_name)
                elif sort_by.startswith('metrics.'):
                    metric_name = sort_by.split('.')[1]
                    return exp.get('metrics', {}).get(metric_name)
                else:
                    return exp.get(sort_by)
            
            experiments.sort(
                key=get_sort_value,
                reverse=not sort_ascending
            )

        # 限制结果数量
        # Limit the number of results
        if limit is not None:
            experiments = experiments[:limit]

        return experiments
    

    def get_params(self) -> Dict:
        """获取当前所有参数
        Get all current parameters"""
        return self._params.copy()
    
    def get_metrics(self) -> Dict:
        """获取当前所有指标
        Get all current metrics"""
        return self._metrics.copy()
    
    def get_artifacts(self) -> Dict[str, List[str]]:
        """获取当前运行的所有文件工件（实例方法）
        Get all file artifacts of the current run (instance method)"""
        return self.get_current_artifacts()

    @classmethod
    def get_experiment(cls, 
                      experiment_name: str, 
                      base_dir: str = "./orruns_experiments",
                      run_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed information of the experiment
        
        Args:
            experiment_name: Name of the experiment
            base_dir: Base directory where experiment data is stored
            run_id: Optional run ID, if specified only return information for that run

        Returns:
            A dictionary containing experiment information, formatted as:
            {
                "name": str,                # Experiment name
                "runs": List[Dict],         # List of run records
                "total_runs": int,          # Total number of runs
                "latest_run": Dict,         # Latest run record
                "parameters": Dict,         # Parameters of the latest run
                "metrics": Dict,            # Metrics of the latest run
                "created_at": str,          # First run time
                "last_updated": str         # Last update time
            }

        Raises:
            FileNotFoundError: When the experiment does not exist
            ValueError: When the specified run ID does not exist
        """
        exp_dir = pathlib.Path(base_dir) / experiment_name
        if not exp_dir.exists():
            raise FileNotFoundError(f"Experiment '{experiment_name}' not found")

        runs = []
        for run_dir in sorted(exp_dir.iterdir(), reverse=True):
            if not run_dir.is_dir():
                continue

            run_info = {
                "run_id": run_dir.name,
                "timestamp": run_dir.name.split("_")[0],  # 从运行ID中提取时间戳
                "params": {},
                "metrics": {}
            }

            # 读取参数
            # Read parameters
            params_file = run_dir / "params" / "params.json"
            if params_file.exists():
                with open(params_file, 'r', encoding='utf-8') as f:
                    run_info["params"] = json.load(f)

            # 读取指标
            # Read metrics
            metrics_file = run_dir / "metrics" / "metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    run_info["metrics"] = json.load(f)

            runs.append(run_info)

        if not runs:
            raise FileNotFoundError(f"No runs found for experiment '{experiment_name}'")

        # 如果指定了运行ID，只返回该运行的信息
        # If a run ID is specified, only return information for that run
        if run_id:
            run = next((r for r in runs if r["run_id"] == run_id), None)
            if run is None:
                raise ValueError(f"Run '{run_id}' not found in experiment '{experiment_name}'")
            return {
                "name": experiment_name,
                "run": run,
                "parameters": run["params"],
                "metrics": run["metrics"],
                "timestamp": run["timestamp"]
            }

        # 修改时间戳解析逻辑
        # Modify timestamp parsing logic
        def parse_timestamp(ts: str) -> datetime:
            """解析时间戳字符串
            Parse timestamp string"""
            try:
                return datetime.strptime(ts, "%Y%m%d_%H%M%S_%f")
            except ValueError:
                try:
                    return datetime.strptime(ts, "%Y%m%d")
                except ValueError:
                    return datetime.strptime(ts, "%Y%m%d_%H%M%S")
        
        # 计算实验的汇总信息
        # Calculate summary information of the experiment

        first_run = runs[-1]  # Earliest run
  
        latest_run = runs[0]  # Latest run
        
        # 格式化时间
        # Format time
        created_at = parse_timestamp(first_run["timestamp"])
        last_updated = parse_timestamp(latest_run["timestamp"])

        return {
            "name": experiment_name,
            "runs": runs,
            "total_runs": len(runs),
            "latest_run": latest_run,
            "parameters": latest_run["params"],
            "metrics": latest_run["metrics"],
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated": last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def get_run(cls, 
                experiment_name: str, 
                run_id: str,
                base_dir: str = "./orruns_experiments") -> Dict[str, Any]:
        """
        Get detailed information of a specific run
        
        Args:
            experiment_name: Name of the experiment
            run_id: Run ID
            base_dir: Base directory where experiment data is stored

        Returns:
            A dictionary containing run information
        Raises:
            FileNotFoundError: When the experiment or run does not exist
        """
        return cls.get_experiment(experiment_name, base_dir, run_id)
    

    @classmethod
    def get_artifact(cls,
                    experiment_name: str,
                    run_id: str,
                    artifact_path: str,
                    artifact_type: str = None,
                    base_dir: str = "./orruns_experiments") -> pathlib.Path:
        """
        Get the path of a specific file artifact
        
        Args:
            experiment_name: Name of the experiment
            run_id: Run ID
            artifact_path: Path of the artifact file
            artifact_type: Type of the artifact ('figure', 'data', or None)
            base_dir: Base directory where experiment data is stored
            
        Returns:
            Full path of the file
            
        Raises:
            FileNotFoundError: When the file does not exist
        """
        
        run_dir = pathlib.Path(base_dir) / experiment_name / run_id
        artifacts_dir = run_dir / "artifacts"

        if artifact_type == 'figure':
            full_path = artifacts_dir / "figures" / artifact_path
        elif artifact_type == 'data':
            full_path = artifacts_dir / "data" / artifact_path
        else:
            full_path = artifacts_dir / artifact_path

        if not full_path.exists():
            raise FileNotFoundError(f"Artifact not found: {full_path}")
            
        return full_path

    @classmethod
    def load_artifact(cls,
                     experiment_name: str,
                     run_id: str,
                     artifact_path: str,
                     artifact_type: str = None,
                     base_dir: str = "./orruns_experiments") -> Any:
        """
        Load the content of a file artifact
        
        Args:
            experiment_name: Name of the experiment
            run_id: Run ID
            artifact_path: Path of the artifact file
            artifact_type: Type of the artifact ('figure', 'data', or None)
            base_dir: Base directory where experiment data is stored
            
        Returns:
            File content (automatically choose loading method based on file type)
            
        """
        file_path = cls.get_artifact(experiment_name, run_id, artifact_path, 
                                   artifact_type, base_dir)
        
        suffix = file_path.suffix.lower()
        
        if suffix in ['.npy']:
            return np.load(file_path)
        elif suffix in ['.npz']:
            return np.load(file_path, allow_pickle=True)
        elif suffix in ['.csv']:
            return pd.read_csv(file_path)
        elif suffix in ['.json']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif suffix in ['.txt', '.log']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    @classmethod
    def list_artifacts(cls,
                       experiment_name: str,
                       run_id: str,
                       base_dir: str = "./orruns_experiments") -> Dict[str, List[str]]:
        """获取指定实验运行的所有文件工件（类方法）
        Get all file artifacts of the specified experiment run (class method)"""
        run_dir = pathlib.Path(base_dir) / experiment_name / run_id
        if not run_dir.exists():
            raise FileNotFoundError(f"Run directory not found: {run_dir}")

        def get_files(directory: pathlib.Path) -> List[str]:
            if not directory.exists():
                return []
            return [
                str(file_path.relative_to(directory))
                for file_path in directory.rglob("*")
                if file_path.is_file()
            ]

        artifacts_dir = run_dir / "artifacts"
        figures_dir = artifacts_dir / "figures"
        data_dir = artifacts_dir / "data"

        return {
            "figures": get_files(figures_dir),
            "data": get_files(data_dir),
            "others": [
                str(p.relative_to(artifacts_dir)) 
                for p in artifacts_dir.glob("*") 
                if p.is_file() and p.parent == artifacts_dir
            ]
        }
    def _get_storage_dir(self) -> str:
        """Get the storage directory
        获取存储目录
        """
        data_dir = self.config.get_data_dir()
        if not data_dir:
            raise ValueError("Data directory not set. Please run 'orruns config --data-dir PATH' first")
        return os.path.join(data_dir, 'experiments')
    
    
    @classmethod
    def get_run_artifacts(cls,
                         experiment_name: str,
                         run_id: str,
                         base_dir: str = "./orruns_experiments") -> Dict[str, List[str]]:
        """获取指定实验运行的所有文件工件（类方法）
        Get all file artifacts of the specified experiment run (class method)"""
        return cls.list_artifacts(experiment_name, run_id, base_dir)

    def get_current_artifacts(self) -> Dict[str, List[str]]:
        """获取当前运行的所有文件工件
        Get all file artifacts of the current run"""
        return self.__class__.list_artifacts(
            self.experiment_name,
            self.run_id,
            str(self.base_dir)
        )