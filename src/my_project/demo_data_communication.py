"""数据互通演示脚本
这个脚本展示了如何使用我们创建的数据管理系统实现Python文件间的数据互通。
"""

import time
import os
from pathlib import Path
from data_manager import get_data_manager, save_data, load_data

def demo_basic_data_sharing():
    """演示基本的数据共享功能。"""
    print("\n🎯 === 基本数据共享演示 ===")
    
    # 获取数据管理器实例
    dm = get_data_manager()
    
    # 1. 保存不同类型的数据
    print("\n📝 1. 保存数据到共享存储")
    
    # 保存配置数据
    config = {
        "app_name": "数据互通演示",
        "version": "1.0.0",
        "debug": True,
        "max_connections": 100
    }
    save_data("app_config", config)
    print("✅ 保存应用配置")
    
    # 保存用户数据
    users = [
        {"id": 1, "name": "张三", "role": "admin"},
        {"id": 2, "name": "李四", "role": "user"},
        {"id": 3, "name": "王五", "role": "user"}
    ]
    save_data("users", users)
    print("✅ 保存用户数据")
    
    # 保存处理结果
    processing_result = {
        "status": "success",
        "processed_files": 5,
        "total_records": 1250,
        "processing_time": 45.6,
        "errors": []
    }
    save_data("processing_result", processing_result)
    print("✅ 保存处理结果")
    
    # 2. 读取数据
    print("\n📖 2. 从共享存储读取数据")
    
    loaded_config = load_data("app_config")
    print(f"📋 应用配置: {loaded_config['app_name']} v{loaded_config['version']}")
    
    loaded_users = load_data("users")
    print(f"👥 用户数量: {len(loaded_users)}")
    
    loaded_result = load_data("processing_result")
    print(f"📊 处理状态: {loaded_result['status']}, 记录数: {loaded_result['total_records']}")
    
    # 3. 列出所有数据
    print("\n📁 3. 当前共享数据列表")
    all_data = dm.list_shared_data()
    for key in all_data:
        info = dm.get_data_info(key)
        size_kb = info.get('size_bytes', 0) / 1024 if info else 0
        print(f"  📄 {key}: {size_kb:.2f} KB")
    
    return dm

def demo_data_update_and_sync():
    """演示数据更新和同步。"""
    print("\n🔄 === 数据更新和同步演示 ===")
    
    dm = get_data_manager()
    
    # 1. 模拟数据更新
    print("\n📝 1. 模拟数据更新过程")
    
    # 初始状态
    status = {
        "current_step": "初始化",
        "progress": 0,
        "start_time": time.time(),
        "messages": []
    }
    dm.save_shared_data("process_status", status)
    print("✅ 初始化状态")
    
    # 模拟处理步骤
    steps = [
        ("读取配置文件", 20),
        ("连接数据库", 40),
        ("处理数据", 70),
        ("生成报告", 90),
        ("完成", 100)
    ]
    
    for step_name, progress in steps:
        time.sleep(1)  # 模拟处理时间
        
        # 更新状态
        status["current_step"] = step_name
        status["progress"] = progress
        status["messages"].append(f"{time.strftime('%H:%M:%S')} - {step_name}")
        
        dm.update_shared_data("process_status", status)
        print(f"🔄 更新: {step_name} ({progress}%)")
    
    # 2. 读取最终状态
    final_status = dm.load_shared_data("process_status")
    print(f"\n✅ 最终状态: {final_status['current_step']} ({final_status['progress']}%)")
    print(f"📝 执行日志: {len(final_status['messages'])} 条消息")

def demo_cross_file_communication():
    """演示跨文件通信。"""
    print("\n🔗 === 跨文件通信演示 ===")
    
    dm = get_data_manager()
    
    # 1. 模拟文件A发送消息给文件B
    print("\n📤 1. 文件A -> 文件B 消息传递")
    
    message_queue = []
    
    # 文件A发送消息
    messages = [
        {"from": "file_a", "to": "file_b", "type": "task", "data": "开始处理用户数据"},
        {"from": "file_a", "to": "file_b", "type": "data", "data": {"user_count": 150, "active_users": 120}},
        {"from": "file_a", "to": "file_b", "type": "status", "data": "处理完成"}
    ]
    
    for msg in messages:
        msg["timestamp"] = time.time()
        message_queue.append(msg)
        dm.save_shared_data("message_queue", message_queue)
        print(f"📤 发送: {msg['type']} - {msg['data']}")
        time.sleep(0.5)
    
    # 2. 模拟文件B接收和处理消息
    print("\n📥 2. 文件B接收和处理消息")
    
    received_queue = dm.load_shared_data("message_queue")
    processed_messages = []
    
    for msg in received_queue:
        print(f"📥 接收: {msg['type']} - {msg['data']}")
        
        # 模拟处理
        processed_msg = {
            "original": msg,
            "processed_at": time.time(),
            "status": "processed"
        }
        processed_messages.append(processed_msg)
        time.sleep(0.3)
    
    # 保存处理结果
    dm.save_shared_data("processed_messages", processed_messages)
    print(f"✅ 处理完成，共处理 {len(processed_messages)} 条消息")

