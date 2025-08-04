"""工具函数模块，提供通用功能。"""

import os
from typing import Dict, Optional, Any
from pathlib import Path

# 尝试导入dotenv，如果安装了的话
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


def load_environment_variables() -> Dict[str, str]:
    """加载环境变量，优先从.env文件加载。

    Returns:
        包含环境变量的字典
    """
    # 如果dotenv可用，尝试加载.env文件
    if DOTENV_AVAILABLE:
        # 查找项目根目录中的.env文件
        project_root = find_project_root()
        env_path = project_root / ".env" if project_root else None
        
        if env_path and env_path.exists():
            load_dotenv(env_path)
            print(f"已从{env_path}加载环境变量")
        else:
            print("未找到.env文件，将使用系统环境变量")
    else:
        print("警告: python-dotenv未安装，无法从.env文件加载环境变量")
        print("提示: 可以通过运行'pip install python-dotenv'安装")
    
    # 收集相关环境变量
    env_vars = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "DEFAULT_MODEL": os.environ.get("DEFAULT_MODEL", "gpt-3.5-turbo"),
        "MAX_TOKENS": os.environ.get("MAX_TOKENS", "1000"),
        "TEMPERATURE": os.environ.get("TEMPERATURE", "0.7"),
    }
    
    return env_vars


def find_project_root() -> Optional[Path]:
    """查找项目根目录，通过向上查找pyproject.toml文件。

    Returns:
        项目根目录的Path对象，如果未找到则返回None
    """
    current_dir = Path.cwd()
    
    # 向上最多查找5层目录
    for _ in range(5):
        if (current_dir / "pyproject.toml").exists():
            return current_dir
        
        # 如果已经到达根目录，停止查找
        if current_dir.parent == current_dir:
            break
            
        current_dir = current_dir.parent
    
    return None


def get_api_key(key_name: str = "OPENAI_API_KEY") -> Optional[str]:
    """获取指定的API密钥。

    Args:
        key_name: API密钥的环境变量名称

    Returns:
        API密钥，如果未设置则返回None
    """
    api_key = os.environ.get(key_name, "")
    
    if not api_key:
        print(f"警告: 未设置{key_name}环境变量")
        print(f"请在.env文件中设置{key_name}，或者通过系统环境变量设置")
        return None
    
    return api_key


def get_model_settings() -> Dict[str, Any]:
    """获取模型设置。

    Returns:
        包含模型设置的字典
    """
    return {
        "model": os.environ.get("DEFAULT_MODEL", "gpt-3.5-turbo"),
        "max_tokens": int(os.environ.get("MAX_TOKENS", "1000")),
        "temperature": float(os.environ.get("TEMPERATURE", "0.7")),
    }


if __name__ == "__main__":
    # 测试环境变量加载
    env_vars = load_environment_variables()
    
    print("\n环境变量加载结果:")
    for key, value in env_vars.items():
        # 对于API密钥，只显示前几个字符和后几个字符
        if "API_KEY" in key and value:
            masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:]
            print(f"{key}: {masked_value}")
        else:
            print(f"{key}: {value}")
    
    # 获取模型设置
    model_settings = get_model_settings()
    print("\n模型设置:")
    for key, value in model_settings.items():
        print(f"{key}: {value}")