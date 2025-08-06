"""数据管理模块，实现Python文件间数据互通。"""

import json
import os
from pathlib import Path
from typing import Any, Optional, Dict
from utils import get_model_settings, find_project_root


class DataManager:
    """数据管理器，用于实现Python文件间的数据共享和持久化。"""
    
    def __init__(self, data_dir_name: str = "data"):
        """初始化数据管理器。
        
        Args:
            data_dir_name: 数据目录名称，默认为"data"
        """
        self.config = get_model_settings()
        project_root = find_project_root()
        
        if project_root:
            self.data_dir = project_root / data_dir_name
        else:
            # 如果找不到项目根目录，使用当前目录
            self.data_dir = Path.cwd() / data_dir_name
        
        # 确保数据目录存在
        self.data_dir.mkdir(exist_ok=True)
        
        print(f"数据管理器初始化完成，数据目录: {self.data_dir}")
    
    def save_shared_data(self, key: str, data: Any) -> bool:
        """保存共享数据到JSON文件。
        
        Args:
            key: 数据的唯一标识符
            data: 要保存的数据（必须可JSON序列化）
            
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            file_path = self.data_dir / f"{key}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存: {key} -> {file_path}")
            return True
        except Exception as e:
            print(f"保存数据失败: {key}, 错误: {e}")
            return False
    
    def load_shared_data(self, key: str, default: Any = None) -> Any:
        """从JSON文件加载共享数据。
        
        Args:
            key: 数据的唯一标识符
            default: 如果数据不存在时返回的默认值
            
        Returns:
            加载的数据，如果文件不存在或加载失败则返回default
        """
        try:
            file_path = self.data_dir / f"{key}.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"数据已加载: {key} <- {file_path}")
                return data
            else:
                print(f"数据文件不存在: {key}")
                return default
        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {key}, 错误: {e}")
            return default
        except Exception as e:
            print(f"加载数据失败: {key}, 错误: {e}")
            return default
    
    def delete_shared_data(self, key: str) -> bool:
        """删除共享数据文件。
        
        Args:
            key: 数据的唯一标识符
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            file_path = self.data_dir / f"{key}.json"
            if file_path.exists():
                file_path.unlink()
                print(f"数据已删除: {key}")
                return True
            else:
                print(f"数据文件不存在，无需删除: {key}")
                return False
        except Exception as e:
            print(f"删除数据失败: {key}, 错误: {e}")
            return False
    
    def list_shared_data(self) -> list:
        """列出所有共享数据的键名。
        
        Returns:
            list: 所有数据键名的列表
        """
        try:
            json_files = list(self.data_dir.glob("*.json"))
            keys = [f.stem for f in json_files]  # 获取不带扩展名的文件名
            print(f"共享数据列表: {keys}")
            return keys
        except Exception as e:
            print(f"列出数据失败, 错误: {e}")
            return []
    
    def update_shared_data(self, key: str, update_data: Dict, merge: bool = True) -> bool:
        """更新共享数据。
        
        Args:
            key: 数据的唯一标识符
            update_data: 要更新的数据
            merge: 是否与现有数据合并，True为合并，False为覆盖
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        try:
            if merge:
                # 合并模式：先加载现有数据，然后更新
                existing_data = self.load_shared_data(key, {})
                if isinstance(existing_data, dict) and isinstance(update_data, dict):
                    existing_data.update(update_data)
                    return self.save_shared_data(key, existing_data)
                else:
                    print(f"合并失败: 数据类型不匹配，使用覆盖模式")
                    return self.save_shared_data(key, update_data)
            else:
                # 覆盖模式：直接保存新数据
                return self.save_shared_data(key, update_data)
        except Exception as e:
            print(f"更新数据失败: {key}, 错误: {e}")
            return False
    
    def get_data_info(self, key: str) -> Optional[Dict]:
        """获取数据文件的信息。
        
        Args:
            key: 数据的唯一标识符
            
        Returns:
            包含文件信息的字典，如果文件不存在返回None
        """
        try:
            file_path = self.data_dir / f"{key}.json"
            if file_path.exists():
                stat = file_path.stat()
                return {
                    "file_path": str(file_path),
                    "size_bytes": stat.st_size,
                    "created_time": stat.st_ctime,
                    "modified_time": stat.st_mtime,
                    "exists": True
                }
            else:
                return {"exists": False}
        except Exception as e:
            print(f"获取文件信息失败: {key}, 错误: {e}")
            return None


# 创建全局数据管理器实例
_global_data_manager = None

def get_data_manager() -> DataManager:
    """获取全局数据管理器实例（单例模式）。
    
    Returns:
        DataManager: 全局数据管理器实例
    """
    global _global_data_manager
    if _global_data_manager is None:
        _global_data_manager = DataManager()
    return _global_data_manager


# 便捷函数
def save_data(key: str, data: Any) -> bool:
    """保存数据的便捷函数。"""
    return get_data_manager().save_shared_data(key, data)

def load_data(key: str, default: Any = None) -> Any:
    """加载数据的便捷函数。"""
    return get_data_manager().load_shared_data(key, default)

def delete_data(key: str) -> bool:
    """删除数据的便捷函数。"""
    return get_data_manager().delete_shared_data(key)

def list_data() -> list:
    """列出所有数据的便捷函数。"""
    return get_data_manager().list_shared_data()


if __name__ == "__main__":
    # 测试数据管理器
    dm = DataManager()
    
    # 测试保存和加载
    test_data = {
        "user_name": "张三",
        "age": 25,
        "skills": ["Python", "数据分析", "机器学习"]
    }
    
    print("\n=== 测试数据管理器 ===")
    
    # 保存数据
    dm.save_shared_data("user_profile", test_data)
    
    # 加载数据
    loaded_data = dm.load_shared_data("user_profile")
    print(f"加载的数据: {loaded_data}")
    
    # 更新数据
    update_info = {"age": 26, "location": "北京"}
    dm.update_shared_data("user_profile", update_info)
    
    # 再次加载查看更新结果
    updated_data = dm.load_shared_data("user_profile")
    print(f"更新后的数据: {updated_data}")
    
    # 列出所有数据
    all_keys = dm.list_shared_data()
    print(f"所有数据键: {all_keys}")
    
    # 获取文件信息
    info = dm.get_data_info("user_profile")
    print(f"文件信息: {info}")