# 今日学习步骤
   1. git 语法 ✅
   2. vscode 快捷键
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