"""
包构建和发布的核心功能
处理包的构建、测试和发布
"""
import os
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional
import logging
import toml

logger = logging.getLogger(__name__)

class PackageBuilder:
    """包构建器，处理打包和发布流程"""
    
    def __init__(self, package_path: str, name: str, version: str,
                 description: str = "", author: str = "", author_email: str = "",
                 python_requires: str = ">=3.7"):
        """
        初始化构建器
        
        Args:
            package_path: 包的根目录路径
            name: 包名
            version: 版本号
            description: 包描述
            author: 作者名称
            author_email: 作者邮箱
            python_requires: Python版本要求
        """
        self.package_path = Path(package_path).resolve()
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.author_email = author_email
        self.python_requires = python_requires
    
    def _generate_pyproject_toml(self) -> Path:
        """生成临时的 pyproject.toml 文件"""
        config = {
            "build-system": {
                "requires": ["hatchling"],
                "build-backend": "hatchling.build"
            },
            "project": {
                "name": self.name,
                "version": self.version,
                "description": self.description,
                "authors": [
                    {"name": self.author, "email": self.author_email}
                ],
                "requires-python": self.python_requires,
                "classifiers": [
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent",
                ],
            },
            "tool": {
                "hatch": {
                    "build": {
                        "targets": {
                            "wheel": {
                                # 指定要打包的文件路径
                                "include": [
                                    self.package_path.name + "/**/*.py",  # 包含所有Python文件
                                    self.package_path.name + "/**/*.pyi",  # 包含类型提示文件
                                    "README.md",  # 包含README文件
                                    "LICENSE",    # 包含许可证文件
                                ]
                            }
                        }
                    }
                }
            }
        }
        
        # 创建临时文件
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "pyproject.toml"
        
        with open(config_path, "w", encoding="utf-8") as f:
            toml.dump(config, f)
        
        return config_path
    
    def _clean_build_dirs(self):
        """清理构建目录"""
        for path in ["dist", "build", f"{self.name}.egg-info"]:
            full_path = self.package_path / path
            if full_path.exists():
                if full_path.is_dir():
                    shutil.rmtree(full_path)
                else:
                    full_path.unlink()
        logger.info("已清理旧的构建文件")
    
    def build(self):
        """构建包"""
        logger.info(f"开始构建包: {self.name}")
        
        # 生成临时配置文件
        config_path = self._generate_pyproject_toml()
        
        # 保存当前目录
        original_dir = os.getcwd()
        
        try:
            # 切换到包目录
            os.chdir(self.package_path)
            
            # 复制配置文件到包目录
            shutil.copy(config_path, "pyproject.toml")
            
            # 清理旧的构建文件
            self._clean_build_dirs()
            
            # 构建包
            subprocess.run(
                ["python", "-m", "build", "--wheel", "--sdist"],
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(f"包构建成功: {self.name} v{self.version}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"构建失败: {e.stderr}")
            raise
        finally:
            # 清理临时文件
            if os.path.exists("pyproject.toml"):
                os.remove("pyproject.toml")
            # 恢复原始目录
            os.chdir(original_dir)
            # 删除临时目录
            shutil.rmtree(config_path.parent)
    
    def upload(self, test: bool = False):
        """
        上传包到 PyPI
        
        Args:
            test: 是否上传到测试 PyPI
        """
        repo = "testpypi" if test else "pypi"
        logger.info(f"开始上传到 {repo}")
        
        try:
            cmd = [
                "python", "-m", "twine", "upload",
                "--verbose",  # 添加详细输出
                "--repository", repo,  # 使用配置文件中的仓库
            ]
            
            # 添加要上传的文件
            dist_files = list(self.package_path.glob("dist/*"))
            if not dist_files:
                raise ValueError("没有找到要上传的文件，请确保构建成功")
            cmd.extend([str(p) for p in dist_files])
            
            # 运行上传命令
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            # 输出详细信息
            if result.stdout:
                logger.info(f"上传输出: \n{result.stdout}")
            if result.stderr:
                logger.info(f"上传错误输出: \n{result.stderr}")
            
            logger.info(f"上传成功: {self.name} v{self.version}")
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or str(e)
            logger.error(f"上传失败: \n{error_msg}")
            raise 