import click
import os
from typing import Optional
from tabulate import tabulate
from datetime import datetime
from ..core.config import Config
from ..tracker import ExperimentTracker

VERSION = "0.1.0"  # Version number 版本号

@click.group()
@click.version_option(version=VERSION, prog_name="ORRuns")
def cli():
    """ORRuns Experiment Management Tool
    ORRuns实验管理工具
    """
    pass

@cli.group()
def config():
    """Configuration Management
    配置管理
    """
    pass

def format_time(timestamp_str: str) -> str:
    """Format timestamp
    格式化时间戳
    """
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S_%f")
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

def format_metrics(metrics: dict) -> str:
    """Format metrics
    格式化指标
    """
    if not metrics:
        return "N/A"
    return "; ".join(f"{k}: {v}" for k, v in metrics.items())

@cli.command()
@click.option('--last', '-l', default=10, help='Show the last n experiments')
@click.option('--pattern', '-p', default=None, help='Experiment name matching pattern')
@click.option('--detailed/--no-detailed', '-d/-nd', default=False, help='Show detailed information')
def list(last: int, pattern: Optional[str], detailed: bool):
    """List experiments
    列出实验
    """
    try:
        config = Config.get_instance()
        if not config.get_data_dir():
            raise click.ClickException("Data directory not set. Please run 'orruns config data-dir PATH' to set the data directory.")

        experiments = ExperimentTracker.list_experiments(
            base_dir=config.get_data_dir()
        )

        if not experiments:
            click.echo("No experiments found")
            return

        # Filter experiments
        # 过滤实验
        if pattern:
            import fnmatch
            experiments = [
                exp for exp in experiments 
                if fnmatch.fnmatch(exp['name'].lower(), pattern.lower())
            ]
            
            if not experiments:
                click.echo(f"No experiments found matching pattern '{pattern}'")
                return

        # Limit the number of displayed experiments
        # 限制显示的实验数量
        experiments = experiments[:last]

        if detailed:
            # Detailed view
            # 详细视图
            for exp in experiments:
                click.echo(f"\nExperiment Name: {exp['name']}")
                click.echo("Run Records:")
                headers = ["Run ID", "Time", "Parameters", "Metrics"]
                table_data = [
                    [
                        run['run_id'],
                        format_time(run['timestamp']),
                        str(run.get('params', {})),
                        format_metrics(run.get('metrics', {}))
                    ]
                    for run in exp['runs'][:5]
                ]
                click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            # Summary view
            # 概要视图
            headers = ["Experiment Name", "Number of Runs", "Last Run Time"]
            table_data = [
                [
                    exp['name'],
                    len(exp['runs']),
                    format_time(exp['runs'][0]['timestamp']) if exp['runs'] else "N/A"
                ]
                for exp in experiments
            ]
            click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))

    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('experiment_name')
@click.option('--run-id', '-r', help='Specific Run ID')
def info(experiment_name: str, run_id: Optional[str]):
    """View experiment details
    查看实验详情
    """
    try:
        config = Config.get_instance()
        exp_info = ExperimentTracker.get_experiment(
            experiment_name=experiment_name,
            base_dir=config.get_data_dir(),
            run_id=run_id
        )
        
        if run_id:
            # Show details of a specific run
            run = exp_info['run']
            click.echo(f"\nRun ID: {run['run_id']}")
            click.echo(f"Time: {format_time(run['timestamp'])}")
            click.echo("\nParameters:")
            for k, v in run.get('params', {}).items():
                click.echo(f"  {k}: {v}")
            click.echo("\nMetrics:")
            for k, v in run.get('metrics', {}).items():
                click.echo(f"  {k}: {v}")
        else:
            # Show experiment overview
            click.echo(f"\nExperiment Name: {exp_info['name']}")
            click.echo(f"Total Runs: {exp_info['total_runs']}")
            click.echo(f"Last Updated: {exp_info['last_updated']}")
            
            # Show recent run records
            click.echo("\nRecent Run Records:")
            headers = ["Run ID", "Time", "Parameters", "Metrics"]
            table_data = [
                [
                    run['run_id'],
                    format_time(run['timestamp']),
                    str(run.get('params', {})),
                    format_metrics(run.get('metrics', {}))
                ]
                for run in exp_info['runs'][:5]  # Show only the last 5 runs 只显示最近的5次运行
            ]
            click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
            
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('experiment_name')
@click.option('--run-id', '-r', help='Specific Run ID')
@click.option('--force/--no-force', '-f/-nf', default=False, help='Force delete without confirmation')
def delete(experiment_name: str, run_id: Optional[str], force: bool):
    """Delete experiment or specific run
    删除实验或特定运行
    """
    try:
        if not force:
            msg = f"Are you sure you want to delete experiment '{experiment_name}'"
            if run_id:
                msg += f" run '{run_id}'"
            msg += "? [y/N]: "
            
            if not click.confirm(msg):
                click.echo("Operation cancelled")
                return

        config = Config.get_instance()
        ExperimentTracker.delete_experiment(
            experiment_name=experiment_name,
            base_dir=config.get_data_dir(),
            run_id=run_id
        )
        
        if run_id:
            click.echo(f"Deleted run '{run_id}' of experiment '{experiment_name}'")
        else:
            click.echo(f"Deleted experiment '{experiment_name}'")
            
    except Exception as e:
        raise click.ClickException(str(e))

@config.command()
@click.argument('path', type=click.Path())
def data_dir(path):
    """Set experiment data directory
    设置实验数据目录
    """
    try:
        # Create directory (if it does not exist)
        # 创建目录（如果不存在）
        os.makedirs(path, exist_ok=True)
        
        config = Config.get_instance()
        config.set_data_dir(path)
        click.echo(f"Data directory set to: {path}")
    except Exception as e:
        raise click.ClickException(f"Failed to set data directory: {str(e)}")

@config.command()
def show():
    """Show current configuration
    显示当前配置
    """
    try:
        config = Config.get_instance()
        data_dir = config.get_data_dir()
        
        click.echo("\nCurrent Configuration:")
        click.echo(f"Data Directory: {data_dir or 'Not set'}")
        click.echo(f"Version: {VERSION}")
    except Exception as e:
        raise click.ClickException(str(e))