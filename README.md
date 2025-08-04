# LLM学习项目

这是一个为新手设计的LLM（大型语言模型）学习项目，旨在帮助你了解LLM的基础知识、提示工程技巧，并培养良好的编程习惯。

## 项目结构

```
├── src/                 # 源代码目录
│   └── my_project/     # 主要代码包
│       ├── __init__.py  # 包初始化文件
│       ├── __main__.py  # 主入口模块
│       ├── llm_basics.py # LLM基础模块
│       ├── exercises.py  # 练习模块
│       └── resources.py  # 学习资源模块
├── tests/              # 测试目录
│   ├── __init__.py     # 测试包初始化文件
│   └── test_llm_basics.py # LLM基础模块测试
├── docs/               # 文档目录
│   ├── getting_started.md # 入门指南
│   └── prompt_engineering.md # 提示工程指南
├── .gitignore          # Git忽略文件
├── pyproject.toml      # 项目配置和依赖管理
├── README.md           # 项目说明文档
└── .pre-commit-config.yaml  # 预提交钩子配置
```

## 特性

- 使用 `pyproject.toml` 进行现代化的项目配置和依赖管理
- 包含测试框架设置和示例测试
- 代码风格检查和格式化工具
- 类型提示支持
- 详细的文档和学习资源
- Git预提交钩子
- LLM基础概念和实践示例
- 提示工程指南和练习

## 开始使用

1. 克隆项目并创建虚拟环境：
   ```bash
   # 克隆项目（如果是从Git仓库获取）
   git clone <repository-url>
   cd llm-learning
   
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. 安装依赖：
   ```bash
   pip install -e .
   ```

3. 运行示例：
   ```bash
   python -m my_project
   ```

4. 运行测试：
   ```bash
   pytest
   ```

## LLM学习路径

本项目提供了一个结构化的LLM学习路径：

1. **基础阶段**
   - 了解LLM的基本概念和工作原理
   - 学习提示工程的基础知识
   - 掌握API的基本使用方法

2. **进阶阶段**
   - 深入学习提示工程技巧
   - 了解上下文学习和少样本学习
   - 学习框架的使用

3. **实践阶段**
   - 构建简单的问答系统
   - 实现文档摘要和信息提取
   - 开发对话式AI应用

4. **高级阶段**
   - 了解模型微调和训练技术
   - 学习评估和优化LLM应用
   - 探索RAG（检索增强生成）技术

## 学习资源

项目包含丰富的学习资源：

- `docs/getting_started.md`：LLM学习入门指南
- `docs/prompt_engineering.md`：提示工程详细指南
- `src/my_project/resources.py`：包含推荐的学习资源、书籍和学习路径
- `src/my_project/exercises.py`：提供LLM相关练习

## 良好习惯指南

- **使用虚拟环境**：隔离项目依赖，避免冲突
- **编写测试**：验证代码功能，确保质量
- **使用类型提示**：增强代码可读性和可维护性
- **遵循编码规范**：使用Black、isort等工具保持代码风格一致
- **编写文档**：为代码添加清晰的注释和文档字符串
- **使用版本控制**：通过Git管理代码变更
- **保护敏感信息**：使用环境变量存储API密钥，不要将其提交到代码库

## 实践建议

1. 从简单的LLM应用开始，如文本分类、摘要生成
2. 尝试不同的提示方式，观察结果差异
3. 参与LLM相关社区，与他人交流学习
4. 定期了解LLM领域的最新进展
5. 注意LLM的伦理问题和安全风险

## 贡献

欢迎贡献代码、报告问题或提出改进建议！

## 许可证

本项目采用MIT许可证。详见LICENSE文件。