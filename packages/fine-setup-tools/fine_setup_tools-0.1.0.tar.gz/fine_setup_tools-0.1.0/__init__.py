"""
Nice Setup Tools - 简化 Python 包的打包和发布流程
一个简单易用的命令行工具，用于自动构建和发布 Python 包到 PyPI
"""

from .core import PackageBuilder
from .config import PackageConfig

__version__ = "0.1.0"
__all__ = ["PackageBuilder", "PackageConfig"] 