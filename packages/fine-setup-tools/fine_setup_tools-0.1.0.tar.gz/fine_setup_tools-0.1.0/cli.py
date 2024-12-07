"""
命令行工具模块
"""
import click
import logging
from pathlib import Path
from typing import Optional
from .core import PackageBuilder

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('name')
@click.argument('version')
@click.option('--description', '-d', default='', help='包的简短描述')
@click.option('--author', '-a', default='', help='作者名称')
@click.option('--email', '-e', default='', help='作者邮箱')
@click.option('--requires-python', default='>=3.7', help='Python版本要求')
@click.option('--test/--no-test', default=True, help='是否先发布到测试PyPI (默认: 是)')
def publish(path: str, name: str, version: str, description: str,
           author: str, email: str, requires_python: str, test: bool):
    """
    简单的Python包发布工具
    
    使用方法:
        python -m nice_setup_tools PATH NAME VERSION [OPTIONS]
    
    示例:
        python -m nice_setup_tools ./my-package my-package 0.1.0 -d "My package" -a "Author" -e "email@example.com"
    """
    try:
        # 初始化构建器
        builder = PackageBuilder(
            package_path=path,
            name=name,
            version=version,
            description=description,
            author=author,
            author_email=email,
            python_requires=requires_python
        )
        
        # 构建包
        logger.info("开始构建包...")
        builder.build()
        logger.info("包构建完成")
        
        if test:
            # 发布到测试环境
            logger.info("开始发布到测试PyPI...")
            builder.upload(test=True)
            logger.info("测试发布完成")
            
            # 询问是否继续发布到正式环境
            if click.confirm('测试发布成功，是否发布到正式PyPI?'):
                logger.info("开始发布到正式PyPI...")
                builder.upload(test=False)
                logger.info("正式发布完成")
        else:
            # 直接发布到正式环境
            logger.info("开始发布到正式PyPI...")
            builder.upload(test=False)
            logger.info("发布完成")
            
        logger.info(f"🎉 恭喜！{name} v{version} 发布成功！")
        
    except Exception as e:
        logger.error(f"发布过程中出现错误: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    publish() 