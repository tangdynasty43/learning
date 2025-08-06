# Python文件间数据互通系统

这是一个完整的Python文件间数据互通解决方案，展示了如何在不同的Python文件之间高效地共享和管理数据。

## 🎯 系统概述

本系统通过JSON文件作为中间存储媒介，实现了多个Python文件之间的数据共享、状态同步和协调执行。

## 📁 文件结构

```
my_project/
├── utils.py                           # 工具函数（环境变量、项目根目录）
├── data_manager.py                     # 核心数据管理器
├── file_a_producer.py                  # 数据生产者示例
├── file_b_consumer.py                  # 数据消费者示例
├── data_coordinator.py                 # 数据协调器（高级功能）
├── demo_data_communication.py          # 基础演示脚本
├── test_change_intime.py               # 原始Excel处理文件
└── README_数据互通系统.md              # 本文档

data/                                   # 共享数据目录
├── *.json                             # 各种共享数据文件
```

## 🚀 核心功能

### 1. 数据管理器 (`data_manager.py`)

**主要特性：**
- ✅ 单例模式，确保全局唯一实例
- ✅ JSON格式存储，跨平台兼容
- ✅ 自动目录创建和管理
- ✅ 完整的CRUD操作（创建、读取、更新、删除）
- ✅ 数据信息查询（大小、修改时间等）
- ✅ 错误处理和异常管理

**核心方法：**
```python
from data_manager import get_data_manager, save_data, load_data

# 保存数据
save_data("key", {"data": "value"})

# 读取数据
data = load_data("key")

# 获取管理器实例
dm = get_data_manager()
dm.list_shared_data()  # 列出所有数据
dm.delete_shared_data("key")  # 删除数据
```

### 2. 数据生产者 (`file_a_producer.py`)

**功能：**
- 📊 处理Excel数据（基于原有的`test_change_intime.py`逻辑）
- 📝 生成用户和项目示例数据
- 📋 保存处理结果和统计信息
- 🔄 更新处理状态

**生成的数据：**
- `excel_processing_result`: Excel处理结果
- `excel_stats`: 数据统计信息
- `users`: 用户数据
- `projects`: 项目数据
- `processing_status`: 处理状态

### 3. 数据消费者 (`file_b_consumer.py`)

**功能：**
- 📖 读取生产者生成的所有数据
- 📊 生成数据分析报告
- 👁️ 监控处理状态
- ⏳ 等待数据可用性

### 4. 数据协调器 (`data_coordinator.py`)

**高级功能：**
- 🎯 协调多文件执行顺序
- 📝 记录执行日志
- ⏳ 等待数据依赖
- 🔄 监控数据变化
- 📋 生成最终报告
- 🎮 交互式管理界面

## 📖 使用方法

### 基础使用

1. **运行基础演示：**
```bash
python demo_data_communication.py
```

2. **单独运行生产者和消费者：**
```bash
# 先运行生产者
python file_a_producer.py

# 再运行消费者
python file_b_consumer.py
```

### 高级使用

1. **运行协调器（自动模式）：**
```bash
python data_coordinator.py
# 选择 1 - 自动运行完整流水线
```

2. **运行协调器（交互模式）：**
```bash
python data_coordinator.py
# 选择 2 - 交互式演示
```

## 💡 实现原理

### 数据存储机制

1. **存储格式：** JSON文件
2. **存储位置：** `C:\Users\用户名\python\data\`
3. **文件命名：** `{数据键名}.json`
4. **编码格式：** UTF-8，支持中文

### 数据同步机制

1. **写入同步：** 立即写入磁盘
2. **读取实时：** 每次读取最新文件内容
3. **并发安全：** 基于文件系统的原子操作
4. **错误恢复：** 自动处理文件不存在等异常

### 依赖管理

```python
# 等待特定数据可用
def wait_for_data(key, timeout=60):
    while timeout > 0:
        data = load_data(key)
        if data is not None:
            return data
        time.sleep(1)
        timeout -= 1
    return None
```

## 🎨 应用场景

### 1. 数据处理流水线
- 文件A处理原始数据
- 文件B进行数据清洗
- 文件C生成报告

### 2. 配置管理
- 中央配置文件
- 多模块共享配置
- 动态配置更新

### 3. 状态同步
- 进度监控
- 状态通知
- 错误报告

### 4. 缓存系统
- 计算结果缓存
- 临时数据存储
- 会话数据管理

## 📊 性能特点

### 优势
- ✅ **简单易用：** 无需复杂配置
- ✅ **跨平台：** JSON格式通用
- ✅ **可读性强：** 人类可读的数据格式
- ✅ **调试友好：** 可直接查看数据文件
- ✅ **持久化：** 程序重启后数据仍然存在

### 限制
- ⚠️ **性能：** 适合中小规模数据
- ⚠️ **并发：** 不适合高并发场景
- ⚠️ **类型：** 仅支持JSON可序列化类型

## 🔧 扩展建议

### 数据库支持
```python
# 可扩展为数据库存储
class DatabaseDataManager:
    def save_shared_data(self, key, data):
        # 存储到数据库
        pass
```

### 网络支持
```python
# 可扩展为网络共享
class NetworkDataManager:
    def save_shared_data(self, key, data):
        # 发送到远程服务器
        pass
```

### 缓存优化
```python
# 添加内存缓存
class CachedDataManager:
    def __init__(self):
        self.cache = {}
    
    def load_shared_data(self, key):
        if key in self.cache:
            return self.cache[key]
        # 从文件加载并缓存
```

## 🛡️ 最佳实践

### 1. 数据命名规范
```python
# 好的命名
save_data("user_profile", data)
save_data("processing_status", status)
save_data("config_database", config)

# 避免的命名
save_data("data", data)  # 太通用
save_data("temp", data)  # 不明确
```

### 2. 错误处理
```python
try:
    data = load_data("important_data")
    if data is None:
        # 处理数据不存在的情况
        data = get_default_data()
except Exception as e:
    # 处理其他异常
    log_error(f"数据加载失败: {e}")
```

### 3. 数据验证
```python
def validate_user_data(data):
    required_fields = ['id', 'name', 'email']
    return all(field in data for field in required_fields)

if validate_user_data(user_data):
    save_data("user", user_data)
```

## 📈 监控和调试

### 查看数据目录
```bash
# Windows
dir C:\Users\%USERNAME%\python\data

# 查看特定文件
type C:\Users\%USERNAME%\python\data\users.json
```

### 数据大小监控
```python
dm = get_data_manager()
for key in dm.list_shared_data():
    info = dm.get_data_info(key)
    print(f"{key}: {info['size_bytes']} bytes")
```

## 🎉 总结

这个数据互通系统提供了一个简单而强大的解决方案，让Python文件之间能够轻松共享数据。通过JSON文件作为中间媒介，实现了：

- 🔄 **数据共享**：多文件间无缝数据传递
- 📊 **状态同步**：实时状态更新和监控
- 🎯 **流程协调**：自动化的执行流水线
- 💾 **数据持久化**：程序重启后数据保持
- 🛡️ **错误处理**：完善的异常处理机制

无论是简单的配置共享，还是复杂的数据处理流水线，这个系统都能提供可靠的支持。