def demo_data_persistence():
    """演示数据持久化。"""
    print("\n💾 === 数据持久化演示 ===")
    
    dm = get_data_manager()
    
    # 1. 创建会话数据
    session_data = {
        "session_id": "demo_session_001",
        "user_id": 1,
        "login_time": time.time(),
        "activities": [],
        "preferences": {
            "theme": "dark",
            "language": "zh-CN",
            "notifications": True
        }
    }
    
    # 2. 模拟用户活动
    activities = [
        "登录系统",
        "查看仪表板",
        "编辑个人资料",
        "上传文件",
        "生成报告"
    ]
    
    print("\n📝 记录用户活动:")
    for activity in activities:
        session_data["activities"].append({
            "action": activity,
            "timestamp": time.time()
        })
        dm.save_shared_data("user_session", session_data)
        print(f"  ✅ {activity}")
        time.sleep(0.5)
    
    # 3. 验证数据持久化
    print("\n🔍 验证数据持久化:")
    
    # 重新加载数据
    loaded_session = dm.load_shared_data("user_session")
    print(f"📋 会话ID: {loaded_session['session_id']}")
    print(f"👤 用户ID: {loaded_session['user_id']}")
    print(f"📊 活动记录: {len(loaded_session['activities'])} 条")
    print(f"⚙️ 用户偏好: {loaded_session['preferences']}")
    
    # 4. 检查文件是否真的存在
    data_dir = Path(dm.data_dir)
    session_file = data_dir / "user_session.json"
    
    if session_file.exists():
        file_size = session_file.stat().st_size
        print(f"💾 数据文件: {session_file} ({file_size} 字节)")
    else:
        print("❌ 数据文件不存在")

def demo_error_handling():
    """演示错误处理。"""
    print("\n🛡️ === 错误处理演示 ===")
    
    dm = get_data_manager()
    
    # 1. 尝试读取不存在的数据
    print("\n📖 1. 读取不存在的数据")
    non_existent_data = dm.load_shared_data("non_existent_key")
    if non_existent_data is None:
        print("✅ 正确处理：返回 None")
    
    # 2. 尝试删除不存在的数据
    print("\n🗑️ 2. 删除不存在的数据")
    delete_result = dm.delete_shared_data("non_existent_key")
    if not delete_result:
        print("✅ 正确处理：返回 False")
    
    # 3. 保存和读取复杂数据结构
    print("\n🔧 3. 复杂数据结构处理")
    complex_data = {
        "nested_dict": {
            "level1": {
                "level2": {
                    "data": [1, 2, 3, {"key": "value"}]
                }
            }
        },
        "unicode_text": "这是中文测试 🎯",
        "special_chars": "!@#$%^&*()_+-=[]{}|;':,.<>?",
        "numbers": [1, 2.5, -3, 1e10],
        "booleans": [True, False, None]
    }
    
    dm.save_shared_data("complex_data", complex_data)
    loaded_complex = dm.load_shared_data("complex_data")
    
    if loaded_complex == complex_data:
        print("✅ 复杂数据结构保存和读取成功")
    else:
        print("❌ 复杂数据结构处理失败")

def run_complete_demo():
    """运行完整的演示。"""
    print("🎯" + "="*60)
    print("🎯 Python文件间数据互通完整演示")
    print("🎯" + "="*60)
    
    try:
        # 运行各个演示
        dm = demo_basic_data_sharing()
        demo_data_update_and_sync()
        demo_cross_file_communication()
        demo_data_persistence()
        demo_error_handling()
        
        # 最终总结
        print("\n🎉 === 演示总结 ===")
        all_data = dm.list_shared_data()
        total_size = 0
        
        print(f"\n📊 共享数据统计:")
        for key in all_data:
            info = dm.get_data_info(key)
            if info:
                size_bytes = info.get('size_bytes', 0)
                total_size += size_bytes
                print(f"  📄 {key}: {size_bytes/1024:.2f} KB")
        
        print(f"\n💾 总存储空间: {total_size/1024:.2f} KB")
        print(f"📁 数据文件数量: {len(all_data)}")
        print(f"📂 数据目录: {dm.data_dir}")
        
        print("\n✅ 所有演示完成！")
        print("\n🎯 主要功能:")
        print("  ✅ 基本数据保存和读取")
        print("  ✅ 数据更新和同步")
        print("  ✅ 跨文件消息传递")
        print("  ✅ 数据持久化")
        print("  ✅ 错误处理")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 启动数据互通演示")
    
    # 检查依赖文件
    required_files = ["data_manager.py", "utils.py"]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {missing_files}")
        print("请确保以下文件存在于当前目录:")
        for file in required_files:
            print(f"  - {file}")
    else:
        success = run_complete_demo()
        if success:
            print("\n🎉 演示成功完成！")
            print("\n💡 提示: 你可以查看生成的数据文件，了解数据是如何在文件间共享的。")
        else:
            print("\n❌ 演示执行失败！")