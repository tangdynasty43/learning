"""文件B - 数据消费者示例
这个文件负责读取和使用其他文件生成的共享数据。
"""

import time
from datetime import datetime
from data_manager import get_data_manager, load_data, list_data

def check_data_availability():
    """检查共享数据的可用性。"""
    print("=== 文件B: 数据消费者 ===")
    print("检查可用的共享数据...")
    
    dm = get_data_manager()
    available_data = dm.list_shared_data()
    
    if available_data:
        print(f"✅ 发现 {len(available_data)} 个共享数据:")
        for key in available_data:
            info = dm.get_data_info(key)
            if info and info.get('exists'):
                size_kb = info['size_bytes'] / 1024
                print(f"  📄 {key}: {size_kb:.2f} KB")
    else:
        print("❌ 没有发现共享数据")
    
    return available_data

def read_excel_processing_result():
    """读取Excel处理结果。"""
    print("\n=== 读取Excel处理结果 ===")
    
    result = load_data("excel_processing_result")
    
    if result:
        print(f"📊 Excel文件: {result.get('file_path', 'Unknown')}")
        print(f"📊 工作表: {result.get('sheet_name', 'Unknown')}")
        print(f"📊 数据形状: {result.get('data_shape', 'Unknown')}")
        print(f"📊 处理状态: {result.get('status', 'Unknown')}")
        print(f"📊 处理时间: {result.get('processing_time', 'Unknown')}")
        
        if result.get('status') == 'success':
            print(f"✅ 成功处理 {result.get('row_count', 0)} 行数据")
            print(f"✅ 列名: {result.get('columns', [])}")
            
            # 显示示例数据
            sample_data = result.get('sample_data', [])
            if sample_data:
                print("\n📋 示例数据:")
                for i, row in enumerate(sample_data, 1):
                    print(f"  行{i}: {row}")
        else:
            print(f"❌ 处理失败: {result.get('error_message', 'Unknown error')}")
    else:
        print("❌ 没有找到Excel处理结果")
    
    return result

def read_statistics():
    """读取统计信息。"""
    print("\n=== 读取统计信息 ===")
    
    stats = load_data("excel_stats")
    
    if stats:
        print(f"📈 总行数: {stats.get('total_rows', 0)}")
        print(f"📈 总列数: {stats.get('total_columns', 0)}")
        print(f"📈 数值列: {stats.get('numeric_columns', 0)}")
        print(f"📈 文本列: {stats.get('text_columns', 0)}")
        print(f"📈 最后更新: {stats.get('last_updated', 'Unknown')}")
    else:
        print("❌ 没有找到统计信息")
    
    return stats

def read_user_and_project_data():
    """读取用户和项目数据。"""
    print("\n=== 读取用户和项目数据 ===")
    
    # 读取用户数据
    users = load_data("users", [])
    projects = load_data("projects", [])
    metadata = load_data("metadata", {})
    
    print(f"👥 用户数据 ({len(users)} 个用户):")
    for user in users:
        print(f"  - {user.get('name', 'Unknown')}: {user.get('age', 'Unknown')}岁, {user.get('department', 'Unknown')}")
    
    print(f"\n🚀 项目数据 ({len(projects)} 个项目):")
    for project in projects:
        status_emoji = "✅" if project.get('status') == '已完成' else "🔄" if project.get('status') == '进行中' else "📋"
        print(f"  {status_emoji} {project.get('name', 'Unknown')}: {project.get('progress', 0)}% ({project.get('status', 'Unknown')})")
    
    if metadata:
        print(f"\n📋 元数据:")
        print(f"  版本: {metadata.get('data_version', 'Unknown')}")
        print(f"  创建者: {metadata.get('created_by', 'Unknown')}")
        print(f"  创建时间: {metadata.get('created_time', 'Unknown')}")
        print(f"  描述: {metadata.get('description', 'Unknown')}")
    
    return users, projects, metadata

