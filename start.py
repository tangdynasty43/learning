#!/usr/bin/env python
"""启动脚本，用于运行LLM学习项目。"""

import os
import sys
from pathlib import Path


def setup_environment():
    """设置环境，确保项目可以正确运行。"""
    # 获取项目根目录
    project_root = Path(__file__).parent.absolute()
    
    # 将项目根目录添加到Python路径
    sys.path.insert(0, str(project_root))
    
    # 检查是否存在.env文件
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("提示: 未找到.env文件，你可能需要从.env.example创建一个.env文件并设置API密钥")


def main():
    """主函数，运行LLM学习项目。"""
    # 设置环境
    setup_environment()
    
    try:
        # 导入并运行项目主模块
        from src.my_project.__main__ import main as project_main
        project_main()
    except ImportError as e:
        print(f"错误: 无法导入项目模块: {e}")
        print("请确保你已经安装了所有必要的依赖:")
        print("  pip install -e .")
    except Exception as e:
        print(f"运行项目时出错: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已终止。")
        sys.exit(0)