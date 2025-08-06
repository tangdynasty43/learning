"""文件A - 数据生产者示例
这个文件负责生成和保存数据，供其他文件使用。
"""

import pandas as pd
from datetime import datetime
from data_manager import get_data_manager, save_data

def process_excel_data():
    """处理Excel数据并保存结果供其他文件使用。"""
    print("=== 文件A: 数据生产者 ===")
    
    # 模拟处理Excel数据（使用之前的test_change_intime.py逻辑）
    excel_path = "C:/Users/唐朝/Desktop/12345.xlsx"
    
    try:
        # 读取Excel数据
        df = pd.read_excel(excel_path, sheet_name="Sheet1")
        
        # 数据处理结果
        processing_result = {
            "file_path": excel_path,
            "sheet_name": "Sheet1",
            "data_shape": df.shape,
            "columns": df.columns.tolist(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "processing_time": datetime.now().isoformat(),
            "status": "success",
            "sample_data": df.head(3).to_dict('records') if len(df) > 0 else []
        }
        
        # 保存处理结果到共享数据
        dm = get_data_manager()
        dm.save_shared_data("excel_processing_result", processing_result)
        
        # 保存统计信息
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "numeric_columns": len(df.select_dtypes(include=['number']).columns),
            "text_columns": len(df.select_dtypes(include=['object']).columns),
            "last_updated": datetime.now().isoformat()
        }
        dm.save_shared_data("excel_stats", stats)
        
        # 使用便捷函数保存配置信息
        config = {
            "default_excel_path": excel_path,
            "default_sheet": "Sheet1",
            "auto_process": True
        }
        save_data("app_config", config)
        
        print(f"✅ 数据处理完成，共 {len(df)} 行 {len(df.columns)} 列")
        print(f"✅ 处理结果已保存到共享数据")
        
        return processing_result
        
    except FileNotFoundError:
        error_result = {
            "file_path": excel_path,
            "status": "error",
            "error_message": "文件不存在",
            "processing_time": datetime.now().isoformat()
        }
        save_data("excel_processing_result", error_result)
        print(f"❌ 文件不存在: {excel_path}")
        return error_result
        
    except Exception as e:
        error_result = {
            "file_path": excel_path,
            "status": "error",
            "error_message": str(e),
            "processing_time": datetime.now().isoformat()
        }
        save_data("excel_processing_result", error_result)
        print(f"❌ 处理失败: {e}")
        return error_result

def generate_sample_data():
    """生成一些示例数据供其他文件使用。"""
    print("\n=== 生成示例数据 ===")
    
    # 用户数据
    users = [
        {"id": 1, "name": "张三", "age": 25, "department": "技术部"},
        {"id": 2, "name": "李四", "age": 30, "department": "销售部"},
        {"id": 3, "name": "王五", "age": 28, "department": "市场部"}
    ]
    
    # 项目数据
    projects = [
        {"id": 101, "name": "数据分析项目", "status": "进行中", "progress": 75},
        {"id": 102, "name": "网站优化", "status": "已完成", "progress": 100},
        {"id": 103, "name": "移动应用开发", "status": "计划中", "progress": 10}
    ]
    
    # 保存数据
    dm = get_data_manager()
    dm.save_shared_data("users", users)
    dm.save_shared_data("projects", projects)
    
    # 保存元数据
    metadata = {
        "data_version": "1.0",
        "created_by": "file_a_producer.py",
        "created_time": datetime.now().isoformat(),
        "description": "示例用户和项目数据"
    }
    dm.save_shared_data("metadata", metadata)
    
    print(f"✅ 已生成 {len(users)} 个用户和 {len(projects)} 个项目数据")
    print("✅ 数据已保存到共享存储")

def update_processing_status(status: str, message: str = ""):
    """更新处理状态，供其他文件监控。"""
    status_info = {
        "current_status": status,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "source_file": "file_a_producer.py"
    }
    
    dm = get_data_manager()
    dm.save_shared_data("processing_status", status_info)
    print(f"📊 状态更新: {status} - {message}")

if __name__ == "__main__":
    print("启动文件A - 数据生产者")
    
    # 更新状态
    update_processing_status("starting", "开始数据处理")
    
    # 处理Excel数据
    result = process_excel_data()
    
    # 生成示例数据
    generate_sample_data()
    
    # 更新最终状态
    if result.get("status") == "success":
        update_processing_status("completed", "所有数据处理完成")
    else:
        update_processing_status("failed", "数据处理失败")
    
    print("\n文件A执行完成！")
    print("其他文件现在可以访问共享数据了。")