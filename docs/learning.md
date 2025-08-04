# 今日学习步骤
   1. git 语法 ✅
   2. vscode 快捷键 ⭐
   3. markdown 语法

## 1. Git 语法详解

### 🎯 Git 是什么？
Git 是一个分布式版本控制系统，帮助你：
- 跟踪代码变化
- 协作开发
- 备份代码
- 回退到之前的版本

### 📚 Git 基础概念

#### 重要术语：
- **仓库(Repository)**：存放项目的地方
- **工作区(Working Directory)**：你编辑文件的地方
- **暂存区(Staging Area)**：准备提交的文件区域
- **提交(Commit)**：保存当前状态的快照
- **分支(Branch)**：独立的开发线
- **远程仓库(Remote)**：托管在网上的仓库（如GitHub）

### 🔧 Git 基础命令

#### 1. 配置 Git（首次使用）
```bash
# 设置用户名和邮箱
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 查看配置
git config --list
```

#### 2. 创建和克隆仓库
```bash
# 初始化新仓库
git init

# 克隆远程仓库
git clone https://github.com/用户名/仓库名.git
```

#### 3. 基本工作流程
```bash
# 查看文件状态
git status

# 添加文件到暂存区
git add 文件名.txt          # 添加单个文件
git add .                   # 添加所有文件
git add *.py               # 添加所有Python文件

# 提交更改
git commit -m "提交信息"     # 提交暂存区的文件
git commit -am "提交信息"    # 添加并提交已跟踪的文件

# 查看提交历史
git log                     # 详细历史
git log --oneline          # 简洁历史
```

#### 4. 分支操作
```bash
# 查看分支
git branch                  # 查看本地分支
git branch -a              # 查看所有分支

# 创建分支
git branch 新分支名

# 切换分支
git checkout 分支名
git switch 分支名           # 新语法

# 创建并切换到新分支
git checkout -b 新分支名
git switch -c 新分支名      # 新语法

# 合并分支
git merge 分支名

# 删除分支
git branch -d 分支名
```

#### 5. 远程仓库操作
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 推送到远程仓库
git push origin main        # 推送main分支
git push -u origin main     # 首次推送并设置上游

# 从远程仓库拉取
git pull origin main        # 拉取并合并
git fetch origin           # 只拉取不合并
```

#### 6. 撤销和回退
```bash
# 撤销工作区的修改
git checkout -- 文件名
git restore 文件名          # 新语法

# 撤销暂存区的文件
git reset HEAD 文件名
git restore --staged 文件名  # 新语法

# 回退到上一个提交
git reset --soft HEAD~1     # 保留更改在暂存区
git reset --mixed HEAD~1    # 保留更改在工作区
git reset --hard HEAD~1     # 完全删除更改
```

### 📝 实际操作示例

#### 完整的Git工作流程：
```bash
# 1. 初始化项目
git init
git add .
git commit -m "初始提交"

# 2. 连接远程仓库
git remote add origin https://github.com/你的用户名/项目名.git
git push -u origin main

# 3. 日常开发
git add 修改的文件
git commit -m "添加新功能"
git push

# 4. 创建功能分支
git checkout -b feature/新功能
# 开发新功能...
git add .
git commit -m "完成新功能"
git push origin feature/新功能