def monitor_processing_status():
    """监控处理状态。"""
    print("\n=== 监控处理状态 ===")
    
    status = load_data("processing_status")
    
    if status:
        current_status = status.get('current_status', 'unknown')
        message = status.get('message', '')
        timestamp = status.get('timestamp', 'Unknown')
        source = status.get('source_file', 'Unknown')
        
        status_emoji = {
            'starting': '🚀',
            'processing': '⚙️',
            'completed': '✅',
            'failed': '❌',
            'unknown': '❓'
        }.get(current_status, '❓')
        
        print(f"{status_emoji} 当前状态: {current_status}")
        print(f"📝 消息: {message}")
        print(f"⏰ 时间: {timestamp}")
        print(f"📁 来源: {source}")
    else:
        print("❌ 没有找到处理状态信息")
    
    return status

def analyze_shared_data():
    """分析所有共享数据并生成报告。"""
    print("\n=== 数据分析报告 ===")
    
    dm = get_data_manager()
    all_keys = dm.list_shared_data()
    
    report = {
        "analysis_time": datetime.now().isoformat(),
        "total_data_files": len(all_keys),
        "data_summary": {},
        "recommendations": []
    }
    
    # 分析每个数据文件
    for key in all_keys:
        data = dm.load_shared_data(key)
        info = dm.get_data_info(key)
        
        if data and info:
            report["data_summary"][key] = {
                "type": type(data).__name__,
                "size_bytes": info.get('size_bytes', 0),
                "has_content": bool(data)
            }
            
            # 根据数据类型添加更多信息
            if isinstance(data, list):
                report["data_summary"][key]["item_count"] = len(data)
            elif isinstance(data, dict):
                report["data_summary"][key]["key_count"] = len(data.keys())
    
    # 生成建议
    if "excel_processing_result" in all_keys:
        excel_result = load_data("excel_processing_result")
        if excel_result and excel_result.get('status') == 'success':
            report["recommendations"].append("Excel数据处理成功，可以进行进一步分析")
        else:
            report["recommendations"].append("Excel数据处理失败，需要检查文件路径和格式")
    
    if "users" in all_keys and "projects" in all_keys:
        report["recommendations"].append("用户和项目数据完整，可以进行关联分析")
    
    # 保存分析报告
    dm.save_shared_data("analysis_report", report)
    
    print(f"📊 共分析 {len(all_keys)} 个数据文件")
    print(f"📋 报告已保存为 'analysis_report'")
    
    return report

def wait_for_data(key: str, timeout: int = 30, check_interval: int = 2):
    """等待特定数据变为可用。
    
    Args:
        key: 要等待的数据键名
        timeout: 超时时间（秒）
        check_interval: 检查间隔（秒）
    """
    print(f"\n⏳ 等待数据 '{key}' 变为可用...")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        data = load_data(key)
        if data is not None:
            print(f"✅ 数据 '{key}' 已可用！")
            return data
        
        print(f"⏳ 等待中... ({int(time.time() - start_time)}s/{timeout}s)")
        time.sleep(check_interval)
    
    print(f"❌ 等待超时，数据 '{key}' 仍不可用")
    return None

if __name__ == "__main__":
    print("启动文件B - 数据消费者")
    
    # 检查数据可用性
    available_data = check_data_availability()
    
    if not available_data:
        print("\n⚠️ 没有发现共享数据，请先运行 file_a_producer.py")
        print("或者等待数据生成...")
        
        # 等待Excel处理结果
        excel_result = wait_for_data("excel_processing_result", timeout=60)
        if not excel_result:
            print("❌ 无法获取数据，退出程序")
            exit(1)
    
    # 读取各种数据
    excel_result = read_excel_processing_result()
    stats = read_statistics()
    users, projects, metadata = read_user_and_project_data()
    status = monitor_processing_status()
    
    # 生成分析报告
    report = analyze_shared_data()
    
    print("\n=== 数据消费完成 ===")
    print("文件B已成功读取并分析所有共享数据！")
    
    # 更新自己的状态
    dm = get_data_manager()
    consumer_status = {
        "consumer_file": "file_b_consumer.py",
        "execution_time": datetime.now().isoformat(),
        "data_processed": len(available_data),
        "status": "completed"
    }
    dm.save_shared_data("consumer_status", consumer_status)