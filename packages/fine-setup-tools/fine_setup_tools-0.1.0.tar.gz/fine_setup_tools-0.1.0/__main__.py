"""
命令行入口模块，支持 python -m nice_setup_tools 方式运行
"""
from .cli import publish

if __name__ == "__main__":
    publish() 