import platform
import psutil
import multiprocessing as mp
import time
from typing import Dict, Optional
from functools import lru_cache
import os
import sys
import cpuinfo

@lru_cache(maxsize=1)
def get_system_info(
    experiment_name: Optional[str] = None, 
    parallel: Optional[bool] = None, 
    times: Optional[int] = None, 
    max_workers: Optional[int] = None,
    detailed: bool = False  # 是否返回详细信息
) -> Dict:
    """
    收集系统信息，默认返回运筹学论文常用的关键信息
    
    Args:
        experiment_name: 实验名称
        parallel: 是否并行执行
        times: 重复次数
        max_workers: 最大工作进程数
        detailed: 是否返回全部详细信息，默认False只返回论文关键信息
        
    Returns:
        包含系统信息的字典
    """
    # 获取CPU信息
    cpu_info = cpuinfo.get_cpu_info()
    
    # 运筹学论文常用的关键信息
    system_info = {
        "hardware": {
            "cpu": {
                "model": cpu_info.get('brand_raw', 'Unknown'),
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "base_frequency_ghz": round(cpu_info.get('hz_advertised_raw', [0])[0] / 1000000000, 2)
            },
            "memory": {
                "total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }
        },
        "software": {
            "os": f"{platform.system()} {platform.release()}",
            "python": platform.python_version(),
            "key_packages": {
                "numpy": __import__('numpy').__version__,
                "scipy": __import__('scipy').__version__
            }
        }
    }
    
    # GPU信息（如果有）
    try:
        import torch
        if torch.cuda.is_available():
            system_info["hardware"]["gpu"] = {
                "model": torch.cuda.get_device_name(0),
                "count": torch.cuda.device_count(),
                "memory_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
            }
    except ImportError:
        pass

    # 如果需要详细信息
    if detailed:
        system_info.update({
            "hardware": {
                "cpu": {
                    **system_info["hardware"]["cpu"],
                    "architecture": cpu_info.get('arch', platform.machine()),
                    "max_frequency_mhz": psutil.cpu_freq().max if hasattr(psutil.cpu_freq(), 'max') else None,
                    "cache_size": cpu_info.get('l2_cache_size', 'Unknown'),
                    "instruction_set": cpu_info.get('flags', [])
                },
                "memory": {
                    **system_info["hardware"]["memory"],
                    "available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
                    "type": "Unknown",
                    "speed": "Unknown"
                },
                "disk": {
                    "total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
                    "free_gb": round(psutil.disk_usage('/').free / (1024 ** 3), 2)
                }
            },
            "software": {
                "os": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine()
                },
                "python": {
                    "version": platform.python_version(),
                    "implementation": platform.python_implementation(),
                    "compiler": platform.python_compiler(),
                    "location": sys.executable
                },
                "packages": {
                    **system_info["software"]["key_packages"],
                    "pandas": __import__('pandas').__version__,
                    "matplotlib": __import__('matplotlib').__version__,
                    "torch": __import__('torch').__version__ if 'torch' in sys.modules else None
                }
            }
        })
        
        # 详细GPU信息
        if "gpu" in system_info["hardware"]:
            system_info["hardware"]["gpu"].update({
                "devices": [
                    {
                        "name": torch.cuda.get_device_name(i),
                        "total_memory_gb": round(torch.cuda.get_device_properties(i).total_memory / (1024**3), 2),
                        "compute_capability": f"{torch.cuda.get_device_capability(i)[0]}.{torch.cuda.get_device_capability(i)[1]}"
                    }
                    for i in range(torch.cuda.device_count())
                ],
                "cuda_version": torch.version.cuda,
                "cudnn_version": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
            })

    # 实验配置信息
    if experiment_name is not None:
        system_info["experiment"] = {
            "name": experiment_name,
            "parallel": parallel,
            "times": times,
            "max_workers": max_workers if parallel else None,
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 详细实验信息
        if detailed:
            system_info["experiment"].update({
                "process_affinity": list(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None,
                "current_memory_usage_gb": round(psutil.Process().memory_info().rss / (1024 ** 3), 2)
            })
    
    return system_info


from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.json import JSON
from rich.table import Table
from rich.text import Text

def print_system_info(system_info: Dict) -> None:
    """
    使用rich库美化打印系统信息
    
    Args:
        system_info: 系统信息字典
    """
    console = Console()
    
    # 创建硬件信息表格
    hw_table = Table(show_header=True, header_style="bold magenta")
    hw_table.add_column("Component", style="cyan")
    hw_table.add_column("Specification", style="green")
    
    # CPU信息
    cpu_info = system_info["hardware"]["cpu"]
    hw_table.add_row(
        "CPU",
        f"{cpu_info['model']}\n"
        f"Cores: {cpu_info['physical_cores']} Physical / {cpu_info['logical_cores']} Logical\n"
        f"Base Frequency: {cpu_info['base_frequency_ghz']} GHz"
    )
    
    # 内存信息
    hw_table.add_row(
        "Memory",
        f"Total: {system_info['hardware']['memory']['total_gb']} GB"
    )
    
    # GPU信息（如果有）
    if "gpu" in system_info["hardware"]:
        gpu_info = system_info["hardware"]["gpu"]
        hw_table.add_row(
            "GPU",
            f"{gpu_info['model']}\n"
            f"Count: {gpu_info['count']}\n"
            f"Memory: {gpu_info['memory_gb']} GB"
        )
    
    # 创建软件信息表格
    sw_table = Table(show_header=True, header_style="bold magenta")
    sw_table.add_column("Component", style="cyan")
    sw_table.add_column("Version", style="green")
    
    # 修复 OS 信息显示
    os_info = system_info["software"]["os"]
    if isinstance(os_info, dict):
        os_str = f"{os_info['system']} {os_info['release']}"
    else:
        os_str = os_info
    sw_table.add_row("OS", os_str)
    
    # 修复 Python 信息显示
    python_info = system_info["software"]["python"]
    if isinstance(python_info, dict):
        python_str = python_info["version"]
    else:
        python_str = python_info
    sw_table.add_row("Python", python_str)
    
    # 修复包版本信息显示
    if "packages" in system_info["software"]:
        packages = system_info["software"]["packages"]
    elif "key_packages" in system_info["software"]:
        packages = system_info["software"]["key_packages"]
    else:
        packages = {}
        
    for pkg, version in packages.items():
        if version is not None:  # 只显示已安装的包
            sw_table.add_row(pkg.capitalize(), str(version))
    
    # 创建实验信息表格（如果有）
    if "experiment" in system_info:
        exp_table = Table(show_header=True, header_style="bold magenta")
        exp_table.add_column("Parameter", style="cyan")
        exp_table.add_column("Value", style="green")
        
        exp_info = system_info["experiment"]
        exp_table.add_row("Name", exp_info["name"])
        exp_table.add_row("Parallel", str(exp_info["parallel"]))
        exp_table.add_row("Times", str(exp_info["times"]))
        exp_table.add_row("Max Workers", str(exp_info["max_workers"]))
        exp_table.add_row("Start Time", exp_info["start_time"])
    
    # 创建布局
    layout = Layout()
    layout.split_column(
        Layout(Panel(
            Text("System Information", justify="center", style="bold white"),
            style="bold blue"
        ), size=3),
        Layout(name="main")
    )
    
    # 分割主区域
    if "experiment" in system_info:
        layout["main"].split_row(
            Layout(Panel(hw_table, title="Hardware", border_style="blue")),
            Layout(Panel(sw_table, title="Software", border_style="green")),
            Layout(Panel(exp_table, title="Experiment", border_style="yellow"))
        )
    else:
        layout["main"].split_row(
            Layout(Panel(hw_table, title="Hardware", border_style="blue")),
            Layout(Panel(sw_table, title="Software", border_style="green"))
        )
    
    # 打印布局
    console.print("\n")
    console.print(layout)
    console.print("\n")