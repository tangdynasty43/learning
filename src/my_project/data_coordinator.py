"""数据协调器 - 管理多个文件间的数据流和执行协调
这个文件展示如何协调多个Python文件的执行和数据交换。
"""

import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from data_manager import get_data_manager, save_data, load_data, list_data

class DataCoordinator:
    """数据协调器，管理文件间的数据流和执行顺序。"""
    
    def __init__(self):
        self.dm = get_data_manager()
        self.execution_log = []
        self.start_time = datetime.now()
        
        print("🎯 数据协调器启动")
        self.log_event("coordinator_started", "数据协调器初始化完成")
    
    def log_event(self, event_type: str, message: str, data: dict = None):
        """记录执行事件。"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
            "data": data or {}
        }
        
        self.execution_log.append(event)
        print(f"📝 [{event_type}] {message}")
        
        # 保存到共享数据
        self.dm.save_shared_data("execution_log", self.execution_log)
    
    def clear_shared_data(self):
        """清理所有共享数据，重新开始。"""
        print("\n🧹 清理共享数据...")
        
        all_keys = self.dm.list_shared_data()
        cleared_count = 0
        
        for key in all_keys:
            if key != "execution_log":  # 保留执行日志
                if self.dm.delete_shared_data(key):
                    cleared_count += 1
        
        self.log_event("data_cleared", f"已清理 {cleared_count} 个共享数据文件")
        return cleared_count
    
    def run_python_file(self, file_path: str, wait_for_completion: bool = True):
        """运行Python文件。
        
        Args:
            file_path: Python文件路径
            wait_for_completion: 是否等待执行完成
        """
        file_name = Path(file_path).name
        self.log_event("file_execution_start", f"开始执行 {file_name}")
        
        try:
            if wait_for_completion:
                # 同步执行
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    cwd=Path(file_path).parent
                )
                
                if result.returncode == 0:
                    self.log_event("file_execution_success", f"{file_name} 执行成功", {
                        "stdout": result.stdout,
                        "execution_time": (datetime.now() - self.start_time).total_seconds()
                    })
                    return True
                else:
                    self.log_event("file_execution_error", f"{file_name} 执行失败", {
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    })
                    return False
            else:
                # 异步执行
                process = subprocess.Popen(
                    [sys.executable, file_path],
                    cwd=Path(file_path).parent
                )
                self.log_event("file_execution_async", f"{file_name} 异步执行启动", {
                    "pid": process.pid
                })
                return process
                
        except Exception as e:
            self.log_event("file_execution_exception", f"{file_name} 执行异常: {str(e)}")
            return False
    
    def wait_for_data(self, key: str, timeout: int = 60, check_interval: int = 2):
        """等待特定数据出现。"""
        self.log_event("wait_for_data_start", f"等待数据 '{key}'")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            data = self.dm.load_shared_data(key)
            if data is not None:
                self.log_event("wait_for_data_success", f"数据 '{key}' 已可用")
                return data
            
            time.sleep(check_interval)
        
        self.log_event("wait_for_data_timeout", f"等待数据 '{key}' 超时")
        return None
    
    def check_data_dependencies(self, required_keys: list):
        """检查数据依赖是否满足。"""
        missing_keys = []
        available_keys = []
        
        for key in required_keys:
            data = self.dm.load_shared_data(key)
            if data is not None:
                available_keys.append(key)
            else:
                missing_keys.append(key)
        
        self.log_event("dependency_check", "数据依赖检查完成", {
            "required": required_keys,
            "available": available_keys,
            "missing": missing_keys
        })
        
        return len(missing_keys) == 0, missing_keys
    
    def orchestrate_data_pipeline(self):
        """协调整个数据处理流水线。"""
        print("\n🚀 开始协调数据处理流水线")
        
        # 第一步：清理旧数据
        self.clear_shared_data()
        
        # 第二步：运行数据生产者
        producer_path = Path(__file__).parent / "file_a_producer.py"
        if producer_path.exists():
            print("\n📊 步骤1: 运行数据生产者")
            success = self.run_python_file(str(producer_path))
            
            if not success:
                self.log_event("pipeline_error", "数据生产者执行失败，停止流水线")
                return False
        else:
            self.log_event("pipeline_error", f"找不到数据生产者文件: {producer_path}")
            return False
        
        # 第三步：等待关键数据
        print("\n⏳ 步骤2: 等待关键数据生成")
        required_data = ["excel_processing_result", "users", "projects"]
        
        for key in required_data:
            data = self.wait_for_data(key, timeout=30)
            if data is None:
                self.log_event("pipeline_error", f"关键数据 '{key}' 未能及时生成")
                return False
        
        # 第四步：运行数据消费者
        consumer_path = Path(__file__).parent / "file_b_consumer.py"
        if consumer_path.exists():
            print("\n📈 步骤3: 运行数据消费者")
            success = self.run_python_file(str(consumer_path))
            
            if not success:
                self.log_event("pipeline_error", "数据消费者执行失败")
                return False
        else:
            self.log_event("pipeline_error", f"找不到数据消费者文件: {consumer_path}")
            return False
        
        # 第五步：生成最终报告
        print("\n📋 步骤4: 生成最终报告")
        self.generate_final_report()
        
        self.log_event("pipeline_success", "数据处理流水线执行完成")
        return True
    
    def generate_final_report(self):
        """生成最终的执行报告。"""
        all_data = self.dm.list_shared_data()
        
        report = {
            "pipeline_execution": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
                "status": "completed"
            },
            "data_summary": {
                "total_data_files": len(all_data),
                "data_files": all_data
            },
            "execution_events": len(self.execution_log),
            "recommendations": []
        }
        
        # 检查各个组件的执行结果
        excel_result = self.dm.load_shared_data("excel_processing_result")
        if excel_result:
            if excel_result.get('status') == 'success':
                report["recommendations"].append("✅ Excel数据处理成功")
            else:
                report["recommendations"].append("❌ Excel数据处理失败")
        
        consumer_status = self.dm.load_shared_data("consumer_status")
        if consumer_status:
            report["recommendations"].append("✅ 数据消费者执行完成")
        
        analysis_report = self.dm.load_shared_data("analysis_report")
        if analysis_report:
            report["recommendations"].append("✅ 数据分析报告已生成")
        
        # 保存最终报告
        self.dm.save_shared_data("final_pipeline_report", report)
        
        print("\n📊 === 最终执行报告 ===")
        print(f"⏱️ 执行时间: {report['pipeline_execution']['duration_seconds']:.2f} 秒")
        print(f"📁 生成数据文件: {report['data_summary']['total_data_files']} 个")
        print(f"📝 执行事件: {report['execution_events']} 个")
        print("\n🎯 执行结果:")
        for rec in report["recommendations"]:
            print(f"  {rec}")
        
        return report
    
    def monitor_data_changes(self, duration: int = 60):
        """监控共享数据的变化。
        
        Args:
            duration: 监控持续时间（秒）
        """
        print(f"\n👁️ 开始监控数据变化 ({duration}秒)")
        
        initial_data = set(self.dm.list_shared_data())
        start_time = time.time()
        
        while time.time() - start_time < duration:
            current_data = set(self.dm.list_shared_data())
            
            # 检查新增的数据
            new_data = current_data - initial_data
            if new_data:
                for key in new_data:
                    self.log_event("data_added", f"新增数据: {key}")
                initial_data = current_data
            
            time.sleep(2)
        
        print("👁️ 监控结束")

def run_interactive_demo():
    """运行交互式演示。"""
    coordinator = DataCoordinator()
    
    while True:
        print("\n" + "="*50)
        print("🎯 数据协调器 - 交互式演示")
        print("="*50)
        print("1. 运行完整数据流水线")
        print("2. 清理所有共享数据")
        print("3. 查看当前共享数据")
        print("4. 运行数据生产者")
        print("5. 运行数据消费者")
        print("6. 生成执行报告")
        print("7. 监控数据变化")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-7): ").strip()
        
        if choice == "1":
            coordinator.orchestrate_data_pipeline()
        elif choice == "2":
            coordinator.clear_shared_data()
        elif choice == "3":
            data_list = coordinator.dm.list_shared_data()
            print(f"\n📁 当前共享数据 ({len(data_list)} 个):")
            for key in data_list:
                info = coordinator.dm.get_data_info(key)
                size = info.get('size_bytes', 0) / 1024 if info else 0
                print(f"  📄 {key}: {size:.2f} KB")
        elif choice == "4":
            producer_path = Path(__file__).parent / "file_a_producer.py"
            coordinator.run_python_file(str(producer_path))
        elif choice == "5":
            consumer_path = Path(__file__).parent / "file_b_consumer.py"
            coordinator.run_python_file(str(consumer_path))
        elif choice == "6":
            coordinator.generate_final_report()
        elif choice == "7":
            duration = input("监控时长（秒，默认60）: ").strip()
            duration = int(duration) if duration.isdigit() else 60
            coordinator.monitor_data_changes(duration)
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    print("🎯 数据协调器启动")
    print("选择运行模式:")
    print("1. 自动运行完整流水线")
    print("2. 交互式演示")
    
    mode = input("请选择 (1-2): ").strip()
    
    if mode == "1":
        coordinator = DataCoordinator()
        success = coordinator.orchestrate_data_pipeline()
        if success:
            print("\n🎉 流水线执行成功！")
        else:
            print("\n❌ 流水线执行失败！")
    elif mode == "2":
        run_interactive_demo()
    else:
        print("❌ 无效选择")