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

#### 3. 基本工作流程 ⭐

**Git的核心工作流程（三个区域）：**
```
工作区 → 暂存区 → 本地仓库 → 远程仓库
  ↓        ↓        ↓         ↓
编辑文件   git add  git commit git push
```

**标准开发流程：**
```bash
# 1. 查看当前状态（养成习惯）
git status

# 2. 查看文件变化
git diff                    # 查看工作区变化
git diff --staged          # 查看暂存区变化

# 3. 添加文件到暂存区
git add 文件名.txt          # 添加单个文件
git add .                   # 添加所有文件
git add *.py               # 添加所有Python文件
git add src/               # 添加整个目录

# 4. 提交更改
git commit -m "提交信息"     # 提交暂存区的文件
git commit -am "提交信息"    # 添加并提交已跟踪的文件

# 5. 推送到远程仓库
git push                    # 推送当前分支
git push origin main        # 指定分支推送

# 6. 查看提交历史
git log                     # 详细历史
git log --oneline          # 简洁历史
git log --graph            # 图形化显示
```

**每日开发标准流程：**
```bash
# 开始工作前
git status                  # 检查状态
git pull                    # 拉取最新代码

# 开发过程中
# ... 编辑代码 ...
git add .                   # 添加修改
git commit -m "描述性信息"   # 提交修改

# 工作结束时
git push                    # 推送到远程
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
|------|------|
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

## 2. VSCode 快捷键详解

### 🎯 为什么要学习快捷键？
- **提高效率**：减少鼠标操作，专注编码
- **专业开发**：快速导航和编辑代码
- **减少疲劳**：避免频繁切换鼠标键盘
- **流畅体验**：让编程变得更加顺畅

### ⌨️ 基础快捷键

#### 1. 文件操作
```
Ctrl + N          新建文件
Ctrl + O          打开文件
Ctrl + S          保存文件
Ctrl + Shift + S  另存为
Ctrl + W          关闭当前文件
Ctrl + Shift + T  重新打开关闭的文件
Ctrl + K, Ctrl + O 打开文件夹
```

#### 2. 编辑操作
```
Ctrl + Z          撤销
Ctrl + Y          重做
Ctrl + X          剪切
Ctrl + C          复制
Ctrl + V          粘贴
Ctrl + A          全选
Ctrl + F          查找
Ctrl + H          替换
Ctrl + D          选择下一个相同单词
Ctrl + Shift + L  选择所有相同单词
```

#### 3. 光标和选择
```
Home              行首
End               行尾
Ctrl + Home       文件开头
Ctrl + End        文件结尾
Ctrl + ←/→        按单词移动光标
Shift + ←/→       选择字符
Ctrl + Shift + ←/→ 按单词选择
Shift + ↑/↓       选择行
Alt + ↑/↓         移动行
Shift + Alt + ↑/↓ 复制行
```

### 🚀 高级快捷键

#### 1. 多光标编辑
```
Alt + Click       添加光标
Ctrl + Alt + ↑/↓  在上/下行添加光标
Ctrl + Shift + L  在所有选中行末尾添加光标
Ctrl + D          选择下一个相同单词（多光标）
Esc               退出多光标模式
```

#### 2. 代码导航 ⭐

##### 🎯 学习目标
- 快速在代码库中定位和跳转
- 理解代码结构和依赖关系
- 提高代码阅读和调试效率

##### 📍 基础导航快捷键
```
Ctrl + G          跳转到指定行号
Ctrl + P          快速打开文件（模糊搜索）
Ctrl + Shift + P  命令面板（所有VSCode命令）
Ctrl + Shift + O  当前文件符号跳转（函数、类、变量）
Ctrl + T          工作区符号搜索（全局搜索）
Ctrl + Shift + F  全局文件内容搜索
```

##### 🔍 代码定义和引用
```
F12               跳转到定义（Go to Definition）
Alt + F12         查看定义（Peek Definition）
Shift + F12       查看所有引用（Find All References）
Ctrl + K F12      在侧边打开定义
Ctrl + Shift + F12 查看实现（Go to Implementation）
```

##### ⬅️➡️ 导航历史
```
Ctrl + -          后退到上一个位置
Ctrl + Shift + -  前进到下一个位置
Alt + ←           后退（备用）
Alt + →           前进（备用）
```

##### 🔄 面包屑导航
```
Ctrl + Shift + .  聚焦面包屑
↑↓←→             面包屑中导航
Enter            选择面包屑项
```

##### 📂 文件浏览器导航
```
Ctrl + Shift + E  打开/聚焦文件浏览器
↑↓               上下选择文件
→                展开文件夹
←                收起文件夹
Enter            打开文件
Space            预览文件
```

##### 🎯 实用导航技巧

**1. 快速文件切换**
```
Ctrl + Tab        在最近文件间切换
Ctrl + P, @       当前文件符号搜索
Ctrl + P, #       工作区符号搜索
Ctrl + P, :       跳转到行号
```

**2. 多光标导航**
```
Ctrl + D          选择下一个相同单词
Ctrl + K Ctrl + D 跳过当前选择下一个
Ctrl + U          撤销最后一个光标
Alt + Click       添加光标
```

**3. 代码折叠导航**
```
Ctrl + Shift + [  折叠当前区域
Ctrl + Shift + ]  展开当前区域
Ctrl + K Ctrl + 0 折叠所有
Ctrl + K Ctrl + J 展开所有
```

##### 🐍 Python 特定导航

**1. Python 符号导航**
```
Ctrl + Shift + O  跳转到类/函数/方法
@:                只显示函数和方法
@                 显示所有符号
```

**2. 导入和模块导航**
```
F12               跳转到导入的模块定义
Alt + F12         预览导入模块
Ctrl + Click      快速跳转到定义
```

**3. 错误和警告导航**
```
F8                下一个错误/警告
Shift + F8        上一个错误/警告
Ctrl + Shift + M  打开问题面板
```

##### 💡 高效导航工作流

**日常开发流程：**
1. `Ctrl + P` → 快速打开文件
2. `Ctrl + Shift + O` → 找到目标函数
3. `F12` → 跳转到依赖定义
4. `Shift + F12` → 查看函数被调用的地方
5. `Ctrl + -` → 返回原位置

**代码审查流程：**
1. `Ctrl + Shift + F` → 搜索关键词
2. `F12` → 查看函数定义
3. `Alt + F12` → 预览相关代码
4. `Ctrl + T` → 搜索相关符号

**调试导航流程：**
1. `F8` → 跳转到错误位置
2. `F12` → 查看错误相关定义
3. `Ctrl + Shift + F` → 搜索错误信息
4. `Shift + F12` → 查看相关引用

##### 📚 学习建议

**第一阶段（基础导航）：**
- 熟练使用 `Ctrl + P` 打开文件
- 掌握 `Ctrl + G` 行号跳转
- 学会 `F12` 跳转定义

**第二阶段（符号导航）：**
- 使用 `Ctrl + Shift + O` 文件内导航
- 掌握 `Ctrl + T` 全局符号搜索
- 学会 `Shift + F12` 查看引用

**第三阶段（高级技巧）：**
- 熟练使用面包屑导航
- 掌握多光标导航技巧
- 建立高效的导航工作流

**实践建议：**
- 每天强制使用快捷键导航，避免鼠标点击
- 在大型项目中练习符号搜索和跳转
- 结合调试功能练习错误导航
- 制作个人常用导航快捷键卡片

#### 3. 代码编辑
```
Ctrl + /          切换行注释
Shift + Alt + A   切换块注释
Ctrl + [          减少缩进
Ctrl + ]          增加缩进
Ctrl + Shift + K  删除行
Ctrl + Enter      在下方插入行
Ctrl + Shift + Enter 在上方插入行
Ctrl + Shift + \  跳转到匹配的括号
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
```

#### 2. Python 特定操作
```
Ctrl + Shift + `  打开新终端
Ctrl + `          切换终端
Ctrl + Shift + P  然后输入 "Python: Select Interpreter"
F8                跳转到下一个错误
Shift + F8        跳转到上一个错误
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
```

#### 2. 窗口分割
```
Ctrl + \          分割编辑器
Ctrl + 1/2/3      聚焦到编辑器组
Ctrl + W          关闭编辑器
Ctrl + K, Ctrl + W 关闭所有编辑器
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
- **结合项目**：在实际Python项目中应用

#### Python开发工作流：
```
1. Ctrl + P → 打开文件
2. Ctrl + Shift + ` → 打开终端
3. 编写代码 → 使用 Ctrl + D, Alt + ↑↓ 等编辑
4. F5 → 调试运行
5. Ctrl + S → 保存
6. Ctrl + Shift + G → Git提交
```

### 💡 高效开发技巧

1. **自定义快捷键**：File → Preferences → Keyboard Shortcuts
2. **使用代码片段**：输入缩写 + Tab
3. **智能感知**：Ctrl + Space 触发代码补全
4. **快速修复**：Ctrl + . 显示快速修复选项
5. **格式化代码**：Shift + Alt + F

---