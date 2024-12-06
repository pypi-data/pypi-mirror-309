from typing import Dict, List, Optional, Any
from pathlib import Path
from ..core.config import Config
from ..tracker import ExperimentTracker
import fnmatch

class ExperimentAPI:
    def __init__(self, data_dir: Optional[str] = None):
        self.config = Config.get_instance()
        if data_dir:
            self.config.set_data_dir(data_dir)
    
    def list_experiments(self, last: int = 10, pattern: Optional[str] = None) -> List[Dict]:
        """List experiments
        列出实验
        """
        experiments = ExperimentTracker.list_experiments(base_dir=self.config.get_data_dir())
        if pattern:
            experiments = [exp for exp in experiments if fnmatch.fnmatch(exp['name'], pattern)]
        return experiments[:last]
    
    def get_experiment(self, experiment_name: str) -> Dict:
        """Get experiment details
        获取实验详情
        """
        return ExperimentTracker.get_experiment(
            experiment_name=experiment_name,
            base_dir=self.config.get_data_dir()
        )
    
    def get_run(self, experiment_name: str, run_id: str) -> Dict:
        """Get details of a specific run
        获取特定运行的详情
        """
        return ExperimentTracker.get_run(
            experiment_name=experiment_name,
            run_id=run_id,
            base_dir=self.config.get_data_dir()
        )
    
    def query_experiments(self, **filters) -> List[Dict]:
        """Query experiments
        查询实验
        """
        # Validate filter format
        # 验证过滤器格式
        parameter_filters = filters.get('parameter_filters', {})
        for key in parameter_filters:
            if '__' not in key:
                raise ValueError(f"Invalid parameter filter format: {key}")
            field, op = key.split('__')
            if op not in ['gt', 'lt', 'eq', 'gte', 'lte']:
                raise ValueError(f"Invalid operator in parameter filter: {op}")
                
        return ExperimentTracker.query_experiments(
            base_dir=self.config.get_data_dir(),
            **filters
        )
    
    def get_artifacts(self, experiment_name: str, run_id: str) -> Dict[str, List[str]]:
        """Get all file artifacts of an experiment run
        获取实验运行的所有文件工件
        """
        return ExperimentTracker.list_artifacts(
            experiment_name,
            run_id,
            base_dir=self.config.get_data_dir()
        )
    
    def get_artifact_path(self, 
                         experiment_name: str,
                         run_id: str,
                         artifact_path: str,
                         artifact_type: Optional[str] = None) -> Path:
        """Get the path of a specific file artifact
        获取特定文件工件的路径
        """
        return ExperimentTracker.get_artifact(
            experiment_name=experiment_name,
            run_id=run_id,
            artifact_path=artifact_path,
            artifact_type=artifact_type,
            base_dir=self.config.get_data_dir()
        )
    
    def load_artifact(self,
                     experiment_name: str,
                     run_id: str,
                     artifact_path: str,
                     artifact_type: Optional[str] = None) -> Any:
        """Load the content of a file artifact
        加载文件工件的内容
        """
        return ExperimentTracker.load_artifact(
            experiment_name=experiment_name,
            run_id=run_id,
            artifact_path=artifact_path,
            artifact_type=artifact_type,
            base_dir=self.config.get_data_dir()
        )