# 5. 合并到主分支
git checkout main
git merge feature/新功能
git push
```

### 🚨 常见问题和解决方案

#### 问题1：提交信息写错了
```bash
git commit --amend -m "正确的提交信息"
```

#### 问题2：忘记添加文件到上次提交
```bash
git add 忘记的文件
git commit --amend --no-edit
```

#### 问题3：合并冲突
```bash
# 1. 手动编辑冲突文件
# 2. 添加解决后的文件
git add 冲突文件
# 3. 完成合并
git commit
```

### 💡 Git 最佳实践

1. **频繁提交**：小步快跑，经常提交
2. **清晰的提交信息**：描述做了什么，为什么做
3. **使用分支**：为每个功能创建分支
4. **定期推送**：避免丢失代码
5. **使用.gitignore**：忽略不需要版本控制的文件

### 📋 常用Git命令速查表

| 命令 | 作用 |
|---

## 2. VSCode 快捷键详解

### 🎯 学习目标
- 提高编程效率，减少鼠标操作
- 专业开发体验，流畅编码
- 减少疲劳，专注代码逻辑

### ⌨️ 基础快捷键

#### 1. 文件操作
```
Ctrl + N          新建文件
Ctrl + O          打开文件
Ctrl + S          保存文件
Ctrl + Shift + S  另存为
Ctrl + W          关闭当前文件
Ctrl + Shift + T  重新打开关闭的文件
Ctrl + P          快速打开文件（模糊搜索）
Ctrl + Tab        在打开的文件间切换
```

#### 2. 编辑操作
```
Ctrl + C          复制
Ctrl + V          粘贴
Ctrl + X          剪切
Ctrl + Z          撤销
Ctrl + Y          重做
Ctrl + A          全选
Ctrl + F          查找
Ctrl + H          查找替换
Ctrl + Shift + F  全局搜索
```

#### 3. 光标和选择
```
Ctrl + D          选择当前单词（多次按选择相同单词）
Ctrl + L          选择当前行
Alt + ↑/↓         移动行
Shift + Alt + ↑/↓ 复制行
Ctrl + Shift + K  删除行
Ctrl + Enter      在下方插入行
Ctrl + Shift + Enter 在上方插入行
```

### 🚀 高级快捷键

#### 1. 多光标编辑
```
Alt + Click       添加光标
Ctrl + Alt + ↑/↓  在上/下行添加光标
Ctrl + D          选择下一个相同单词
Ctrl + K Ctrl + D 跳过当前选择下一个
Ctrl + U          撤销最后一个光标
Ctrl + Shift + L  选择所有相同单词
```

#### 2. 代码导航
```
Ctrl + G          跳转到指定行号
Ctrl + P          快速打开文件（模糊搜索）
Ctrl + Shift + P  命令面板（所有VSCode命令）
Ctrl + Shift + O  当前文件符号跳转（函数、类、变量）
Ctrl + T          工作区符号搜索（全局搜索）
F12               跳转到定义
Alt + F12         查看定义（预览）
Shift + F12       查看所有引用
Ctrl + -          后退到上一个位置
Ctrl + Shift + -  前进到下一个位置
```

#### 3. 代码编辑
```
Ctrl + /          切换行注释
Shift + Alt + A   切换块注释
Ctrl + [          减少缩进
Ctrl + ]          增加缩进
Ctrl + Shift + \  跳转到匹配的括号
Ctrl + Shift + [  折叠当前区域
Ctrl + Shift + ]  展开当前区域
Ctrl + K Ctrl + 0 折叠所有
Ctrl + K Ctrl + J 展开所有
```

### 🐍 Python 开发专用快捷键

#### 1. 代码运行和调试
```
F5                开始调试
Ctrl + F5         运行（不调试）
F9                切换断点
F10               单步跳过
F11               单步进入
Shift + F11       单步跳出
Shift + F5        停止调试
F8                跳转到下一个错误
Shift + F8        跳转到上一个错误
```

#### 2. Python 特定操作
```
Ctrl + Shift + `  打开新终端
Ctrl + `          切换终端
Ctrl + Shift + P  然后输入 "Python: Select Interpreter"
Ctrl + Shift + M  打开问题面板
```

### 🔧 界面和窗口管理

#### 1. 面板切换
```
Ctrl + Shift + E  资源管理器
Ctrl + Shift + F  搜索
Ctrl + Shift + G  源代码管理（Git）
Ctrl + Shift + D  调试
Ctrl + Shift + X  扩展
Ctrl + J          切换面板
Ctrl + B          切换侧边栏
F11               全屏模式
```

#### 2. 窗口分割
```
Ctrl + \          分割编辑器
Ctrl + 1/2/3      聚焦到编辑器组
Ctrl + W          关闭编辑器
Ctrl + K Ctrl + W 关闭所有编辑器
Ctrl + Shift + N  新建窗口
```

### 📋 常用快捷键速查表

| 分类 | 快捷键 | 功能 |
|------|--------|------|
| **文件** | `Ctrl + N` | 新建文件 |
| | `Ctrl + S` | 保存 |
| | `Ctrl + P` | 快速打开 |
| **编辑** | `Ctrl + D` | 选择相同单词 |
| | `Alt + ↑/↓` | 移动行 |
| | `Ctrl + /` | 注释 |
| **导航** | `Ctrl + G` | 跳转行 |
| | `F12` | 跳转定义 |
| | `Ctrl + Shift + O` | 符号跳转 |
| **调试** | `F5` | 开始调试 |
| | `F9` | 断点 |
| | `F10` | 单步跳过 |

### 🎯 学习建议

#### 循序渐进学习法：
1. **第一周**：掌握基础文件操作（Ctrl+N, S, P, W）
2. **第二周**：学习编辑快捷键（Ctrl+D, /, Alt+↑↓）
3. **第三周**：掌握导航快捷键（F12, Ctrl+G, Ctrl+Shift+O）
4. **第四周**：学习调试快捷键（F5, F9, F10）

#### 实践技巧：
- **每天练习**：选择3-5个快捷键重点练习
- **强制使用**：禁用鼠标右键菜单，强制使用快捷键
- **制作卡片**：把常用快捷键写在便签上
- **工作流整合**：将快捷键融入日常开发流程

### 💡 Python开发工作流快捷键

#### 典型开发流程：
1. `Ctrl + P` → 打开Python文件
2. `Ctrl + Shift + O` → 找到目标函数
3. `F12` → 查看依赖定义
4. `Ctrl + /` → 添加注释
5. `F5` → 运行调试
6. `F9` → 设置断点
7. `F10` → 单步调试
8. `Ctrl + S` → 保存文件

#### 代码重构流程：
1. `Ctrl + D` → 选择要重构的变量
2. `Ctrl + Shift + L` → 选择所有相同变量
3. 直接输入新名称
4. `Shift + F12` → 检查所有引用
5. `Ctrl + S` → 保存更改

### 🔥 高效开发技巧

#### 1. 代码片段快捷键
```
for + Tab         for循环模板
if + Tab          if语句模板
def + Tab         函数定义模板
class + Tab       类定义模板
```

#### 2. 智能感知快捷键
```
Ctrl + Space      触发智能感知
Ctrl + Shift + Space 参数提示
Ctrl + I          快速修复
F2                重命名符号
```

#### 3. 终端集成快捷键
```
Ctrl + Shift + `  新建终端
Ctrl + `          显示/隐藏终端
Ctrl + C          终止当前命令
Ctrl + L          清屏
```

### 🎓 学习建议总结

作为Python初学者，建议你：
1. **从基础开始**：先掌握文件操作和基本编辑
2. **每天练习**：选择几个快捷键重点练习
3. **实际应用**：在编写Python代码时强制使用
4. **循序渐进**：不要一次学太多，分阶段掌握
5. **制作备忘录**：把常用快捷键贴在显示器旁
6. **结合项目**：在实际Python项目中练习使用

记住：熟练使用VSCode快捷键可以让你的编程效率提升50%以上！

------|------|
| `git status` | 查看文件状态 |
| `git add .` | 添加所有文件到暂存区 |
| `git commit -m "信息"` | 提交更改 |
| `git push` | 推送到远程仓库 |
| `git pull` | 从远程仓库拉取 |
| `git log` | 查看提交历史 |
| `git branch` | 查看分支 |
| `git checkout 分支名` | 切换分支 |
| `git merge 分支名` | 合并分支 |

### 🎓 学习建议

作为Python初学者，建议你：
1. **先掌握基础命令**：add, commit, push, pull
2. **多练习**：在你的Python项目中使用Git
3. **理解概念**：工作区、暂存区、仓库的关系
4. **逐步学习高级功能**：分支、合并、回退
5. **养成好习惯**：经常提交，写清楚提交信息

---