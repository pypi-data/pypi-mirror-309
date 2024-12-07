"""
包配置相关的类和工具
用于解析和管理 pyproject.toml 配置文件
"""
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import tomli
import logging

logger = logging.getLogger(__name__)

@dataclass
class PackageConfig:
    """包配置类，用于存储打包相关的所有配置信息"""
    
    name: str
    version: str
    description: str = ""
    author: str = ""
    author_email: str = ""
    packages: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    python_requires: str = ">=3.7"
    
    @classmethod
    def from_pyproject(cls, path: Path) -> "PackageConfig":
        """从 pyproject.toml 文件加载配置"""
        try:
            with open(path, "rb") as f:
                data = tomli.load(f)
            
            # 支持 poetry 和标准格式
            if "tool" in data and "poetry" in data["tool"]:
                config = data["tool"]["poetry"]
                authors = config.get("authors", [""])[0].split("<")
                author = authors[0].strip()
                author_email = authors[1].rstrip(">").strip() if len(authors) > 1 else ""
                
                return cls(
                    name=config["name"],
                    version=config["version"],
                    description=config.get("description", ""),
                    author=author,
                    author_email=author_email,
                    dependencies=list(config.get("dependencies", {}).keys()),
                    python_requires=config.get("python", ">=3.7")
                )
            else:
                project = data.get("project", {})
                authors = project.get("authors", [{}])[0]
                
                return cls(
                    name=project["name"],
                    version=project["version"],
                    description=project.get("description", ""),
                    author=authors.get("name", ""),
                    author_email=authors.get("email", ""),
                    dependencies=project.get("dependencies", []),
                    python_requires=project.get("requires-python", ">=3.7")
                )
                
        except Exception as e:
            logger.error(f"解析配置文件失败: {e}")
            raise ValueError(f"无法解析配置文件 {path}: {str(e)}") 